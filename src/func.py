import progressbar
import psycopg2

from config import config
from src.Company import Company
from src.DBManager import DBManager
from src.HH_API import HeadHunterCompany, HeadHunterVacancy
from src.Vacancy import Vacancy

companies_ids = [2458132, 867009, 3533565, 9887868, 1446270, 2729188, 9137365, 4797848, 99985, 4606]


def create_database(database_name: str, params: dict) -> None:
    """ Создание БД и таблиц для сохранения данных о компаниях и вакансиях """

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE companies (
                employer_id INTEGER PRIMARY KEY,
                company_name VARCHAR NOT NULL,
                company_description TEXT,
                company_site_url TEXT,
                open_vacancies INTEGER
            )
        """)

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE vacancies (
                vacancy_name VARCHAR,
                alternate_url TEXT,
                salary_from INTEGER,
                salary_to INTEGER,
                salary_currency VARCHAR,
                employer_id INTEGER REFERENCES companies(employer_id),
                vacancy_area_name VARCHAR,
                requirement TEXT,
                responsibility TEXT
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(table_name: str, data: dict, database_name: str, params: dict) -> None:
    """ Функция сохраняет данные в БД """

    conn = psycopg2.connect(dbname=database_name, **params)
    conn.autocommit = True
    cur = conn.cursor()

    columns = ', '.join(data.keys())
    values = ', '.join(["%s"] * len(data))

    sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

    cur.execute(sql_query, list(data.values()))

    cur.close()
    conn.close()


def get_and_save_company_data(database_name: str, params: dict):
    """ Функция получает и сохраняет данные о компаниях с hh.ru в БД"""

    companies_list = []

    bar = progressbar.ProgressBar(
        maxval=len(companies_ids),
        widgets=['Загрузка компании: ', progressbar.Percentage(), ' ', progressbar.Bar(), ' ',
                 progressbar.ETA()]
    )
    bar.start()
    for i, company_id in enumerate(companies_ids):
        company = HeadHunterCompany(company_id)
        companies_list.append(company.load_data())
        bar.update(i + 1)
    bar.finish()

    companies = [Company.from_company_cls(company) for company in companies_list]
    bar = progressbar.ProgressBar(
         maxval=len(companies),
         widgets=['Сохранение данных: ', progressbar.Percentage(), ' ', progressbar.Bar(), ' ',
                  progressbar.ETA()]
    )
    bar.start()
    for i, company in enumerate(companies):
        companies_data = {
            "employer_id": company.employer_id,
            "company_name": company.name,
            "company_description": company.description,
            "company_site_url": company.site_url,
            "open_vacancies": company.open_vacancies
        }
        save_data_to_database('companies', companies_data, database_name, params)
        bar.update(i + 1)
    bar.finish()


def get_and_save_vacancy_data(database_name: str, params: dict):
    """ Функция получает и сохраняет данные о вакансиях с hh.ru в БД"""

    vacancies_list = []

    bar = progressbar.ProgressBar(
         maxval=len(companies_ids),
         widgets=['Загрузка вакансии: ', progressbar.Percentage(), ' ', progressbar.Bar(), ' ',
                  progressbar.ETA()]
    )
    bar.start()
    for i, vacancies_id in enumerate(companies_ids):
        vacancy = HeadHunterVacancy(vacancies_id)
        vacancies_list.extend(vacancy.load_data())
        bar.update(i + 1)
    bar.finish()

    vacancies = [Vacancy.from_vacancy_cls(vacancy) for vacancy in vacancies_list]
    bar = progressbar.ProgressBar(
         maxval=len(vacancies),
         widgets=['Сохранение данных: ', progressbar.Percentage(), ' ', progressbar.Bar(), ' ',
                  progressbar.ETA()]
    )
    bar.start()
    for i, vacancy in enumerate(vacancies):
        vacancy_data = {
            "vacancy_name": vacancy.name,
            "alternate_url": vacancy.alternate_url,
            "salary_from": vacancy.salary_from,
            "salary_to": vacancy.salary_to,
            "salary_currency": vacancy.salary_currency,
            "employer_id": vacancy.employer_id,
            "vacancy_area_name": vacancy.area_name,
            "requirement": vacancy.requirement,
            "responsibility": vacancy.responsibility
        }
        save_data_to_database('vacancies', vacancy_data, database_name, params)
        bar.update(i + 1)
    bar.finish()

    print("Вся информация сохранена в базу данных hh\n")


def user_request():
    """ Функция отрабатывает запросы пользователя по выводу нужной информации """

    params = config()
    db_manager = DBManager("hh", params)

    user_input = input("Выберите запрос:\n"
                       "1 - Вывести список всех компаний и количество вакансии у каждой компании\n"
                       "2 - Вывести список всех вакансии с указанием названия компании, названия вакансии и зарплаты "
                       "и ссылки на вакансию\n"
                       "3 - Вывести среднюю зарплату по вакансиям\n"
                       "4 - Вывести список всех вакансии, у которых зарплата выше средней по всем вакансиям\n"
                       "5 - Вывести список всех вакансии, в названии которых содержится запрашиваемое слово\n")

    if user_input == "1":
        companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
        print("Список всех компаний и количество вакансии у каждой компании:\n")
        for i in companies_and_vacancies_count:
            print(i)

    elif user_input == "2":
        all_vacancies = db_manager.get_all_vacancies()
        print("Cписок всех вакансии с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию:"
              "\n")
        for i in all_vacancies:
            print(i)

    elif user_input == "3":
        avg_salary = db_manager.get_avg_salary()
        print(f"Средняя зарплата по вакансиям: {avg_salary}\n")

    elif user_input == "4":
        vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
        print("Список всех вакансии, у которых зарплата выше средней по всем вакансиям:\n")
        for i in vacancies_with_higher_salary:
            print(i)

    elif user_input == "5":
        user_choice = input("Введите ключевое слово\n")
        vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_choice)
        print("Список всех вакансии, в названии которых содержится запрашиваемое слово:\n")
        for i in vacancies_with_keyword:
            print(i)
