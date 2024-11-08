import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta, datetime
from logging import Logger
from time import sleep
from typing import List, Optional, Type, TypeVar

from kafka.coordinator.assignors.abstract import AbstractPartitionAssignor

from buz.event import Event, Subscriber
from buz.event.consumer import Consumer
from buz.event.domain.queue.queue_repository import QueueRepository
from buz.event.infrastructure.buz_kafka.consume_strategy.consume_strategy import KafkaConsumeStrategy
from buz.event.infrastructure.buz_kafka.consume_strategy.kafka_on_fail_strategy import KafkaOnFailStrategy
from buz.event.middleware.consume_middleware import ConsumeMiddleware
from buz.event.middleware.consume_middleware_chain_resolver import ConsumeMiddlewareChainResolver
from buz.event.strategies.retry.consume_retrier import ConsumeRetrier
from buz.event.strategies.retry.reject_callback import RejectCallback
from buz.kafka import (
    KafkaConnectionConfig,
    KafkaConsumerRecord,
    ConsumerInitialOffsetPosition,
)
from buz.kafka.infrastructure.deserializers.bytes_to_message_deserializer import BytesToMessageDeserializer
from buz.kafka.infrastructure.deserializers.implementations.json_bytes_to_message_deserializer import (
    JSONBytesToMessageDeserializer,
)
from buz.kafka.infrastructure.kafka_python.factories.kafka_python_multi_threaded_consumer_factory import (
    KafkaPythonMultiThreadedConsumerFactory,
)
from buz.kafka.infrastructure.kafka_python.kafka_poll_record import KafkaPollRecord
from buz.kafka.infrastructure.kafka_python.kafka_python_multi_threaded_consumer import KafkaPythonMultiThreadedConsumer

T = TypeVar("T", bound=Event)
KafkaConsumer = KafkaPythonMultiThreadedConsumer  # TODO: remove this alias once we comply with the interface


