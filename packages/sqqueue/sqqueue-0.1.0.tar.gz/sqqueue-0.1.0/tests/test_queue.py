# tests/test_sqqueue.py

import datetime
import os
import sqlite3
import tempfile
import time

import pytest

from sqqueue import Err, Ok, SQLiteQueue
from sqqueue.exceptions import (
    CompletionError,
    DequeueError,
    EnqueueError,
    QueueError,
    RequeueError,
)
from sqqueue.result import Result


@pytest.fixture
def temp_db():
    """
    Fixture to create a temporary database for testing.
    """
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)  # Close the file descriptor
    yield db_path
    os.remove(db_path)


@pytest.fixture
def queue(temp_db):
    """
    Fixture to initialize the SQLiteQueue with the temporary database.
    """
    return SQLiteQueue(
        db_path=temp_db,
        table_name="test_message_queue",
        vacuum_threshold=10,  # Lower threshold for testing
        vacuum_on_start=True,  # Ensure vacuum runs on start
        statsd_host=None,  # Disable StatsD for testing
        statsd_port=None,
        default_max_attempts=3,
    )


def test_enqueue(queue):
    """
    Test that messages can be enqueued successfully.
    """
    result: Result[int, EnqueueError] = queue.enqueue("Test Task 1")
    assert result.is_ok(), f"Enqueue failed: {result.error}"
    assert isinstance(result.value, int), "Enqueued message ID should be an integer."

    # Verify the message exists in the database
    with queue._get_connection() as conn:
        cursor = conn.execute(
            f"""
            SELECT payload, status FROM {queue.table_name} WHERE id = ?;
        """,
            (result.value,),
        )
        row = cursor.fetchone()
        assert row is not None, "Enqueued message not found in the database."
        assert row[0] == "Test Task 1", "Payload does not match."
        assert row[1] == "pending", "Initial status should be 'pending'."


def test_dequeue(queue):
    """
    Test that messages can be dequeued and marked as 'processing'.
    """
    # Enqueue a message
    enqueue_result = queue.enqueue("Test Task 2")
    assert enqueue_result.is_ok(), f"Enqueue failed: {enqueue_result.error}"
    msg_id = enqueue_result.value

    # Dequeue the message
    dequeue_result: Result[tuple, DequeueError] = queue.dequeue()
    assert dequeue_result.is_ok(), f"Dequeue failed: {dequeue_result.error}"
    message = dequeue_result.value
    assert message is not None, "No message dequeued."
    dequeued_id, payload = message
    assert dequeued_id == msg_id, "Dequeued message ID does not match."
    assert payload == "Test Task 2", "Dequeued payload does not match."

    # Verify the message status is 'processing'
    with queue._get_connection() as conn:
        cursor = conn.execute(
            f"""
            SELECT status FROM {queue.table_name} WHERE id = ?;
        """,
            (msg_id,),
        )
        row = cursor.fetchone()
        assert row is not None, "Dequeued message not found in the database."
        assert row[0] == "processing", "Message status should be 'processing'."


def test_complete_message(queue):
    """
    Test that a dequeued message can be marked as complete.
    """
    # Enqueue and dequeue a message
    enqueue_result = queue.enqueue("Test Task 3")
    assert enqueue_result.is_ok(), f"Enqueue failed: {enqueue_result.error}"
    msg_id = enqueue_result.value

    dequeue_result = queue.dequeue()
    assert dequeue_result.is_ok(), f"Dequeue failed: {dequeue_result.error}"
    message = dequeue_result.value
    assert message is not None, "No message dequeued."
    dequeued_id, _ = message
    assert dequeued_id == msg_id, "Dequeued message ID does not match."

    # Complete the message
    complete_result: Result[None, CompletionError] = queue.complete(msg_id)
    assert complete_result.is_ok(), f"Completion failed: {complete_result.error}"

    # Verify the message is removed from the queue
    with queue._get_connection() as conn:
        cursor = conn.execute(
            f"""
            SELECT * FROM {queue.table_name} WHERE id = ?;
        """,
            (msg_id,),
        )
        row = cursor.fetchone()
        assert row is None, "Completed message should be removed from the queue."


