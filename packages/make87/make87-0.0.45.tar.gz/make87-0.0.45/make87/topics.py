import os
import threading
from collections import deque
from datetime import timedelta
from functools import partial
from typing import Callable, Dict, Optional, TypeVar, Generic, List, Tuple, Any
from typing import Type
from typing import Union

import zenoh
from google.protobuf.message import Message
from make87.utils import parse_topics, PUB, SUB
from zenoh import Session
from zenoh.handlers import RingChannel

T = TypeVar("T", bound=Message)
T_M = TypeVar("T_M", bound="MessageWithMetadata")


class Topic:
    """Base class for topics."""

    def __init__(self, name: str):
        self.name = name


class Metadata:
    def __init__(self, topic_name: str, message_type_decoded: str, bytes_transmitted: int):
        self.topic_name: str = topic_name
        self.message_type_decoded: str = message_type_decoded
        self.bytes_transmitted: int = bytes_transmitted

    def __repr__(self):
        return f"Metadata(topic_name={self.topic_name}, message_type_decoded={self.message_type_decoded}, bytes_transmitted={self.bytes_transmitted})"

    def __str__(self):
        return f"Metadata(topic_name={self.topic_name}, message_type_decoded={self.message_type_decoded}, bytes_transmitted={self.bytes_transmitted})"


class MessageWithMetadata(Generic[T]):
    """A message with metadata."""

    def __init__(self, message: T, metadata: Metadata):
        self.message: T = message
        self.metadata: Metadata = metadata


class TypedPublisherTopic(Generic[T]):
    """A typed publisher topic that publishes messages of type `T`."""

    def __init__(self, inner: "PublisherTopic", message_type: Type[T]):
        self._inner = inner
        self._message_type = message_type  # Store the actual class for runtime encoding

    def publish(self, message: T) -> None:
        """Publish a message of type `T`."""
        if not message.HasField("timestamp"):
            message.timestamp.GetCurrentTime()  # Assuming this method exists

        encoded_message = message.SerializeToString()
        self._inner.publisher.put(zenoh.ZBytes(encoded_message))


class PublisherTopic(Topic):
    """A topic used for publishing messages."""

    def __init__(self, name: str, session: zenoh.Session):
        super().__init__(name)
        self._session = session
        self._pub = self._session.declare_publisher(
            f"{name}", encoding=zenoh.Encoding.APPLICATION_PROTOBUF, priority=zenoh.Priority.REAL_TIME, express=True
        )

    @property
    def publisher(self):
        return self._pub


class TypedSubscriberTopic(Generic[T]):
    """A typed subscriber topic that provides messages of type `T`."""

    def __init__(self, inner: "SubscriberTopic", message_type: Type[T]):
        self._inner = inner
        self._message_type = message_type  # Store the actual class for runtime decoding

    def subscribe(self, callback: Callable[[T], None]) -> None:
        """Subscribe to the topic with a callback that expects messages of type `T`."""

        def _decode_message(sample: zenoh.Sample):
            message = self._message_type()
            try:
                message.ParseFromString(sample.payload.to_bytes())
                callback(message)
            except Exception as e:
                raise Exception(f"Failed to decode message on topic '{self._inner.name}': {e}")

        self._inner.subscribe(_decode_message)

    def subscribe_with_metadata(self, callback: Callable[[MessageWithMetadata[T]], None]) -> None:
        """Subscribe to the topic with a callback that expects messages of type `T`."""

        def _decode_message(sample: zenoh.Sample):
            message = self._message_type()
            try:
                message.ParseFromString(sample.payload.to_bytes())
            except Exception as e:
                raise Exception(f"Failed to decode message on topic '{self._inner.name}': {e}")

            callback(
                MessageWithMetadata(
                    message=message,
                    metadata=Metadata(
                        topic_name=str(sample.key_expr),
                        message_type_decoded=type(message).__name__,
                        bytes_transmitted=len(sample.payload),
                    ),
                )
            )

        self._inner.subscribe(_decode_message)

    def receive(self) -> T:
        """Receive a message from the topic."""
        sample = self._inner.subscriber.recv()
        message = self._message_type()
        message.ParseFromString(sample.payload.to_bytes())
        return message

    def receive_with_metadata(self) -> MessageWithMetadata[T]:
        """Receive a message from the topic."""
        sample = self._inner.subscriber.recv()
        message = self._message_type()
        message.ParseFromString(sample.payload.to_bytes())
        return MessageWithMetadata(
            message=message,
            metadata=Metadata(
                topic_name=str(sample.key_expr),
                message_type_decoded=type(message).__name__,
                bytes_transmitted=len(sample.payload),
            ),
        )


