from abc import ABC, abstractmethod


def BaseHandler(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def handle(self):
        raise NotImplementedError(f"Must implement {self.handle.__name__}")
