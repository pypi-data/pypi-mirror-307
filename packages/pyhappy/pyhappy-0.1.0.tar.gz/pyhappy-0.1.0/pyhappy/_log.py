#
#
# class EventLogger(BaseLogger):
#     """Event-based logger that handles specific event types."""
#
#     def __init__(self, config: EventLoggingConfig):
#         super().__init__(config)
#         self.config: EventLoggingConfig = config
#         self._event_handlers = {}
#         self._event_queue = Queue()
#         self._setup_event_dispatch()
#
#     def register_handler(self, event_type: str, handler: Callable):
#         """Register a handler for a specific event type."""
#         self._event_handlers[event_type] = handler
#
#     def _setup_event_dispatch(self):
#         """Setup event dispatch mechanism."""
#         if self.config.async_dispatch:
#             self._thread_pool.submit(self._event_dispatcher)
#
#     def _event_dispatcher(self):
#         """Background task to dispatch events."""
#         while True:
#             events = []
#             with contextlib.suppress(Empty):
#                 # Collect batch of events
#                 while len(events) < self.config.batch_size:
#                     event = self._event_queue.get(timeout=self.config.flush_interval)
#                     events.append(event)
#
#             # Process collected events
#             if events:
#                 self._process_events(events)
#
#     def _process_events(self, events: List[dict]):
#         """Process a batch of events."""
#         for event in events:
#             event_type = event.get('type')
#             handler = self._event_handlers.get(event_type)
#             if handler:
#                 try:
#                     handler(event)
#                 except Exception as e:
#                     self.log(f"Error processing event {event_type}: {str(e)}", LogLevel.ERROR)
#
#     def log(self, message: str, level: Union[str, LogLevel] = LogLevel.INFO, **kwargs):
#         """Log an event with the specified level and metadata."""
#         event = {
#             'type': kwargs.get('event_type', 'generic'),
#             'timestamp': datetime.now().isoformat(),
#             'level': level.value if isinstance(level, LogLevel) else level,
#             'message': message,
#             'metadata': kwargs
#         }
#         self._event_queue.put(event)
#
#
# class QueueLogger(BaseLogger):
#     # FIXIT running in loop
#     """Queue-based logger for high-throughput logging."""
#
#     def __init__(self, config: QueueLoggingConfig):
#         super().__init__(config)
#         self.config: QueueLoggingConfig = config
#         self._log_queue = Queue(maxsize=self.config.queue_size)
#         self._start_workers()
#
#     def _start_workers(self):
#         """Start worker threads to process the queue."""
#         for _ in range(self.config.workers):
#             self._thread_pool.submit(self._queue_worker)
#
#     def _queue_worker(self):
#         """Worker process to handle queued log messages."""
#         batch = []
#         last_flush = datetime.now()
#
#         while True:
#             with contextlib.suppress(Empty):
#                 while len(batch) < self.config.batch_size:
#                     message = self._log_queue.get(timeout=self.config.flush_interval)
#                     batch.append(message)
#
#             # Check if we should flush based on time or batch size
#             if batch and (len(batch) >= self.config.batch_size or
#                           (datetime.now() - last_flush).total_seconds() >= self.config.flush_interval):
#                 self._flush_batch(batch)
#                 batch = []
#                 last_flush = datetime.now()
#
#     def _flush_batch(self, batch: List[dict]):
#         """Flush a batch of log messages."""
#         for msg in batch:
#             super().log(**msg)
#
#     def log(self, message: str, level: Union[str, LogLevel] = LogLevel.INFO, **kwargs):
#         """Queue a log message for processing."""
#         self._log_queue.put({
#             'message': message,
#             'level': level,
#             **kwargs
#         })
#
#
# class BufferLogger(BaseLogger, Generic[T]):
#     """Logger that uses a circular buffer for message storage."""
#
#     def __init__(self, config: BufferLoggingConfig):
#         super().__init__(config)
#         self.config: BufferLoggingConfig = config
#         self._buffer = BufferProtocol[dict](config.buffer_config)
#         self._start_buffer_processor()
#
#     def _start_buffer_processor(self):
#         """Start the background buffer processor."""
#         self._thread_pool.submit(self._buffer_processor)
#
#     def _buffer_processor(self):
#         """Background task to process buffered messages."""
#         while True:
#             time.sleep(self.config.flush_interval)
#             self._flush_buffer()
#
#     def _flush_buffer(self):
#         """Flush messages from the buffer."""
#         retry_count = 0
#         while retry_count < self.config.max_retries:
#             try:
#                 with self._buffer.transaction():
#                     while not self._buffer.is_empty:
#                         msg = self._buffer.pop()
#                         super().log(**msg)
#                 break
#             except Exception as e:
#                 retry_count += 1
#                 if retry_count >= self.config.max_retries:
#                     self.log(f"Failed to flush buffer after {retry_count} attempts: {str(e)}",
#                              LogLevel.ERROR)
#
#     def log(self, message: str, level: Union[str, LogLevel] = LogLevel.INFO, **kwargs):
#         """Add a message to the buffer."""
#         try:
#             with self._buffer.transaction():
#                 self._buffer.push({
#                     'message': message,
#                     'level': level,
#                     'timestamp': datetime.now().isoformat(),
#                     **kwargs
#                 })
#         except Exception as e:
#             # Fallback to direct logging if buffer fails
#             super().log(f"Buffer operation failed: {str(e)}", LogLevel.ERROR)
#             super().log(message, level, **kwargs)