class SubscriberTopic(Topic):
    """A topic used for subscribing to messages."""

    def __init__(self, name: str, session: zenoh.Session):
        super().__init__(name)
        self._session = session
        self._sub = self._session.declare_subscriber(f"{self.name}", RingChannel(1))  # supports `.recv`
        self._cb_subs = []
        self._subscribers = []

    def _callback(self, sample: zenoh.Sample) -> None:
        for subscriber in self._subscribers:
            subscriber(sample)

    @property
    def subscriber(self) -> zenoh.Subscriber:
        return self._sub

    def subscribe(self, callback: Callable) -> None:
        self._cb_subs.append(self._session.declare_subscriber(f"{self.name}", callback))


class MultiSubscriberTopic:
    """Handles synchronized subscription to multiple topics."""

    def __init__(
        self,
        delta_time: float = 0.1,
    ):
        self._subscriber_topics: List[TypedSubscriberTopic] = []
        self._buffers: Dict[str, deque] = {}
        self._delta_time: timedelta = timedelta(seconds=delta_time)
        self._lock: threading.Lock = threading.Lock()

    def _buffer_message(self, callback: Callable[[T], None], message_with_metadata: MessageWithMetadata[T]):
        message, metadata = message_with_metadata.message, message_with_metadata.metadata
        with self._lock:
            self._buffers[metadata.topic_name].append(
                {"message": message, "metadata": metadata, "timestamp": message.timestamp.ToDatetime()}
            )
            self._try_match_messages(callback=callback)

    def _buffer_message_with_metadata(
        self, callback: Callable[[T_M], None], message_with_metadata: MessageWithMetadata[T]
    ):
        message, metadata = message_with_metadata.message, message_with_metadata.metadata
        with self._lock:
            self._buffers[metadata.topic_name].append(
                {"message": message, "metadata": metadata, "timestamp": message.timestamp.ToDatetime()}
            )
            self._try_match_messages_with_metadata(callback=callback)

    def _try_match_messages_generic(
        self, callback: Callable[[Any], None], message_extractor: Callable[[Dict[str, Any]], Any]
    ):
        while all(self._buffers[topic._inner.name] for topic in self._subscriber_topics):
            msg_group = [self._buffers[topic._inner.name][0] for topic in self._subscriber_topics]
            timestamps = [msg["timestamp"] for msg in msg_group]
            if max(timestamps) - min(timestamps) <= self._delta_time:
                messages = tuple(message_extractor(msg) for msg in msg_group)
                callback(messages)
                for topic in self._subscriber_topics:
                    self._buffers[topic._inner.name].popleft()
                return
            else:
                # Remove the oldest message
                oldest_topic_name = min(self._buffers, key=lambda name: self._buffers[name][0]["timestamp"])
                self._buffers[oldest_topic_name].popleft()

    def _try_match_messages(self, callback: Callable[[T], None]):
        self._try_match_messages_generic(callback, lambda msg: msg["message"])

    def _try_match_messages_with_metadata(self, callback: Callable[[T_M], None]):
        self._try_match_messages_generic(
            callback,
            lambda msg: MessageWithMetadata(message=msg["message"], metadata=msg["metadata"]),
        )

    def add_topic(self, topic: TypedSubscriberTopic, max_queue_size: int = 10):
        with self._lock:
            self._subscriber_topics.append(topic)
            self._buffers[topic._inner.name] = deque(maxlen=max_queue_size)

    def subscribe(self, callback: Callable[[Tuple[T, ...]], None]) -> None:
        if not self._subscriber_topics:
            raise ValueError("No topics added to MultiSubscriberTopic. Please call add_topic() first.")
        for topic in self._subscriber_topics:
            topic.subscribe_with_metadata(partial(self._buffer_message, callback))

    def subscribe_with_metadata(self, callback: Callable[[Tuple[T_M, ...]], None]) -> None:
        if not self._subscriber_topics:
            raise ValueError("No topics added to MultiSubscriberTopic. Please call add_topic() first.")
        for topic in self._subscriber_topics:
            topic.subscribe_with_metadata(partial(self._buffer_message_with_metadata, callback))


