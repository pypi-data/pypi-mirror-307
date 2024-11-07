from pybondi.aggregate import Aggregate
from pybondi.messagebus import Messagebus, Command
from pybondi.repository import Repository
from pybondi.publisher import Publisher

class Session:
    """
    A session manages a unit of work, cordinates the repository, the message bus and
    the publisher, mantaing the transactional boundaries.
    """

    def __init__(self, repository: Repository, publisher: Publisher, messagebus: Messagebus):
        self.repository = repository
        self.messagebus = messagebus
        self.publisher = publisher

    def add(self, aggregate: Aggregate):
        """
        Adds an aggregate to the repository.
        """
        self.repository.add(aggregate)

    def collect_events(self):
        """
        Collects events from all aggregates in the repository and enqueues them in the message bus.
        """
        for aggregate in self.repository.aggregates.values():
            while aggregate.root.events:
                event = aggregate.root.events.popleft()
                self.messagebus.enqueue(event)

    def run(self):
        """
        Processes all messages in the queue.
        """
        while self.messagebus.queue:
            message = self.messagebus.dequeue()
            self.messagebus.dispatch(message)
            self.collect_events()

    def execute(self, command: Command):
        """
        Executes a command by enqueuing it in the message bus and processing all messages in the queue.
        """
        self.messagebus.enqueue(command)
        self.run()

    def begin(self):
        """
        Begins a new transaction.
        """
        self.publisher.begin()

    def commit(self):
        """
        Commits changes from the transaction.
        """
        self.repository.commit(), self.publisher.commit()

    def rollback(self):
        """
        Rolls back changes of the transaction.
        """
        self.repository.rollback(), self.publisher.rollback()

    def close(self):
        """
        Closes the session.
        """
        self.publisher.close()

    def __enter__(self):
        self.publisher.begin()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.run()
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.close()