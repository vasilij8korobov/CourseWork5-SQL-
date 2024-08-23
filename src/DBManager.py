from decimal import Decimal

import psycopg2


class DBManager:
    """ Класс для подключения к БД """

    def __init__(self, database_name: str, params: dict):
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.cur = self.conn.cursor()
        self.conn.autocommit = True

    def get_companies_and_vacancies_count(self):
        """ Метод получает список всех компаний и количество вакансии у каждой компании """

        self.cur.execute(
            """
            SELECT c.company_name, COUNT(v.employer_id)
            FROM companies c
            JOIN vacancies v USING (employer_id)
            GROUP BY c.company_name
            ORDER BY COUNT DESC
            """
        )
        return self.cur.fetchall()

    def get_all_vacancies(self):
        """ Метод получает список всех вакансии с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию """

        self.cur.execute(
            """
            SELECT c.company_name, v.vacancy_name, v.salary_from, v.salary_to, v.salary_currency, v.alternate_url
            FROM vacancies v
            JOIN companies c USING (employer_id)
            WHERE v.salary_from != 0 AND v.salary_from IS NOT NULL AND v.salary_to != 0 AND v.salary_to IS NOT NULL
            ORDER BY v.salary_from DESC
            """
        )
        return self.cur.fetchall()

    def get_avg_salary(self):
        """ Метод получает среднюю зарплату по вакансиям """

        self.cur.execute(
            """
            SELECT AVG((salary_from + salary_to) / 2) AS avg_salary
            FROM vacancies
            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
            """
        )
        result = self.cur.fetchone()
        avg_salary = Decimal(result[0])
        formatted_avg_salary = format(avg_salary, '.2f')
        return formatted_avg_salary

    def get_vacancies_with_higher_salary(self):
        """ Метод получает список всех вакансии, у которых зарплата выше средней по всем вакансиям """

        avg_salary = self.get_avg_salary()[0][0]

        self.cur.execute(
            """
            SELECT v.vacancy_name, v.salary_from, v.salary_to, v.alternate_url
            FROM vacancies v
            WHERE ((v.salary_from + v.salary_to) / 2) > %s
            """, (avg_salary,)
        )
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """ Метод получает список всех вакансии, в названии которых содержатся переданные с метод слова """

        keyword = f"%{keyword.lower()}%"

        self.cur.execute(
            """
            SELECT v.vacancy_name, v.salary_from, v.salary_to, v.alternate_url
            FROM vacancies v
            WHERE LOWER(v.vacancy_name) LIKE %s
            """, (keyword,)
        )
        return self.cur.fetchall()
