import asyncio
import logging

logger = logging.getLogger(__name__)


def handle_task_errors(task: asyncio.Task) -> None:
    """
    Handle and log any errors from an asyncio task.
    This function is used to handle and log any errors from an asyncio task.
    It is used to handle the errors from the asyncio task in the consumer context.
    """
    try:
        task_exception = task.exception()
    except (asyncio.InvalidStateError, asyncio.CancelledError):
        logger.error(
            "This is not supposed to happen as we should always use this functions on task that we know are done."
        )
        raise
    match task_exception:
        case None:
            return
        case TimeoutError():
            # A TimeoutError occurred when a task took too long to complete related to the timeout configuration.
            # This is logged as a warning to indicate that the task exceeded the allowed time.
            # TODO: maybe handle it another way.
            logger.warning(f"Task timed out: {task_exception}")
        case asyncio.CancelledError():
            # An asyncio.CancelledError occurred when a task was cancelled.
            # This is logged as a warning to indicate that the task was intentionally stopped.
            # TODO: maybe the interrupt error should cancel the currently treated tasks. Same thing for the stop event.
            logger.warning(f"Task cancelled: {task_exception}")
        case _:
            # Any other exception occurred, which is re-raised to propagate the error.
            # This ensures that unexpected errors are not silently ignored.
            logger.exception("Unexpected error:")
            raise task_exception