def test_fail_message_and_move_to_dlq(queue):
    """
    Test that failing a message moves it to the dead-letter queue after max attempts.
    """
    # Enqueue a message
    enqueue_result = queue.enqueue("Test Task 4")
    assert enqueue_result.is_ok(), f"Enqueue failed: {enqueue_result.error}"
    msg_id = enqueue_result.value

    # Dequeue and fail the message 3 times
    for attempt in range(queue.default_max_attempts):
        dequeue_result = queue.dequeue()
        assert (
            dequeue_result.is_ok()
        ), f"Dequeue failed on attempt {attempt + 1}: {dequeue_result.error}"
        message = dequeue_result.value
        assert message is not None, "No message dequeued."
        dequeued_id, _ = message
        assert dequeued_id == msg_id, "Dequeued message ID does not match."
        # Fail the message
        fail_result = queue.fail_message(msg_id, send_to_dlq=False)
        assert (
            fail_result.is_ok()
        ), f"Fail message failed on attempt {attempt + 1}: {fail_result.error}"

    queue.dequeue()  # have to get one more time to trigger movement to DLQ

    # Verify the message is in the dead-letter queue
    dead_letters_result = queue.get_dead_letters()
    assert (
        dead_letters_result.is_ok()
    ), f"Retrieving dead letters failed: {dead_letters_result.error}"
    dead_letters = dead_letters_result.value
    assert any(
        dlq["id"] == msg_id for dlq in dead_letters
    ), "Failed message not found in DLQ."


def test_recover_processing_messages(queue):
    """
    Test that the recovery method correctly recovers messages stuck in 'processing'.
    """
    # Enqueue and dequeue a message
    enqueue_result = queue.enqueue("Test Task 5")
    assert enqueue_result.is_ok(), f"Enqueue failed: {enqueue_result.error}"
    msg_id = enqueue_result.value

    dequeue_result = queue.dequeue()
    assert dequeue_result.is_ok(), f"Dequeue failed: {dequeue_result.error}"
    message = dequeue_result.value
    assert message is not None, "No message dequeued."

    # Simulate expiration of visibility timeout by setting processing_at to past
    past_time = datetime.datetime.utcnow() - datetime.timedelta(
        seconds=queue.default_visibility_timeout + 10
    )
    with queue._get_connection() as conn:
        conn.execute(
            f"""
            UPDATE {queue.table_name}
            SET processing_at = ?
            WHERE id = ?;
        """,
            (past_time, msg_id),
        )
        conn.commit()

    # Trigger recovery
    recovery_result: Result[int, QueueError] = queue.recover_processing_messages()
    assert recovery_result.is_ok(), f"Recovery failed: {recovery_result.error}"
    recovered_count = recovery_result.value
    assert recovered_count == 1, "Recovery count should be 1."

    # Verify the message status is back to 'pending'
    with queue._get_connection() as conn:
        cursor = conn.execute(
            f"""
            SELECT status, processing_at FROM {queue.table_name} WHERE id = ?;
        """,
            (msg_id,),
        )
        row = cursor.fetchone()
        assert row is not None, "Recovered message not found."
        assert row[0] == "pending", "Recovered message status should be 'pending'."
        assert row[1] is None, "Processing_at should be NULL after recovery."


