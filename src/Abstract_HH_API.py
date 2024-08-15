from abc import ABC, abstractmethod

class GetAPI(ABC):
    """

    """

    @abstractmethod
    def user_choice(self, keyword):
        pass

    @abstractmethod
    def load_data(self):
        pass