class BuzKafkaMultiThreadedConsumer(Consumer):
    def __init__(
        self,
        *,
        connection_config: KafkaConnectionConfig,
        consume_strategy: KafkaConsumeStrategy,
        on_fail_strategy: KafkaOnFailStrategy,
        queue_repository: QueueRepository[tuple[KafkaConsumer, KafkaPollRecord]],
        kafka_partition_assignors: tuple[Type[AbstractPartitionAssignor], ...] = (),
        subscribers: list[Subscriber],
        logger: Logger,
        consumer_initial_offset_position: ConsumerInitialOffsetPosition,
        deserializers_per_subscriber: dict[Subscriber, BytesToMessageDeserializer[T]],
        consume_middlewares: Optional[List[ConsumeMiddleware]] = None,
        consume_retrier: Optional[ConsumeRetrier] = None,
        reject_callback: Optional[RejectCallback] = None,
        max_queue_size: int,
        max_records_retrieved_per_poll: int,
        min_time_between_polls_in_ms: int,
    ):
        self.__connection_config = connection_config
        self.__consume_strategy = consume_strategy
        self.__on_fail_strategy = on_fail_strategy
        self.__queue_repository = queue_repository
        self.__kafka_partition_assignors = kafka_partition_assignors
        self.__subscribers = subscribers
        self.__logger = logger
        self.__consumer_initial_offset_position = consumer_initial_offset_position
        self.__deserializers_per_subscriber = deserializers_per_subscriber
        self.__consume_middleware_chain_resolver = ConsumeMiddlewareChainResolver(consume_middlewares or [])
        self.__consume_retrier = consume_retrier
        self.__reject_callback = reject_callback
        self.__max_queue_size = max_queue_size
        self.__max_records_retrieved_per_poll = max_records_retrieved_per_poll
        self.__min_time_between_polls = timedelta(milliseconds=min_time_between_polls_in_ms)

        self.__subscriber_per_consumer_mapper: dict[KafkaConsumer, Subscriber] = {}
        self.__polling_threads_pool: ThreadPoolExecutor = ThreadPoolExecutor()
        self.__kafka_consumers_with_poll_requested: set[KafkaConsumer] = set()
        self.__should_stop = threading.Event()

    def run(self) -> None:
        self.__start_all_kafka_consumers_concurrently()

        for kafka_consumer, subscriber in self.__subscriber_per_consumer_mapper.items():
            self.__request_more_records_asynchronously(kafka_consumer=kafka_consumer, last_time_polled=datetime.now())

        self.__consume_kafka_poll_records_from_queue()

    def __start_all_kafka_consumers_concurrently(self):
        startup_threads_pool = ThreadPoolExecutor()
        for subscriber in self.__subscribers:
            startup_threads_pool.submit(self.__create_kafka_consumer_for_subscriber, subscriber)

        startup_threads_pool.shutdown()

    def __create_kafka_consumer_for_subscriber(self, subscriber: Subscriber) -> None:
        byte_deserializer = self.__deserializers_per_subscriber.get(subscriber)
        kafka_python_consumer_factory = KafkaPythonMultiThreadedConsumerFactory(
            consumer_group=self.__consume_strategy.get_subscription_group(subscriber),
            topics=self.__consume_strategy.get_topics(subscriber),
            kafka_connection_config=self.__connection_config,
            initial_offset_position=self.__consumer_initial_offset_position,
            byte_deserializer=byte_deserializer or JSONBytesToMessageDeserializer(event_class=subscriber.handles()),  # type: ignore[arg-type]
            kafka_partition_assignors=self.__kafka_partition_assignors,
            logger=self.__logger,
        )
        kafka_consumer = kafka_python_consumer_factory.build()
        self.__subscriber_per_consumer_mapper[kafka_consumer] = subscriber

    def __poll_kafka_consumer(self, kafka_consumer: KafkaConsumer, last_time_polled: datetime) -> None:
        self.__kafka_consumers_with_poll_requested.remove(kafka_consumer)

        if self.__consumer_has_already_stopped():
            return

        queue_size = self.__queue_repository.get_size()
        available_space_in_queue = self.__max_queue_size - queue_size

        if self.__should_poll_for_more_records(available_space_in_queue, last_time_polled):
            last_time_polled = datetime.now()
            for kafka_poll_record in kafka_consumer.poll(
                timeout_ms=0,
                number_of_messages_to_poll=min(self.__max_records_retrieved_per_poll, available_space_in_queue),
            ):
                self.__queue_repository.push((kafka_consumer, kafka_poll_record))

        self.__request_more_records_asynchronously(kafka_consumer=kafka_consumer, last_time_polled=last_time_polled)

    def __should_poll_for_more_records(self, available_space_in_queue: int, last_time_polled: datetime) -> bool:
        if available_space_in_queue <= 0:
            return False

        if datetime.now() - last_time_polled < self.__min_time_between_polls:
            return False

        return True

    def __request_more_records_asynchronously(self, kafka_consumer: KafkaConsumer, last_time_polled: datetime) -> None:
        if kafka_consumer in self.__kafka_consumers_with_poll_requested:
            return

        self.__kafka_consumers_with_poll_requested.add(kafka_consumer)
        self.__polling_threads_pool.submit(self.__poll_kafka_consumer, kafka_consumer, last_time_polled)

    def __consume_kafka_poll_records_from_queue(self) -> None:
        while not self.__consumer_has_already_stopped():
            if self.__queue_repository.is_empty():
                sleep(0.1)
                continue

            consumer, kafka_poll_record = self.__queue_repository.pop()
            subscriber = self.__subscriber_per_consumer_mapper[consumer]
            consumer.consume(
                kafka_poll_record=kafka_poll_record,
                consumption_callback=lambda kafka_record: self.__consumption_callback(subscriber, kafka_record),
            )

    def __consumption_callback(self, subscriber: Subscriber, message: KafkaConsumerRecord[T]) -> None:
        self.__consume_middleware_chain_resolver.resolve(
            event=message.value, subscriber=subscriber, consume=self.__perform_consume
        )

    def stop(self) -> None:
        if self.__consumer_has_already_stopped():
            return

        self.__should_stop.set()
        self.__logger.info("Waiting until all polling tasks finish...")
        self.__polling_threads_pool.shutdown()
        self.__logger.info("All polling tasks finished. Stopping kafka consumers...")
        for kafka_consumer in self.__subscriber_per_consumer_mapper.keys():
            kafka_consumer.stop()
        self.__logger.info("All kafka consumers stopped")

    def __consumer_has_already_stopped(self) -> bool:
        return self.__should_stop.is_set()

    def __perform_consume(self, event: T, subscriber: Subscriber) -> None:
        should_retry = True
        while should_retry is True:
            try:
                return subscriber.consume(event)
            except Exception as exc:
                self.__logger.warning(f"Event {event.id} could not be consumed by the subscriber {subscriber.fqn}")

                if self.__should_retry(event, subscriber) is True:
                    self.__register_retry(event, subscriber)
                    continue
                else:
                    if self.__reject_callback:
                        self.__reject_callback.on_reject(event=event, subscribers=[subscriber])

                    if self.__on_fail_strategy == KafkaOnFailStrategy.STOP_ON_FAIL:
                        raise exc

    def __should_retry(self, event: Event, subscriber: Subscriber) -> bool:
        if self.__consume_retrier is None:
            return False

        return self.__consume_retrier.should_retry(event, [subscriber])

    def __register_retry(self, event: Event, subscriber: Subscriber) -> None:
        if self.__consume_retrier is None:
            return None

        return self.__consume_retrier.register_retry(event, [subscriber])
