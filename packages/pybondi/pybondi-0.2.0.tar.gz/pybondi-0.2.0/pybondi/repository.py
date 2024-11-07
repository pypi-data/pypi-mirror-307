from abc import ABC, abstractmethod
from pybondi.aggregate import Aggregate

class Repository(ABC):
    """
    Repository is an abstract class that defines the interface for storing and restoring aggregates.

    It maintains an internal identity map of aggregates and provides methods for:
    - Adding new aggregates to the map.
    - Committing changes to the underlying storage.
    - Rolling back changes to the previous state.

    Concrete subclasses must implement the `store` and `restore` methods to provide
    specific storage and retrieval mechanisms.
    """

    
    def __init__(self):
        self.aggregates = dict[str, Aggregate]()

    def add(self, aggregate: Aggregate):
        """
        Adds an aggregate to the internal identity map.

        Parameters:
            aggregate: The aggregate to be added.
        """
        self.aggregates[aggregate.root.id] = aggregate

    def commit(self):
        """
        Commits changes to the underlying storage for all stored aggregates.

        Iterates over each aggregate in the identity map and calls the `store` method
        to persist its current state.
        """
        for aggregate in self.aggregates.values():
            self.store(aggregate)

    def rollback(self):
        """
        Rolls back changes to the previous state for all stored aggregates.

        Iterates over each aggregate in the identity map and calls the `restore` method
        to load its previous state from storage.
        """
        for aggregate in self.aggregates.values():
            self.restore(aggregate)

    @abstractmethod
    def store(self, aggregate: Aggregate):
        """
        Stores the given aggregate to the underlying storage.

        Args:
            aggregate: The aggregate to be stored.
        """
        ...

    @abstractmethod
    def restore(self, aggregate: Aggregate):
        """
        Restores the given aggregate from the underlying storage.

        Args:
            aggregate: The aggregate to be restored.
        """
        ...
