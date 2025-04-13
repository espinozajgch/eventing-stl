from abc import ABC, abstractmethod

class BaseProviderConverter(ABC):
    def __init__(self):
        self.scale = (105, 68)

    @abstractmethod
    def convert(self, event):
        pass