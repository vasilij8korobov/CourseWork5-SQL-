import requests
from src.Abstract_HH_API import GetAPI


class HeadHunterCompany(GetAPI):
    """
    Класс для подключения к API работодателя на HH.ru
    """

    def __init__(self, employer_id: int):
        self.__url = f"https://api.hh.ru/employers/{employer_id}"
        self.headers = {"User-Agent": "HH-User-Agent"}

    def load_data(self):
        """ Метод выгружает данные """

        get_response = requests.get(self.__url, headers=self.headers)
        data = get_response.json()
        return data


class HeadHunterVacancy(GetAPI):
    """ Класс для подключения к API вакансии работодателя """

    def __init__(self, vacancies_id):
        self.__url = f"https://api.hh.ru/vacancies?employer_id={vacancies_id}"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"per_page": 100}

    def load_data(self):
        get_response = requests.get(self.__url, headers=self.headers, params=self.params)
        data = get_response.json()['items']
        return data