class _TopicManager:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self._session: Optional[Session] = None
        self._topics: Dict[str, Union[PublisherTopic, SubscriberTopic]] = {}
        self._topic_names: Dict[str, str] = {}
        self._initialized: bool = False

    @classmethod
    def get_instance(cls):
        """Singleton pattern to ensure only one instance exists."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def initialize(self):
        """Initialize the session and topics."""
        with self._lock:
            if self._initialized:
                return  # Already initialized

            # Read configuration from environment variables
            if "COMMUNICATION_CONFIG" in os.environ:
                config = zenoh.Config.from_json5(os.environ["COMMUNICATION_CONFIG"])
            else:
                config = zenoh.Config()
            self._session = zenoh.open(config=config)
            # Initialize topics
            self._initialize_topics()
            self._initialized = True

    def _initialize_topics(self):
        """Initialize topics based on the TOPICS environment variable."""
        topic_data = parse_topics()

        for topic in topic_data.topics:
            if topic.topic_key in self._topics:
                continue  # Topic already initialized
            if isinstance(topic, PUB):
                topic_type = PublisherTopic(
                    name=topic.topic_key,
                    session=self._session,
                )
            elif isinstance(topic, SUB):
                topic_type = SubscriberTopic(
                    name=topic.topic_key,
                    session=self._session,
                )
            else:
                raise ValueError(f"Invalid topic type {topic.topic_type}")
            self._topics[topic.topic_key] = topic_type
            self._topic_names[topic.topic_name] = topic.topic_key

    def _get_untyped_topic(self, name: str) -> Union[PublisherTopic, SubscriberTopic]:
        """Retrieve a topic by name."""
        if not self._initialized:
            raise RuntimeError("SessionManager not initialized. Call initialize() first.")
        if name not in self._topics:
            available_topics = ", ".join(self._topics.keys())
            raise ValueError(f"Topic '{name}' not found. Available topics: {available_topics}")
        return self._topics[name]

    def get_publisher_topic(self, name: str, message_type: Type[T]) -> TypedPublisherTopic[T]:
        """Retrieve a publisher topic by name."""
        topic = self._get_untyped_topic(name=name)
        if not isinstance(topic, PublisherTopic):
            raise ValueError(f"Topic '{name}' is not a publisher topic.")
        return TypedPublisherTopic(inner=topic, message_type=message_type)

    def get_subscriber_topic(self, name: str, message_type: Type[T]) -> TypedSubscriberTopic[T]:
        """Retrieve a topic by name."""
        topic = self._get_untyped_topic(name=name)
        if not isinstance(topic, SubscriberTopic):
            raise ValueError(f"Topic '{name}' is not a subscriber topic.")
        return TypedSubscriberTopic(inner=topic, message_type=message_type)

    def resolve_topic_name(self, name: str) -> str:
        """Resolve a topic name to a topic key."""
        if not self._initialized:
            raise RuntimeError("SessionManager not initialized. Call initialize() first.")
        if name not in self._topic_names:
            raise ValueError(f"Topic name '{name}' not found.")
        return self._topic_names[name]


def get_publisher_topic(name: str, message_type: Type[T]) -> TypedPublisherTopic[T]:
    """Retrieve a publisher topic by name.

    Args:
        name: The name of the topic to retrieve used in the `MAKE87.yml` file.
        message_type: The type of message to be published.

    Returns:
        The publisher topic object.

    Raises:
        RuntimeError: If the make87 library has not been initialized correctly. Call `make87.initialize()`.
        ValueError: If the topic is not found.
        ValueError: If the topic is not a publisher topic.

    """
    return _TopicManager.get_instance().get_publisher_topic(name=name, message_type=message_type)


def get_subscriber_topic(name: str, message_type: Type[T]) -> TypedSubscriberTopic[T]:
    """Retrieve a subscriber topic by name.

    Args:
        name: The name of the topic to retrieve used in the `MAKE87.yml` file.
        message_type: The type of message to be subscribed to. Will be used for automatic decoding.

    Returns:
        The subscriber topic object.

    Raises:
        RuntimeError: If the make87 library has not been initialized correctly. Call `make87.initialize()`.
        ValueError: If the topic is not found.
        ValueError: If the topic is not a subscriber topic.
    """
    return _TopicManager.get_instance().get_subscriber_topic(name=name, message_type=message_type)


def resolve_topic_name(name: str) -> str:
    """Resolve a topic name to its dynamic topic key.

    Args:
        name: Name of the topic used in the `MAKE87.yml` file.

    Returns:
        The dynamic topic key used to reference the topic.

    Raises:
        RuntimeError: If the make87 library has not been initialized correctly. Call `make87.initialize()`.
        ValueError: If the topic name is not found.
    """
    return _TopicManager.get_instance().resolve_topic_name(name)
