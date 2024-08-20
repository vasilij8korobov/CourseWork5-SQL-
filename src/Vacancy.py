from typing import Any


class Vacancy:
    """ Класс для работы с вакансиями """

    __slots__ = (
        "name", "alternate_url", "salary_from", "salary_to", "salary_currency", "employer_id", "area_name",
        "requirement", "responsibility"
    )

    def __init__(
            self, name, alternate_url, salary_from, salary_to, salary_currency, employer_id, area_name, requirement,
            responsibility
    ):
        """ Конструктор класса """

        self.name: str = name
        self.alternate_url: str = alternate_url
        self.salary_from: int = salary_from
        self.salary_to: int = salary_to
        self.salary_currency: str = salary_currency
        self.employer_id = employer_id
        self.area_name: str = area_name
        self.requirement: str = requirement
        self.responsibility: str = responsibility

    def __str__(self) -> str:
        """ Строковое представление вакансии """

        return (f"Наименование вакансии: {self.name}\n"
                f"Ссылка на вакансию: {self.alternate_url}\n"
                f"Зарплата: от {self.salary_from} до {self.salary_to}\n"
                f"Валюта: {self.salary_currency}\n"
                f"ID компании: {self.employer_id}"
                f"Место работы: {self.area_name}\n"
                f"Краткое описание: {self.requirement}\n"
                f"{self.responsibility}\n")

    @classmethod
    def from_vacancy_cls(cls, vacancy_data: dict) -> Any:
        """ Метод возвращает экземпляр класса в виде словаря """

        if isinstance(vacancy_data, dict):

            salary = vacancy_data.get("salary", {})
            salary_from = salary.get("from", 0) if salary else 0
            salary_to = salary.get("to", 0) if salary else 0
            salary_currency = salary.get("currency", "Нет данных") if salary else "Нет данных"

            return cls(
                vacancy_data["name"],
                vacancy_data["alternate_url"],
                salary_from,
                salary_to,
                salary_currency,
                vacancy_data["employer"]["id"],
                vacancy_data["area"]["name"],
                vacancy_data["snippet"].get("requirement", "Нет данных о требованиях"),
                vacancy_data["snippet"].get("responsibility", "Нет данных об обязанностях"),
            )
        else:
            print("Ошибка: данные компании должны быть словарем")
            return None