from __future__ import annotations

from logging import Logger
from typing import Callable, Optional, Type, Tuple, cast

from kafka import KafkaConsumer as KafkaPythonLibraryConsumer
from kafka.coordinator.assignors.abstract import AbstractPartitionAssignor

from buz.kafka.domain.models.consumer_initial_offset_position import ConsumerInitialOffsetPosition
from buz.kafka.domain.models.kafka_connection_config import KafkaConnectionConfig
from buz.kafka.domain.models.kafka_consumer_record import KafkaConsumerRecord
from buz.kafka.infrastructure.deserializers.byte_deserializer import ByteDeserializer
from buz.kafka.infrastructure.kafka_python.kafka_poll_record import KafkaPollRecord
from buz.kafka.infrastructure.kafka_python.translators.consumer_initial_offset_position_translator import (
    ConsumerInitialOffsetPositionTranslator,
)
from buz.kafka.infrastructure.serializers.kafka_header_serializer import KafkaHeaderSerializer


class KafkaPythonMultiThreadedConsumer:
    __DEFAULT_POLL_TIMEOUT_MS = 0
    __DEFAULT_SESSION_TIMEOUT_MS = 1000 * 10
    # https://docs.confluent.io/platform/current/installation/configuration/consumer-configs.html#session-timeout-ms

    def __init__(
        self,
        *,
        consumer_group: str,
        topics: list[str],
        connection_config: KafkaConnectionConfig,
        initial_offset_position: ConsumerInitialOffsetPosition,
        byte_deserializer: ByteDeserializer,
        header_serializer: KafkaHeaderSerializer,
        partition_assignors: Tuple[Type[AbstractPartitionAssignor], ...],
        logger: Logger,
        session_timeout_ms: int = __DEFAULT_SESSION_TIMEOUT_MS,
    ):
        self.__consumer_group = consumer_group
        self.__topics = topics
        self.__initial_offset_position = initial_offset_position
        self.__connection_config = connection_config
        self.__byte_deserializer = byte_deserializer
        self.__header_serializer = header_serializer
        self.__partition_assignors = partition_assignors
        self.__logger = logger
        self.__session_timeout_ms = session_timeout_ms

        self.__consumer = self.__generate_consumer()

    def __generate_consumer(self) -> KafkaPythonLibraryConsumer:
        sasl_mechanism: Optional[str] = None

        if self.__connection_config.credentials.sasl_mechanism is not None:
            sasl_mechanism = self.__connection_config.credentials.sasl_mechanism.value

        consumer = KafkaPythonLibraryConsumer(
            bootstrap_servers=self.__connection_config.bootstrap_servers,
            security_protocol=self.__connection_config.credentials.security_protocol.value,
            sasl_mechanism=sasl_mechanism,
            sasl_plain_username=self.__connection_config.credentials.user,
            sasl_plain_password=self.__connection_config.credentials.password,
            client_id=self.__connection_config.client_id,
            group_id=self.__consumer_group,
            enable_auto_commit=False,
            auto_offset_reset=ConsumerInitialOffsetPositionTranslator.to_kafka_supported_format(
                self.__initial_offset_position
            ),
            session_timeout_ms=self.__session_timeout_ms,
            partition_assignment_strategy=list(self.__partition_assignors),
        )

        consumer.subscribe(self.__topics)
        return consumer

    def poll(
        self,
        *,
        timeout_ms: int = __DEFAULT_POLL_TIMEOUT_MS,
        number_of_messages_to_poll: Optional[int] = None,
    ) -> list[KafkaPollRecord]:
        poll_results = self.__consumer.poll(
            timeout_ms=timeout_ms,
            max_records=number_of_messages_to_poll,
        )

        return [
            cast(KafkaPollRecord, consumer_record)
            for consumer_records in poll_results.values()
            for consumer_record in consumer_records
        ]

    def consume(
        self,
        *,
        kafka_poll_record: KafkaPollRecord,
        consumption_callback: Callable[[KafkaConsumerRecord], None],
    ) -> None:
        if kafka_poll_record.value is not None:
            consumption_callback(
                KafkaConsumerRecord(
                    value=self.__byte_deserializer.deserialize(kafka_poll_record.value),
                    headers=self.__header_serializer.unserialize(kafka_poll_record.headers),
                )
            )

        self.__consumer.commit()

    def stop(self) -> None:
        self.__logger.info(f"Closing connection of consumer with group_id={self.__consumer_group}")
        self.__consumer.close(autocommit=False)
