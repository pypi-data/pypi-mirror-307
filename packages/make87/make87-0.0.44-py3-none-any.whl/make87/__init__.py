from make87.handlers import logging_handler, stdout_handler, stderr_handler
from make87.peripherals import _PeripheralManager
from make87.peripherals import resolve_peripheral_name  # noqa
from make87.topics import _TopicManager
from make87.topics import (  # noqa
    get_publisher_topic,
    get_subscriber_topic,
    resolve_topic_name,
    MessageWithMetadata,
    Metadata,
    TypedPublisherTopic,
    TypedSubscriberTopic,
    MultiSubscriberTopic,
)

__all__ = [
    "MessageWithMetadata",
    "Metadata",
    "MultiSubscriberTopic",
    "TypedPublisherTopic",
    "TypedSubscriberTopic",
    "get_publisher_topic",
    "get_subscriber_topic",
    "initialize",
    "resolve_peripheral_name",
    "resolve_topic_name",
]


def initialize():
    """Initializes the Make87 SDK. Must be called before using any other SDK functions."""
    # Initialize the session manager
    _TopicManager.get_instance().initialize()
    _PeripheralManager.get_instance().initialize()
    # Set up logging and handlers
    logging_handler.setup()
    stdout_handler.setup()
    stderr_handler.setup()