def test_dead_letter_reprocessing(queue):
    """
    Test retrieving dead-letter messages and reprocessing them back to the main queue.
    """
    # Enqueue a message that will fail
    enqueue_result = queue.enqueue("Test Task 6")
    assert enqueue_result.is_ok(), f"Enqueue failed: {enqueue_result.error}"
    msg_id = enqueue_result.value

    # Dequeue and fail the message 3 times to move it to DLQ
    for _ in range(queue.default_max_attempts):
        dequeue_result = queue.dequeue()
        assert dequeue_result.is_ok(), f"Dequeue failed: {dequeue_result.error}"
        message = dequeue_result.value
        assert message is not None, "No message dequeued."
        queue.fail_message(msg_id, send_to_dlq=False)

    queue.dequeue()  ### force to dlq

    # Ensure moves to dead letter queue
    dead_letters = queue.get_dead_letters()
    assert dead_letters.is_ok(), f"Get Dead Letters Failed: {dead_letters.error}"
    dead_letters_result = dead_letters.value
    assert len(dead_letters_result) == 1
    assert dead_letters_result[0]["id"] is msg_id

    # bring back the task for further testing
    queue.reprocess_dead_letter(msg_id)
    time.sleep(1)

    # reque with new id
    msg_id, _ = queue.dequeue().value

    # Fail the message without sending to DLQ
    fail_result = queue.fail_message(msg_id, send_to_dlq=False)
    assert fail_result.is_ok(), f"Fail message failed: {fail_result.error}"

    # Now, requeue it to DLQ
    # Since send_to_dlq was False, the message should be in 'pending' again, let's dequeue and fail with send_to_dlq=True
    dequeue_result = queue.dequeue()
    assert dequeue_result.is_ok(), f"Dequeue failed: {dequeue_result.error}"
    message = dequeue_result.value
    assert message is not None, "No message dequeued."

    # Fail and send to DLQ
    fail_result = queue.fail_message(msg_id, send_to_dlq=True)
    assert fail_result.is_ok(), f"Fail message failed: {fail_result.error}"

    # Retrieve dead-letter messages
    dead_letters_result = queue.get_dead_letters()
    assert (
        dead_letters_result.is_ok()
    ), f"Retrieving dead letters failed: {dead_letters_result.error}"
    dead_letters = dead_letters_result.value
    assert any(
        dlq["id"] == msg_id for dlq in dead_letters
    ), "Failed message not found in DLQ."

    # Reprocess the message from DLQ
    reprocess_result: Result[None, RequeueError] = queue.reprocess_dead_letter(msg_id)
    assert (
        reprocess_result.is_ok()
    ), f"Reprocessing DLQ message failed: {reprocess_result.error}"

    msg_id += 1  # increments message id

    # Verify the message is back in the main queue as 'pending'
    with queue._get_connection() as conn:
        cursor = conn.execute(
            f"""
            SELECT status FROM {queue.table_name} WHERE id = ?;
        """,
            (msg_id,),
        )
        row = cursor.fetchone()
        assert row is not None, "Reprocessed message not found in the main queue."
        assert row[0] == "pending", "Reprocessed message status should be 'pending'."

    # Verify the message is removed from DLQ
    dead_letters_result = queue.get_dead_letters()
    assert (
        dead_letters_result.is_ok()
    ), f"Retrieving dead letters failed: {dead_letters_result.error}"
    dead_letters = dead_letters_result.value
    assert not any(
        dlq["id"] == msg_id for dlq in dead_letters
    ), "Reprocessed message should be removed from DLQ."


def test_batch_enqueue_dequeue(queue):
    """
    Test batch enqueueing and dequeueing of messages.
    """
    # Prepare batch payloads
    payloads = [
        ("Batch Task 1", 1, 0, None),
        ("Batch Task 2", 2, 5, None),
        ("Batch Task 3", 1, 10, None),
    ]

    # Enqueue batch
    enqueue_batch_result: Result[list, EnqueueError] = queue.enqueue_batch(payloads)
    assert (
        enqueue_batch_result.is_ok()
    ), f"Batch enqueue failed: {enqueue_batch_result.error}"
    message_ids = enqueue_batch_result.value
    assert len(message_ids) == 3, "Should enqueue 3 messages."

    time.sleep(5)

    # Dequeue batch
    dequeue_batch_result: Result[list, DequeueError] = queue.dequeue_batch(batch_size=2)
    assert (
        dequeue_batch_result.is_ok()
    ), f"Batch dequeue failed: {dequeue_batch_result.error}"
    messages = dequeue_batch_result.value
    assert len(messages) == 2, "Should dequeue 2 messages."

    # Verify messages are marked as 'processing'
    for msg_id, payload in messages:
        with queue._get_connection() as conn:
            cursor = conn.execute(
                f"""
                SELECT status FROM {queue.table_name} WHERE id = ?;
            """,
                (msg_id,),
            )
            row = cursor.fetchone()
            assert row is not None, "Dequeued message not found."
            assert (
                row[0] == "processing"
            ), "Dequeued message status should be 'processing'."


