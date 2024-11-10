# sqqueue/exceptions.py


class QueueError(Exception):
    """Base exception class for sqqueue."""

    pass


class EnqueueError(QueueError):
    """Exception raised when enqueue operation fails."""

    pass


class DequeueError(QueueError):
    """Exception raised when dequeue operation fails."""

    pass


class CompletionError(QueueError):
    """Exception raised when completing a message fails."""

    pass


class RequeueError(QueueError):
    """Exception raised when requeueing a message fails."""

    pass
