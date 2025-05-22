import os
from datetime import datetime

from controllers.budget_controller import BudgetController
from models.transaction import CATEGORIES, Transaction
from utils.serialization_handler import SerializationHandler
from utils.data_generator import generate_example_json


def _debug_create_test_data():
    generate_example_json()
    print("Testowy budżet wygenerowany")


class Console:
    header = "---- [ MANAGER BUDŻETU ] ----"
    def __init__(self):
        self._bc = BudgetController()

    def run(self):
        self.__main_loop()

    def __main_loop(self):
        user_input = 1

        while user_input != 0:
            self._main_menu()
            user_input = int(input())

            match user_input:
                case 1:
                    self._load_budget()

                case 2:
                    self._budget()

                case 3:
                    self._add_transaction()

                case 4:
                    self._remove_transaction()

                case 99:
                    _debug_create_test_data()

                case 0:
                    break


            os.system('cls')

    def _main_menu(self):
        menu = f"""
{self.header}
Działasz na pliku budżetowym: {self._bc.get_transaction_file_path()}
Dostępne środki {self._bc.get_funds()}
[1] Wczytaj budżet
[2] Wyświetl budżet
[3] Dodaj transakcje
[4] Usuń transakcje

[99] Wygeneruj testowy budżet (debug)
[0] Wyjdź
"""

        print(menu)

    def _load_budget(self):

        files_str = [filename for filename in os.listdir("data")]
        s = f"""
{self.header}
Dostępne pliki:
{files_str}

Podaj nazwę pliku:
"""
        print(s)

        user_input = str(input())
        self._bc.load_transactions(user_input)


    def _budget(self):

        if self.__file_not_loaded():
            transactions_str = "Nie wczytano pliku z budżetem"
        else:
            transactions_str = sorted(self._bc.transactions, key=lambda t: t.date)
        s = f"""
{self.header}
Transakcje:
{transactions_str}

"""
        print(s)

        str(input("Naciśnij dowolny klawisz aby kontynuować"))

    def _add_transaction(self):

        print({self.header})

        if self.__file_not_loaded():
            print("Nie wczytano pliku z budżetem")
            return

        print("Podaj dane transakcji")

        try:
            date_input = str(input("Podaj datę w formacie YYYY-MM-DD: "))

            # bez map() zmienne byłyby str a nie int
            year, month, day = map(int, date_input.split('-'))
            date = datetime(year, month, day)

            category_input = str(input("Podaj kategorię: "))
            if category_input not in CATEGORIES:
                category = "Inne"
            else:
                category = category_input

            amount_input = float(input("Podaj kwotę transakcji: "))
            amount = round(amount_input, 2)

            is_euro = input("Czy jest to kwota w Euro? (y/n): ").lower().strip() == 'y'

            description = str(input("Podaj opis transakcji: "))

            # pozyskiwanie nowego, najwyższego numeru id
            id = max((t.id for t in self._bc.transactions), default=0) + 1

            transaction = Transaction(id, date, category, amount, description, is_euro)

            self._bc.add_transaction(transaction)
        except ValueError:
            print("Coś poszło nie tak")

        print(f"Transakcja pomyślnie dodana {transaction}")

        str(input("Naciśnij dowolny klawisz aby kontynuować"))

        return

    def _remove_transaction(self):

        if self.__file_not_loaded():
            print("Nie wczytano pliku z budżetem")
            return

        self._budget()

        id_input = int(input("Podaj numer transakcji, którą chcesz usunąć: "))


        self._bc.remove_transaction(id_input)
        print("Transakcja usunięta pomyślnie")



        str(input("Naciśnij dowolny klawisz aby kontynuować"))





    def __file_not_loaded(self):
        return self._bc.transactions is None
