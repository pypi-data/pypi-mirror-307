from abc import ABC, abstractmethod
from typing import Any
from typing import Sequence
from pybondi.publisher import Publisher

class Callback(ABC):
    '''
    Callbacks should be injected into the aggregate's methods to allow it to process
    data and communicate their results to the message publisher.
    '''

    def __init__(self):
        self.publisher = Publisher()

    def bind(self, publisher: Publisher):
        '''
        Bind a publisher to the callback object.        
        '''
        self.publisher = publisher

    def set(self, name: str, value: Any) -> None:
        '''
        Set a value on the callback object.

        Paramaters:
            name: The name of the attribute.
            value: The value to set.       
        '''
        setattr(self, name, value)

    @abstractmethod
    def __call__(self, *args, **kwargs):
        '''
        Call the callback object. Data from the aggregate's methods should be passed
        to the callback object through this method, and processed accordingly.

        The callback object should also communicate the results of the processing to
        the message publisher directly or should implement a buffer to store the results
        until the flush method is called.        
        '''
        ...

    @abstractmethod
    def flush(self): 
        '''
        Flush the callback object. If the callback object has a buffer, the buffer should
        be flushed and the data should be sent to the message publisher.    
        '''
        ...

    @abstractmethod
    def reset(self):
        '''
        Reset the callback object. The callback object should reset any internal state
        that it maintains, if any.
        '''
        ...


class Callbacks:
    '''
    Callbacks is a class that manages a group of callback objects. It is responsible for
    calling the callback objects, flushing their buffers, and resetting their internal
    state, as if they were a single callback object.

    Example:

    callback = Callbacks([SomeCallback(), OtherCallback())
    '''

    def __init__(self, callbacks: Sequence[Callback]):
        self.publisher = Publisher()
        self.list = list[Callback](callbacks)
    
    def bind(self, publisher: Publisher):
        '''
        Bind a publisher to all the callback objects.
        '''
        [callback.bind(publisher) for callback in self.list]

    def set(self, name: str, value: Any) -> None:
        '''
        Set a value to all the callback objects.

        Paramaters:
            name: The name of the attribute.
            value: The value to set.       
        '''
        [callback.set(name, value) for callback in self.list]


    def __call__(self, *args, **kwargs):
        '''
        Call the callbacks. Data from the aggregate's methods should be passed
        to the callback objects through this method, and processed accordingly.   
        '''
        [callback(*args, **kwargs) for callback in self.list]

    def flush(self):
        '''
        Flush the callbacks. If the callback objects have a buffer, the buffer should
        be flushed and the data should be sent to the message publisher.    
        '''
        [callback.flush() for callback in self.list]
        
    def reset(self):
        '''
        Reset the callbacks. The callback objects should reset any internal state
        that they maintain, if any.
        '''
        [callback.reset() for callback in self.list]