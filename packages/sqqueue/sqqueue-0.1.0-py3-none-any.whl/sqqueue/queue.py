# sqqueue/queue.py

import datetime
import logging
import os
import sqlite3
import threading
import time
from contextlib import contextmanager
from typing import Any, List, Optional, Tuple

# Optional statsd integration
try:
    from statsd import StatsClient
except ImportError:
    StatsClient = None

from .config import setup_logging
from .exceptions import (
    CompletionError,
    DequeueError,
    EnqueueError,
    QueueError,
    RequeueError,
)
from .result import Err, Ok, Result


class SQLiteQueue:
    """
    A SQLite-based persistent queue implementation with enhanced SQLite defaults,
    Write-Ahead Logging (WAL), VACUUM maintenance, priority queues, delayed messages,
    message visibility timeouts, dead-letter queues (DLQ), batch operations, and optional
    StatsD metrics integration.

    Attributes:
        db_path (str): Path to the SQLite database file.
        table_name (str): Name of the queue table.
        logger (logging.Logger): Logger instance.
        statsd_client (Optional[StatsClient]): Optional StatsD client for metrics.
    """

    def __init__(
        self,
        db_path: str = "queue.db",
        table_name: str = "message_queue",
        vacuum_threshold: int = 1000,  # Number of operations after which to vacuum
        vacuum_on_start: bool = False,  # Whether to perform VACUUM on initialization
        statsd_host: Optional[str] = None,  # StatsD server host
        statsd_port: Optional[int] = None,  # StatsD server port
        statsd_prefix: str = "sqqueue",  # Prefix for all statsd metrics
        default_priority: int = 0,
        default_visibility_timeout: int = 300,  # in seconds
        default_max_attempts: int = 5,
    ):
        """
        Initializes the SQLiteQueue with enhanced features.

        Args:
            db_path (str): Path to the SQLite database file.
            table_name (str): Name of the queue table.
            vacuum_threshold (int): Number of operations after which to perform VACUUM.
            vacuum_on_start (bool): Whether to perform VACUUM upon initialization.
            statsd_host (Optional[str]): Hostname of the StatsD server.
            statsd_port (Optional[int]): Port of the StatsD server.
            statsd_prefix (str): Prefix for StatsD metrics.
            default_priority (int): Default priority for messages.
            default_visibility_timeout (int): Default visibility timeout in seconds.
            default_max_attempts (int): Default maximum processing attempts.
            recovery_interval (int): Interval in seconds for recovery thread to run.
        """
        self.db_path = db_path
        self.table_name = table_name
        self.logger = setup_logging()
        self._lock = threading.Lock()
        self._operation_count = 0
        self._vacuum_threshold = vacuum_threshold
        self.default_priority = default_priority
        self.default_visibility_timeout = default_visibility_timeout
        self.default_max_attempts = default_max_attempts

        # Initialize StatsD client if host and port are provided and statsd is available
        if statsd_host and statsd_port and StatsClient:
            self.statsd_client = StatsClient(
                host=statsd_host, port=statsd_port, prefix=statsd_prefix
            )
            self.logger.info("StatsD client initialized.")
        elif statsd_host or statsd_port:
            self.logger.warning(
                "StatsD configuration provided but 'statsd' package is not installed. Metrics will be disabled."
            )
            self.statsd_client = None
        else:
            self.statsd_client = None

        self._initialize_db()
        if vacuum_on_start:
            with self._lock, self._get_connection() as conn:
                self.vacuum_database(conn)

    def _initialize_db(self):
        """Creates the queue table and dead-letter queue table if they do not exist and sets SQLite PRAGMA settings."""
        try:
            with self._get_connection() as conn:
                # Set PRAGMA settings for sensible defaults
                conn.execute("PRAGMA journal_mode = WAL;")
                conn.execute(
                    "PRAGMA synchronous = NORMAL;"
                )  # Balance between performance and durability
                conn.execute("PRAGMA foreign_keys = ON;")
                conn.execute("PRAGMA temp_store = MEMORY;")
                conn.execute("PRAGMA cache_size = 10000;")  # Adjust as needed

                # Create the main message queue table
                conn.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        payload TEXT NOT NULL,
                        status TEXT NOT NULL DEFAULT 'pending',
                        priority INTEGER NOT NULL DEFAULT 0,
                        visible_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        processing_at DATETIME,
                        attempts INTEGER DEFAULT 0,
                        max_attempts INTEGER DEFAULT 5,
                        dlq TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                """
                )

                # Create the dead-letter queue table
                dlq_name = self.table_name + "_dlq"
                conn.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS {dlq_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        payload TEXT NOT NULL,
                        status TEXT NOT NULL DEFAULT 'dead',
                        priority INTEGER NOT NULL DEFAULT 0,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                """
                )

                # Create an index to optimize status and id queries
                conn.execute(
                    f"""
                    CREATE INDEX IF NOT EXISTS idx_status_id ON {self.table_name} (status, id);
                """
                )

                conn.commit()
            self.logger.debug(
                f"Initialized database with PRAGMA settings and ensured tables '{self.table_name}' and '{dlq_name}' exist."
            )
        except sqlite3.Error as e:
            self.logger.error(f"Failed to initialize database: {e}")
            raise QueueError(f"Database initialization failed: {e}")

    def recover_processing_messages(self) -> Result[int, QueueError]:
        """
        Public method to recover messages with expired visibility timeouts.
        Resets messages stuck in 'processing' status back to 'pending'.

        Returns:
            Result[int, QueueError]: Ok(count) if successful, Err(QueueError) otherwise.
        """
        try:
            with self._get_connection() as conn:
                current_time = datetime.datetime.utcnow()
                self.logger.debug(
                    f"Recovery: Starting at {current_time.isoformat()} UTC."
                )
                cursor = conn.execute(
                    f"""
                    SELECT COUNT(*) FROM {self.table_name}
                    WHERE status = 'processing' AND processing_at <= ?;
                """,
                    (current_time,),
                )
                count = cursor.fetchone()[0]
                self.logger.debug(f"Recovery: Found {count} messages to recover.")
                if count > 0:
                    conn.execute(
                        f"""
                        UPDATE {self.table_name}
                        SET status = 'pending', processing_at = NULL, updated_at = CURRENT_TIMESTAMP
                        WHERE status = 'processing' AND processing_at <= ?;
                    """,
                        (current_time,),
                    )
                    conn.commit()
                    self.logger.info(
                        f"Recovered {count} messages from 'processing' to 'pending' due to visibility timeout."
                    )
                    # Emit StatsD metrics if enabled
                    if self.statsd_client:
                        self.statsd_client.incr("recovered_messages", count)
                else:
                    self.logger.debug(
                        "Recovery: No messages needed recovery at this time."
                    )
            return Ok(count)
        except sqlite3.Error as e:
            self.logger.error(f"Failed to recover processing messages: {e}")
            return Err(QueueError(f"Recovery of processing messages failed: {e}"))

    @contextmanager
    def _get_connection(self):
        """Context manager for SQLite connection with retry mechanism and PRAGMA settings."""
        retries = 5
        delay = 0.1  # Initial delay in seconds
        for attempt in range(retries):
            try:
                conn = sqlite3.connect(
                    self.db_path,
                    timeout=30,
                    check_same_thread=False,
                    isolation_level=None,  # Autocommit mode
                )
                # Apply PRAGMA settings
                conn.execute("PRAGMA foreign_keys = ON;")
                conn.execute("PRAGMA journal_mode = WAL;")  # Ensure WAL mode
                conn.execute(
                    "PRAGMA synchronous = NORMAL;"
                )  # Balance performance and durability
                conn.execute("PRAGMA temp_store = MEMORY;")
                conn.execute("PRAGMA cache_size = 10000;")  # Adjust as needed

                yield conn
                conn.close()
                break
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    self.logger.error(f"Database connection possibly stale: {e}")
                    conn.rollback()
                    conn.close()
                    break
                if "database is locked" in str(e):
                    self.logger.warning(
                        f"Database is locked, retrying in {delay} seconds..."
                    )
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    self.logger.error(f"OperationalError during connection: {e}")
                    raise
        else:
            self.logger.error(
                "Failed to acquire database connection after multiple attempts."
            )
            raise QueueError("Database is locked and cannot be accessed.")

    def enqueue(
        self,
        payload: str,
        priority: Optional[int] = None,
        delay: int = 0,
        max_attempts: Optional[int] = None,
    ) -> Result[int, EnqueueError]:
        """
        Adds a new payload to the queue with optional priority, delay, and max_attempts.

        Args:
            payload (str): The message or task data to enqueue.
            priority (Optional[int]): The priority level of the message. Higher values indicate higher priority.
            delay (int): Delay in seconds before the message becomes available for processing.
            max_attempts (Optional[int]): Maximum number of processing attempts for the message.

        Returns:
            Result[int, EnqueueError]: Ok(message_id) if successful, Err(EnqueueError) otherwise.
        """
        priority = priority if priority is not None else self.default_priority
        max_attempts = (
            max_attempts if max_attempts is not None else self.default_max_attempts
        )
        try:
            visible_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=delay)
            with self._lock, self._get_connection() as conn:
                cursor = conn.execute(
                    f"""
                    INSERT INTO {self.table_name} (payload, status, priority, visible_at, max_attempts)
                    VALUES (?, 'pending', ?, ?, ?);
                """,
                    (payload, priority, visible_at, max_attempts),
                )
                message_id = cursor.lastrowid
                self.logger.debug(
                    f"Enqueued message ID {message_id}: {payload} with priority {priority}, delay {delay}s, max_attempts {max_attempts}"
                )

                # Emit StatsD metrics
                if self.statsd_client:
                    self.statsd_client.incr("enqueue")
                    self.statsd_client.incr(f"enqueue_priority_{priority}")
                    self._emit_queue_size(conn)

                self._increment_operation_count(conn)
                return Ok(message_id)
        except sqlite3.Error as e:
            self.logger.error(f"Failed to enqueue message: {e}")
            return Err(EnqueueError(f"Enqueue failed: {e}"))

    def dequeue(
        self, visibility_timeout: Optional[int] = None
    ) -> Result[Optional[Tuple[int, str]], DequeueError]:
        """
        Retrieves and marks the next pending message as 'processing',
        prioritizing higher-priority messages and respecting visibility delays.
        Sets a visibility timeout after which the message becomes visible again if not completed.

        Args:
            visibility_timeout (Optional[int]): Time in seconds before the message becomes visible again.

        Returns:
            Result[Optional[Tuple[int, str]], DequeueError]: Ok((message_id, payload)) if a message is available,
                                                             Ok(None) if no message is available,
                                                             Err(DequeueError) otherwise.
        """
        visibility_timeout = (
            visibility_timeout
            if visibility_timeout is not None
            else self.default_visibility_timeout
        )
        try:
            with self._lock, self._get_connection() as conn:
                conn.execute("BEGIN EXCLUSIVE;")
                current_time = datetime.datetime.utcnow()
                cursor = conn.execute(
                    f"""
                    SELECT id, payload, priority, attempts, max_attempts FROM {self.table_name}
                    WHERE status = 'pending' AND visible_at <= ?
                    ORDER BY priority DESC, id ASC
                    LIMIT 1;
                """,
                    (current_time,),
                )
                row = cursor.fetchone()
                if row:
                    message_id, payload, priority, attempts, max_attempts = row
                    if attempts >= max_attempts:
                        # Move to dead-letter queue
                        dlq_name = self.table_name + "_dlq"
                        conn.execute(
                            f"""
                            INSERT INTO {dlq_name} (payload, status, priority, created_at, updated_at)
                            VALUES (?, 'dead', ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
                        """,
                            (payload, priority),
                        )
                        conn.execute(
                            f"""
                            DELETE FROM {self.table_name} WHERE id = ?;
                        """,
                            (message_id,),
                        )
                        conn.commit()
                        self.logger.warning(
                            f"Moved message ID {message_id} to dead-letter queue '{dlq_name}' after {attempts} attempts."
                        )
                        # Emit StatsD metrics
                        if self.statsd_client:
                            self.statsd_client.incr("dead_letter")
                        return Ok(None)

                    # Proceed to dequeue the message
                    processing_time = current_time + datetime.timedelta(
                        seconds=visibility_timeout
                    )
                    conn.execute(
                        f"""
                        UPDATE {self.table_name}
                        SET status = 'processing', processing_at = ?, attempts = attempts + 1, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?;
                    """,
                        (processing_time, message_id),
                    )
                    conn.commit()
                    self.logger.debug(
                        f"Dequeued message ID {message_id}: {payload} with priority {priority}, visibility_timeout {visibility_timeout}s (Attempt {attempts + 1})"
                    )

                    # Emit StatsD metrics
                    if self.statsd_client:
                        self.statsd_client.incr("dequeue")
                        self.statsd_client.incr(f"dequeue_priority_{priority}")
                        self._emit_queue_size(conn)

                    self._increment_operation_count(conn)
                    return Ok((message_id, payload))
                else:
                    conn.commit()
                    self.logger.debug("Dequeue called but no pending messages found.")
                    return Ok(None)
        except sqlite3.Error as e:
            self.logger.error(f"Failed to dequeue message: {e}")
            return Err(DequeueError(f"Dequeue failed: {e}"))

    def complete(self, message_id: int) -> Result[None, CompletionError]:
        """
        Marks a message as completed by deleting it from the queue.

        Args:
            message_id (int): The ID of the message to complete.

        Returns:
            Result[None, CompletionError]: Ok(None) if successful, Err(CompletionError) otherwise.
        """
        try:
            with self._lock, self._get_connection() as conn:
                conn.execute(
                    f"""
                    DELETE FROM {self.table_name}
                    WHERE id = ? AND status = 'processing';
                """,
                    (message_id,),
                )
                if conn.total_changes == 0:
                    self.logger.warning(
                        f"No message with ID {message_id} in 'processing' state to complete."
                    )
                    return Err(
                        CompletionError(
                            f"Message ID {message_id} not found or not in 'processing' state."
                        )
                    )
                conn.commit()
                self.logger.debug(f"Completed and removed message ID {message_id}.")

                # Emit StatsD metrics
                if self.statsd_client:
                    self.statsd_client.incr("complete")
                    self._emit_queue_size(conn)

                self._increment_operation_count(conn)
                return Ok(None)
        except sqlite3.Error as e:
            self.logger.error(f"Failed to complete message ID {message_id}: {e}")
            return Err(
                CompletionError(f"Completion failed for message ID {message_id}: {e}")
            )

    def requeue(self, message_id: int) -> Result[None, RequeueError]:
        """
        Requeues a message by setting its status back to 'pending'.

        Args:
            message_id (int): The ID of the message to requeue.

        Returns:
            Result[None, RequeueError]: Ok(None) if successful, Err(RequeueError) otherwise.
        """
        try:
            with self._lock, self._get_connection() as conn:
                conn.execute(
                    f"""
                    UPDATE {self.table_name}
                    SET status = 'pending', processing_at = NULL, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ? AND status = 'processing';
                """,
                    (message_id,),
                )
                if conn.total_changes == 0:
                    self.logger.warning(
                        f"No message with ID {message_id} in 'processing' state to requeue."
                    )
                    return Err(
                        RequeueError(
                            f"Message ID {message_id} not found or not in 'processing' state."
                        )
                    )
                conn.commit()
                self.logger.debug(f"Requeued message ID {message_id}.")

                # Emit StatsD metrics if enabled
                if self.statsd_client:
                    self.statsd_client.incr("requeue")
                    self._emit_queue_size(conn)

                self._increment_operation_count(conn)
                return Ok(None)
        except sqlite3.Error as e:
            self.logger.error(f"Failed to requeue message ID {message_id}: {e}")
            return Err(RequeueError(f"Requeue failed for message ID {message_id}: {e}"))

    def enqueue_batch(
        self, payloads: List[Tuple[str, int, int, Optional[int]]]
    ) -> Result[List[int], EnqueueError]:
        """
        Adds multiple payloads to the queue in a single transaction.

        Args:
            payloads (List[Tuple[str, int, int, Optional[int]]]): A list of tuples containing (payload, priority, delay, max_attempts).

        Returns:
            Result[List[int], EnqueueError]: Ok(list_of_message_ids) if successful, Err(EnqueueError) otherwise.
        """
        try:
            with self._lock, self._get_connection() as conn:
                message_ids = []
                for payload, priority, delay, max_attempts in payloads:
                    priority = (
                        priority if priority is not None else self.default_priority
                    )
                    max_attempts = (
                        max_attempts
                        if max_attempts is not None
                        else self.default_max_attempts
                    )
                    visible_at = datetime.datetime.utcnow() + datetime.timedelta(
                        seconds=delay
                    )
                    cursor = conn.execute(
                        f"""
                        INSERT INTO {self.table_name} (payload, status, priority, visible_at, max_attempts)
                        VALUES (?, 'pending', ?, ?, ?);
                    """,
                        (payload, priority, visible_at, max_attempts),
                    )
                    message_ids.append(cursor.lastrowid)
                    self.logger.debug(
                        f"Enqueued message ID {cursor.lastrowid}: {payload} with priority {priority}, delay {delay}s, max_attempts {max_attempts}"
                    )

                # Emit StatsD metrics
                if self.statsd_client:
                    self.statsd_client.incr("enqueue", len(payloads))
                    self._emit_queue_size(conn)

                self._increment_operation_count(conn)
                return Ok(message_ids)
        except sqlite3.Error as e:
            self.logger.error(f"Failed to enqueue batch messages: {e}")
            return Err(EnqueueError(f"Batch enqueue failed: {e}"))

    def dequeue_batch(
        self, batch_size: int = 10, visibility_timeout: Optional[int] = None
    ) -> Result[List[Tuple[int, str]], DequeueError]:
        """
        Retrieves and marks multiple pending messages as 'processing',
        prioritizing higher-priority messages and respecting visibility delays.
        Sets a visibility timeout after which the messages become visible again if not completed.

        Args:
            batch_size (int): The maximum number of messages to dequeue.
            visibility_timeout (Optional[int]): Time in seconds before the messages become visible again.

        Returns:
            Result[List[Tuple[int, str]], DequeueError]: Ok(list_of_messages) if successful, Err(DequeueError) otherwise.
        """
        visibility_timeout = (
            visibility_timeout
            if visibility_timeout is not None
            else self.default_visibility_timeout
        )
        try:
            with self._lock, self._get_connection() as conn:
                conn.execute("BEGIN EXCLUSIVE;")
                current_time = datetime.datetime.utcnow()
                cursor = conn.execute(
                    f"""
                    SELECT id, payload, priority, attempts, max_attempts FROM {self.table_name}
                    WHERE status = 'pending' AND visible_at <= ?
                    ORDER BY priority DESC, id ASC
                    LIMIT ?;
                """,
                    (current_time, batch_size),
                )
                rows = cursor.fetchall()
                if rows:
                    messages = []
                    for row in rows:
                        message_id, payload, priority, attempts, max_attempts = row
                        if attempts >= max_attempts:
                            # Move to dead-letter queue
                            dlq_name = self.table_name + "_dlq"
                            conn.execute(
                                f"""
                                INSERT INTO {dlq_name} (payload, status, priority, created_at, updated_at)
                                VALUES (?, 'dead', ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
                            """,
                                (payload, priority),
                            )
                            conn.execute(
                                f"""
                                DELETE FROM {self.table_name} WHERE id = ?;
                            """,
                                (message_id,),
                            )
                            self.logger.warning(
                                f"Moved message ID {message_id} to dead-letter queue '{dlq_name}' after {attempts} attempts."
                            )
                            # Emit StatsD metrics
                            if self.statsd_client:
                                self.statsd_client.incr("dead_letter")
                        else:
                            # Dequeue the message
                            processing_time = current_time + datetime.timedelta(
                                seconds=visibility_timeout
                            )
                            conn.execute(
                                f"""
                                UPDATE {self.table_name}
                                SET status = 'processing', processing_at = ?, attempts = attempts + 1, updated_at = CURRENT_TIMESTAMP
                                WHERE id = ?;
                            """,
                                (processing_time, message_id),
                            )
                            messages.append((message_id, payload))
                            self.logger.debug(
                                f"Dequeued message ID {message_id}: {payload} with priority {priority}, visibility_timeout {visibility_timeout}s (Attempt {attempts + 1})"
                            )

                    conn.commit()

                    # Emit StatsD metrics
                    if self.statsd_client:
                        self.statsd_client.incr("dequeue", len(messages))
                        self._emit_queue_size(conn)

                    self._increment_operation_count(conn)
                    return Ok(messages)
                else:
                    conn.commit()
                    self.logger.debug(
                        "Dequeue batch called but no pending messages found."
                    )
                    return Ok([])
        except sqlite3.Error as e:
            self.logger.error(f"Failed to dequeue batch messages: {e}")
            return Err(DequeueError(f"Batch dequeue failed: {e}"))

    def fail_message(
        self, message_id: int, send_to_dlq: bool = False
    ) -> Result[None, CompletionError]:
        """
        Marks a message as failed. Optionally moves it to the dead-letter queue.

        Args:
            message_id (int): The ID of the message to fail.
            send_to_dlq (bool): Whether to move the failed message to the dead-letter queue.

        Returns:
            Result[None, CompletionError]: Ok(None) if successful, Err(CompletionError) otherwise.
        """
        try:
            with self._lock, self._get_connection() as conn:
                if send_to_dlq:
                    dlq_name = self.table_name + "_dlq"
                    cursor = conn.execute(
                        f"""
                        SELECT payload, priority FROM {self.table_name}
                        WHERE id = ? AND status = 'processing';
                    """,
                        (message_id,),
                    )
                    row = cursor.fetchone()
                    if row:
                        payload, priority = row
                        conn.execute(
                            f"""
                            INSERT INTO {dlq_name} (payload, status, priority, created_at, updated_at)
                            VALUES (?, 'dead', ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
                        """,
                            (payload, priority),
                        )
                        conn.execute(
                            f"""
                            DELETE FROM {self.table_name}
                            WHERE id = ?;
                        """,
                            (message_id,),
                        )
                        self.logger.debug(
                            f"Moved failed message ID {message_id} to dead-letter queue '{dlq_name}'."
                        )
                        # Emit StatsD metrics
                        if self.statsd_client:
                            self.statsd_client.incr("dead_letter")
                    else:
                        self.logger.warning(
                            f"No message with ID {message_id} in 'processing' state to fail."
                        )
                        raise CompletionError(
                            f"Message ID {message_id} not found or not in 'processing' state."
                        )
                else:
                    # Requeue the message
                    conn.execute(
                        f"""
                        UPDATE {self.table_name}
                        SET status = 'pending', processing_at = NULL, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ? AND status = 'processing';
                    """,
                        (message_id,),
                    )
                    if conn.total_changes == 0:
                        self.logger.warning(
                            f"No message with ID {message_id} in 'processing' state to fail."
                        )
                        raise CompletionError(
                            f"Message ID {message_id} not found or not in 'processing' state."
                        )
                    self.logger.debug(f"Requeued failed message ID {message_id}.")
                    # Emit StatsD metrics
                    if self.statsd_client:
                        self.statsd_client.incr("fail")
                        self._emit_queue_size(conn)

                conn.commit()
                self._increment_operation_count(conn)
                return Ok(None)
        except sqlite3.Error as e:
            self.logger.error(f"Failed to fail message ID {message_id}: {e}")
            return Err(
                CompletionError(
                    f"Fail operation failed for message ID {message_id}: {e}"
                )
            )

    def get_dead_letters(self) -> Result[List[dict], QueueError]:
        """
        Retrieves all messages from the dead-letter queue.

        Returns:
            Result[List[dict], QueueError]: Ok(list_of_dead_letters) if successful, Err(QueueError) otherwise.
        """
        dlq_name = self.table_name + "_dlq"
        try:
            with self._lock, self._get_connection() as conn:
                cursor = conn.execute(
                    f"""
                    SELECT id, payload, priority, created_at, updated_at
                    FROM {dlq_name};
                """
                )
                messages = [
                    {
                        "id": row[0],
                        "payload": row[1],
                        "priority": row[2],
                        "created_at": row[3],
                        "updated_at": row[4],
                    }
                    for row in cursor.fetchall()
                ]
                self.logger.debug(
                    f"Retrieved {len(messages)} messages from dead-letter queue '{dlq_name}'."
                )
                return Ok(messages)
        except sqlite3.Error as e:
            self.logger.error(f"Failed to retrieve dead-letter messages: {e}")
            return Err(QueueError(f"Retrieval of dead-letter messages failed: {e}"))

    def reprocess_dead_letter(self, message_id: int) -> Result[None, RequeueError]:
        """
        Re-enqueues a message from the dead-letter queue back to the main queue.

        Args:
            message_id (int): The ID of the message to reprocess.

        Returns:
            Result[None, RequeueError]: Ok(None) if successful, Err(RequeueError) otherwise.
        """
        dlq_name = self.table_name + "_dlq"
        try:
            with self._lock, self._get_connection() as conn:
                cursor = conn.execute(
                    f"""
                    SELECT payload, priority FROM {dlq_name}
                    WHERE id = ?;
                """,
                    (message_id,),
                )
                row = cursor.fetchone()
                if row:
                    payload, priority = row
                    conn.execute(
                        f"""
                        INSERT INTO {self.table_name} (payload, status, priority, visible_at, max_attempts)
                        VALUES (?, 'pending', ?, CURRENT_TIMESTAMP, {self.default_max_attempts});
                    """,
                        (payload, priority),
                    )
                    conn.execute(
                        f"""
                        DELETE FROM {dlq_name} WHERE id = ?;
                    """,
                        (message_id,),
                    )
                    conn.commit()
                    self.logger.debug(
                        f"Reprocessed message ID {message_id} from dead-letter queue back to main queue."
                    )
                    # Emit StatsD metrics
                    if self.statsd_client:
                        self.statsd_client.incr("reprocess_dead_letter")
                        self._emit_queue_size(conn)
                    return Ok(None)
                else:
                    self.logger.warning(
                        f"No message with ID {message_id} found in dead-letter queue '{dlq_name}'."
                    )
                    raise RequeueError(
                        f"Message ID {message_id} not found in dead-letter queue."
                    )
        except sqlite3.Error as e:
            self.logger.error(
                f"Failed to reprocess dead-letter message ID {message_id}: {e}"
            )
            return Err(
                RequeueError(f"Reprocess failed for message ID {message_id}: {e}")
            )

    def get_all_statuses(self) -> Result[dict, QueueError]:
        """
        Retrieves a count of messages in each status.

        Returns:
            Result[dict, QueueError]: Ok(status_counts) if successful, Err(QueueError) otherwise.
        """
        try:
            with self._lock, self._get_connection() as conn:
                cursor = conn.execute(
                    f"""
                    SELECT status, COUNT(*) FROM {self.table_name}
                    GROUP BY status;
                """
                )
                statuses = {row[0]: row[1] for row in cursor.fetchall()}
                self.logger.debug(f"Current queue statuses: {statuses}")
                return Ok(statuses)
        except sqlite3.Error as e:
            self.logger.error(f"Failed to retrieve message statuses: {e}")
            return Err(QueueError(f"Status retrieval failed: {e}"))

    def peek(self) -> Result[Optional[Tuple[int, str]], QueueError]:
        """
        Peeks at the next pending message without marking it as 'processing'.

        Returns:
            Result[Optional[Tuple[int, str]], QueueError]: Ok((message_id, payload)) if a message is available,
                                                          Ok(None) if no message is available,
                                                          Err(QueueError) otherwise.
        """
        try:
            with self._lock, self._get_connection() as conn:
                current_time = datetime.datetime.utcnow()
                cursor = conn.execute(
                    f"""
                    SELECT id, payload FROM {self.table_name}
                    WHERE status = 'pending' AND visible_at <= ?
                    ORDER BY priority DESC, id ASC
                    LIMIT 1;
                """,
                    (current_time,),
                )
                row = cursor.fetchone()
                if row:
                    self.logger.debug(f"Peeked at message ID {row[0]}: {row[1]}")
                else:
                    self.logger.debug("Peek called but no pending messages found.")
                return Ok(row)
        except sqlite3.Error as e:
            self.logger.error(f"Failed to peek at message: {e}")
            return Err(QueueError(f"Peek failed: {e}"))

    def is_empty(self) -> Result[bool, QueueError]:
        """
        Checks if the queue is empty.

        Returns:
            Result[bool, QueueError]: Ok(True) if empty, Ok(False) otherwise,
                                      Err(QueueError) if the check operation fails.
        """
        try:
            with self._lock, self._get_connection() as conn:
                current_time = datetime.datetime.utcnow()
                cursor = conn.execute(
                    f"""
                    SELECT 1 FROM {self.table_name} WHERE status = 'pending' AND visible_at <= ? LIMIT 1;
                """,
                    (current_time,),
                )
                empty = cursor.fetchone() is None
                self.logger.debug(f"Queue is_empty check: {empty}")
                return Ok(empty)
        except sqlite3.Error as e:
            self.logger.error(f"Failed to check if queue is empty: {e}")
            return Err(QueueError(f"is_empty check failed: {e}"))

    def vacuum_database(self, conn: sqlite3.Connection) -> Result[None, QueueError]:
        """
        Performs a VACUUM operation to clean and defragment the database.

        Returns:
            Result[None, QueueError]: Ok(None) if successful, Err(QueueError) otherwise.
        """
        try:
            conn.execute("VACUUM;")
            self.logger.info("Performed VACUUM on the database.")
            # Emit StatsD metric for maintenance
            if self.statsd_client:
                self.statsd_client.incr("vacuum")
            return Ok(None)
        except sqlite3.Error as e:
            self.logger.error(f"Failed to perform VACUUM: {e}")
            return Err(QueueError(f"VACUUM operation failed: {e}"))

    def perform_checkpoint(self, conn: sqlite3.Connection) -> Result[None, QueueError]:
        """
        Performs a WAL checkpoint to merge WAL logs back into the main database.

        Returns:
            Result[None, QueueError]: Ok(None) if successful, Err(QueueError) otherwise.
        """
        try:
            conn.execute("PRAGMA wal_checkpoint(FULL);")
            self.logger.info("Performed WAL checkpoint.")
            # Emit StatsD metric for checkpoint
            if self.statsd_client:
                self.statsd_client.incr("checkpoint")
            return Ok(None)
        except sqlite3.Error as e:
            self.logger.error(f"Failed to perform WAL checkpoint: {e}")
            return Err(QueueError(f"WAL checkpoint failed: {e}"))

    def _increment_operation_count(self, conn: sqlite3.Connection) -> None:
        """
        Increments the operation count and triggers VACUUM if threshold is reached.

        Args:
            conn (sqlite3.Connection): The SQLite connection.
        """
        self._operation_count += 1
        if self._operation_count >= self._vacuum_threshold:
            try:
                self.vacuum_database(conn)
                self.perform_checkpoint(conn)
                self._operation_count = 0
            except QueueError as e:
                self.logger.error(f"Failed to perform maintenance operations: {e}")

    def get_operation_count(self) -> int:
        """
        Retrieves the current operation count.

        Returns:
            int: The number of operations performed since the last VACUUM.
        """
        return self._operation_count

    def _emit_queue_size(self, conn: sqlite3.Connection) -> None:
        """
        Emits the current queue size as a StatsD gauge.

        Args:
            conn (sqlite3.Connection): The SQLite connection.
        """
        if not self.statsd_client:
            return

        try:
            current_time = datetime.datetime.utcnow()
            cursor = conn.execute(
                f"""
                SELECT COUNT(*) FROM {self.table_name}
                WHERE status = 'pending' AND visible_at <= ?;
            """,
                (current_time,),
            )
            count = cursor.fetchone()[0]
            self.statsd_client.gauge("queue_size", count)
            self.logger.debug(f"Emitted queue_size gauge: {count}")
        except sqlite3.Error as e:
            self.logger.error(f"Failed to emit queue size metric: {e}")
            # Do not raise exception to avoid interfering with queue operations
