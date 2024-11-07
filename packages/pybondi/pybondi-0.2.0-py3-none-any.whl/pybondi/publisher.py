from typing import Any
from abc import ABC, abstractmethod

class Subscriber(ABC):
    """
    An abstract base class for subscribers to a publisher.

    Subscribers are responsible for receiving messages, managing transactions,
    and closing their connections.
    """

    @abstractmethod
    def receive(self, message: Any) -> None:
        """
        Receives a message from the publisher.

        Args:
            message: The message to be received.
        """

    @abstractmethod
    def begin(self) -> None:
        """
        Starts a new transaction.
        """

    @abstractmethod
    def commit(self) -> None:
        """
        Commits the current transaction.
        """

    @abstractmethod
    def rollback(self) -> None:
        """
        Rolls back the current transaction.
        """

    @abstractmethod
    def close(self) -> None:
        """
        Closes the subscriber and its connection.
        """


class Publisher:
    """
    A publisher that manages a set of subscribers and publishes messages to them.

    The publisher is responsible for subscribing and unsubscribing subscribers,
    publishing messages to subscribed topics, and coordinating transactions
    across all subscribers.

    The difference between a publisher and a message bus is that a publisher
    is responsible for publish data from the inside of the bounded context
    to outside systems. A message bus is responsible for routing events and
    commands within the bounded context.
    """

    def __init__(self) -> None:
        """
        Initializes the publisher with an empty subscriber dictionary.
        """
        self.subscribers = dict[str, list[Subscriber]]()

    def subscribe(self, topic: str, subscriber: Subscriber) -> None:
        """
        Subscribes a subscriber to a specific topic.

        Parameters:
            topic: The topic to subscribe to.
            subscriber: The subscriber to add.
        """
        self.subscribers.setdefault(topic, []).append(subscriber)

    def publish(self, topic: str, message: Any) -> None:
        """
        Publishes a message to a specific topic.

        The message is sent to all subscribers of the given topic.

        Parameters:
            topic: The topic to publish to.
            message: The message to be published.
        """
        for subscriber in self.subscribers.get(topic, []):
            subscriber.receive(message)

    def commit(self) -> None:
        """
        Commits the current transaction for all subscribers.
        """
        for list in self.subscribers.values():
            [subscriber.commit() for subscriber in list]

    def rollback(self) -> None:
        """
        Rolls back the current transaction for all subscribers.
        """
        for list in self.subscribers.values():
            [subscriber.rollback() for subscriber in list]

    def begin(self) -> None:
        """
        Starts a new transaction for all subscribers.
        """
        for list in self.subscribers.values():
            [subscriber.begin() for subscriber in list]

    def close(self) -> None:
        """
        Closes all subscribers and their connections.
        """
        for list in self.subscribers.values():
            [subscriber.close() for subscriber in list]