def test_peek(queue):
    """
    Test the peek operation to view the next pending message without dequeuing it.
    """
    # Enqueue a message
    enqueue_result = queue.enqueue("Peek Task")
    assert enqueue_result.is_ok(), f"Enqueue failed: {enqueue_result.error}"
    msg_id = enqueue_result.value

    # Peek the message
    peek_result: Result[tuple, QueueError] = queue.peek()
    assert peek_result.is_ok(), f"Peek failed: {peek_result.error}"
    message = peek_result.value
    assert message is not None, "No message peeked."
    peeked_id, payload = message
    assert peeked_id == msg_id, "Peeked message ID does not match."
    assert payload == "Peek Task", "Peeked payload does not match."

    # Verify the message is still 'pending'
    with queue._get_connection() as conn:
        cursor = conn.execute(
            f"""
            SELECT status FROM {queue.table_name} WHERE id = ?;
        """,
            (msg_id,),
        )
        row = cursor.fetchone()
        assert row is not None, "Peeked message not found."
        assert row[0] == "pending", "Peeked message status should remain 'pending'."


def test_is_empty(queue):
    """
    Test the is_empty method to check if the queue has pending messages.
    """
    # Initially, the queue should be empty
    is_empty_result = queue.is_empty()
    assert is_empty_result.is_ok(), f"is_empty check failed: {is_empty_result.error}"
    assert is_empty_result.value is True, "Queue should be empty initially."

    # Enqueue a message
    enqueue_result = queue.enqueue("IsEmpty Task")
    assert enqueue_result.is_ok(), f"Enqueue failed: {enqueue_result.error}"

    # Now, the queue should not be empty
    is_empty_result = queue.is_empty()
    assert is_empty_result.is_ok(), f"is_empty check failed: {is_empty_result.error}"
    assert is_empty_result.value is False, "Queue should not be empty after enqueue."

    # Dequeue the message
    dequeue_result = queue.dequeue()
    assert dequeue_result.is_ok(), f"Dequeue failed: {dequeue_result.error}"
    message = dequeue_result.value
    assert message is not None, "No message dequeued."

    # Now, the queue should be empty again
    is_empty_result = queue.is_empty()
    assert is_empty_result.is_ok(), f"is_empty check failed: {is_empty_result.error}"
    assert is_empty_result.value is True, "Queue should be empty after dequeuing."


def test_vacuum_and_checkpoint(queue):
    """
    Test that VACUUM and WAL checkpoint operations can be performed successfully.
    """
    # Perform VACUUM
    with queue._get_connection() as conn:
        vacuum_result = queue.vacuum_database(conn)
        assert vacuum_result.is_ok(), f"VACUUM failed: {vacuum_result.error}"
        # Perform WAL checkpoint
        checkpoint_result = queue.perform_checkpoint(conn)
        assert (
            checkpoint_result.is_ok()
        ), f"WAL checkpoint failed: {checkpoint_result.error}"


def test_operation_count_and_maintenance(queue, temp_db):
    """
    Test that the operation count increments and maintenance operations are triggered.
    """
    # Initial operation count
    initial_count = queue.get_operation_count()
    assert initial_count == 0, "Initial operation count should be 0."

    # Perform operations to reach the vacuum threshold
    for i in range(queue._vacuum_threshold):
        enqueue_result = queue.enqueue(f"Maintenance Task {i}")
        assert (
            enqueue_result.is_ok()
        ), f"Enqueue failed at operation {i}: {enqueue_result.error}"

    # After threshold, operation count should reset
    assert (
        queue.get_operation_count() == 0
    ), "Operation count should reset after reaching vacuum threshold."

    # Check that VACUUM was performed by checking the database integrity
    # SQLite doesn't provide direct feedback, so we can perform a simple query
    with queue._get_connection() as conn:
        try:
            conn: sqlite3.Connection
            result = conn.execute("PRAGMA integrity_check;").fetchone()
            assert (
                result[0] == "ok"
            ), "Database integrity check failed after maintenance."
        except sqlite3.Error as e:
            pytest.fail(f"Database integrity check raised an error: {e}")
