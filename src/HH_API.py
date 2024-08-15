import requests
from config import get_url
from src.Abstract_HH_API import GetAPI


class HeadHuntersAPI(GetAPI):
    """

    """

    def __init__(self):
        self.__url = get_url
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"text": "", "per_page": 10, "only_with_vacancies": True}

    def user_choice(self, keyword):
        """

        :param keyword:
        :return:
        """
        self.params["text"] = keyword
        get_response = requests.get(url=self.__url, headers=self.headers, params=self.params)
        if get_response.status_code != 200:
            raise Exception(f"Ошибка: {get_response.status_code}")
        return get_response.json()

    def load_data(self):
        pass


check = HeadHuntersAPI()
print(check.user_choice(input()), sep="\n")
