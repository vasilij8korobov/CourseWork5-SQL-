from abc import ABC, abstractmethod


class GetAPI(ABC):
    """
    Абстрактный класс для получения вакансии с hh.ru
    """

    @abstractmethod
    def load_data(self):
        pass
