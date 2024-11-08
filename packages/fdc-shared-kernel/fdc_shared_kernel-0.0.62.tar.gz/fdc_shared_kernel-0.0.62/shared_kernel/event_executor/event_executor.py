import threading
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any, Callable, Dict, Optional

from shared_kernel.config import Config
from shared_kernel.interfaces import DataBus
from shared_kernel.logger import Logger
from shared_kernel.messaging.utils.event_messages import AWSEventMessage, EventMessage
from shared_kernel.status_tracker import StatusTracker
from shared_kernel.enums import TaskStatus

app_config = Config()
logger = Logger(app_config.get("APP_NAME"))


class EventExecutor:
    def __init__(
        self, databus: DataBus, status_tracker: StatusTracker
    ):
        """
        Initialize the event executor.

        Args:
            databus: databus - AWS Databus (SQS and Events) / NATS / HTTP
            status_tracker: Status tracker to track status of events task and jobs
        """
        self.databus = databus
        self.status_tracker = status_tracker
        # listener threads for each events
        self._threads: Dict[str, threading.Thread] = {}
        # concurrent executors for each event
        self._executors: Dict[str, ThreadPoolExecutor] = {}
        self._shutdown_event = threading.Event()
        self._active_futures: Dict[str, set[Future]] = {}
        logger.info("EventExecutor initialized.")

    def _process_message(
        self,
        event_msg: EventMessage,
        callback: Callable[[dict, Optional[dict]], None],
    ) -> bool:
        """
        Process a single message with error handling

        Args:
            event_msg: Parsed event message
            callback: Handler function to process the message

        Returns:
            bool: True if processing succeeded, False otherwise
        """
        try:
            # set the start time of the event exceution in the event meta
            event_msg.event_meta.start_event()

            logger.info(
                f"Processing event {event_msg.event_name}. trace-id: {event_msg.event_meta.trace_id}. span-id: {event_msg.event_meta.trace_id}."
            )
            task: dict = self.status_tracker.get_task(
                task=event_msg.event_name, task_id=event_msg.event_meta.job_id
            )

            if task is None:
                logger.info(
                    f"Creating new task for event {event_msg.event_name}. trace-id: {event_msg.event_meta.trace_id}. span-id: {event_msg.event_meta.trace_id}."
                )
                self.status_tracker.create_task(
                    trace_id=event_msg.event_meta.trace_id,
                    span_id=event_msg.event_meta.span_id,
                    task=event_msg.event_name,
                    status=TaskStatus.PROCESSING.value,
                    task_id=event_msg.event_meta.job_id,
                )

                callback(event_msg.raw_message, None)

            elif task["status"] == TaskStatus.PROCESSING.value:
                logger.info(
                    f"Task {event_msg.event_name} is already processing. trace-id: {event_msg.event_meta.trace_id}. span-id: {event_msg.event_meta.trace_id}."
                )
                callback(event_msg.raw_message, task.get("tracking_payload"))

            return True

        except Exception as e:
            logger.error(
                f"Error processing event {event_msg.event_name} trace-id: {event_msg.event_meta.trace_id}. span-id: {event_msg.event_meta.trace_id} : {str(e)}"
            )
            # adding the failure reason to the event meta
            event_msg.event_meta.failure_reason = str(e)

            self.status_tracker.mark_task_as_failure(
                span_id=event_msg.event_meta.span_id,
                trace_id=event_msg.event_meta.trace_id,
                task=event_msg.event_name,
                failure_reason=str(e),
                task_id=event_msg.event_meta.job_id,
            )

            # NOTE: for dead letter queue we are simply publishing the
            # failed event to the databus as a DLQ event.
            dlq_message = {
                "event_name": event_msg.event_name,
                "event_payload": event_msg.event_payload,
                "event_meta": event_msg.event_meta.to_dict(),
            }

            self.databus.publish_event("DLQ", dlq_message)

            return False

        finally:
            # set the end time of the event exceution in the event meta
            event_msg.event_meta.end_event()

            logger.info(
                    f"Setting tracking payload for event {event_msg.event_name}. trace-id: {event_msg.event_meta.trace_id}. span-id: {event_msg.event_meta.trace_id}."
                )
            self.status_tracker.set_tracking_payload(
                    span_id=event_msg.event_meta.span_id,
                    trace_id=event_msg.event_meta.trace_id,
                    task=event_msg.event_name,
                    tracking_payload=event_msg.to_json(),
                    task_id=event_msg.event_meta.job_id,
                )

    def _callback_wrapper(self, callback: Callable[[Any], None], message: dict) -> None:
        """
        Wrapper around message processing to handle cleanup and status updates.
        """
        success = False

        try:
            logger.info(f"Initiating callback for message: {message}")
            event_msg = AWSEventMessage(message)
            success = self._process_message(event_msg, callback)
        finally:
            if success:
                logger.info(
                    f"Event {event_msg.event_name} completed successfully. trace-id: {event_msg.event_meta.trace_id}. span-id: {event_msg.event_meta.trace_id}."
                )
                self.status_tracker.update_task(
                    span_id=event_msg.event_meta.span_id,
                    trace_id=event_msg.event_meta.trace_id,
                    task=event_msg.event_name,
                    status=TaskStatus.COMPLETED.value,
                    task_id=event_msg.event_meta.job_id,
                )
            else:
                logger.warning(
                    f"Event {event_msg.event_name} failed during processing. trace-id: {event_msg.event_meta.trace_id}. span-id: {event_msg.event_meta.trace_id}."
                )
            self.databus.delete_message(event_msg)

    def _listen_events(
        self,
        event_name: str,
        executor: ThreadPoolExecutor,
        callback: Callable[[Any], None],
    ) -> None:
        """
        Main event listening loop for a specific event type.
        """
        logger.info(f"Starting event listener for [{event_name}].")
        while not self._shutdown_event.is_set():
            try:
                message = self.databus.get_async_message(event_name)
                if message:
                    logger.info(f"Received message for event {event_name}: {message}")
                    future = executor.submit(self._callback_wrapper, callback, message)
                    future.add_done_callback(lambda f: self._active_futures[event_name].discard(f))
                    self._active_futures[event_name].add(future)
            except Exception as e:
                logger.error(f"Error in event listener for {event_name}: {str(e)}")
        logger.info(f"Event listener for {event_name} has been stopped.")

    def register_event(
        self,
        event_name: str,
        callback: Callable[[Any], None],
        max_concurrency: int,
    ) -> None:
        """
        Register an event handler with the specified concurrency limit.

        Args:
            event_name: Name of the event to handle
            callback: Function to call with the event payload
            max_concurrency: Maximum number of concurrent executions

        Raises:
            ValueError: If event is already registered
        """
        if event_name in self._threads:
            raise ValueError(f"Event {event_name} is already registered")

        logger.info(
            f"Registering event {event_name} with max concurrency of {max_concurrency}."
        )

        # the DataBus interface requires subscribe_async_event
        # to accept a callback parameter as part of its method signature.
        self.databus.subscribe_async_event(event_name, None)

        executor = ThreadPoolExecutor(
            max_workers=max_concurrency, thread_name_prefix=f"Executor-{event_name}"
        )
        self._executors[event_name] = executor

        # keeping track of active futures returned by
        # submitting a job to the threadpool executor
        self._active_futures[event_name] = set()

        thread = threading.Thread(
            target=self._listen_events,
            args=(event_name, executor, callback),
            name=f"EventListener-{event_name}",
            daemon=True,
        )
        self._threads[event_name] = thread
        thread.start()
        logger.info(f"Event {event_name} registered and listener thread started.")

    def shutdown(self) -> None:
        """
        Gracefully shut down all event listeners.
        """
        logger.info("Shutting down EventExecutor.")
        self._shutdown_event.set()

        # wait for threads to finish
        for event_name, thread in self._threads.items():
            thread.join()

        # wait for active tasks to complete
        for event_name, futures in self._active_futures.items():
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    logger.error(
                        f"Error during shutdown of {event_name} task: {str(e)}"
                    )

        # shutdown executors
        for event_name, executor in self._executors.items():
            executor.shutdown(
                wait=True,
            )

        self._threads.clear()
        self._executors.clear()
        self._active_futures.clear()
        logger.info("EventExecutor shutdown complete.")
