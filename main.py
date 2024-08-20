from config import config
from src.func import create_database, get_and_save_company_data, get_and_save_vacancy_data, user_request


def main():
    """ Запуск программы """

    print("Началось получение и сохранение данных...")

    params = config()

    create_database("hh", params)
    get_and_save_company_data("hh", params)
    get_and_save_vacancy_data("hh", params)
    user_request()

    while True:
        user_choice = input("Хотите сделать еще один запрос?\n").lower()
        if user_choice == "да":
            user_request()
        else:
            break


if __name__ == "__main__":
    main()
