import os
from datetime import datetime

from controllers.budget_controller import BudgetController
from controllers.filter_controller import TransactionFilter, filter_controller
from controllers.report_controller import generate_report
from models.transaction import CATEGORIES, Transaction
from utils.serialization_handler import SerializationHandler
from utils.data_generator import generate_example_json


def _debug_create_test_data():
    generate_example_json(count=100)
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
            user_input = str(input())


            match user_input:
                case '1':
                    self._load_budget()

                case '2':
                    self._budget()

                case '3':
                    self._add_transaction()

                case '4':
                    self._remove_transaction()

                case '5':
                    self._edit_transaction()

                case '6':
                    self._filer_transactions()

                case '99':
                    _debug_create_test_data()

                case '0':
                    break

                case _:
                    print("")


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
[5] Edytuj transakcje
[6] Filtruj transakcje

[99] Wygeneruj testowy budżet (debug)
[0] Wyjdź
"""

        print(menu)

    def _load_budget(self):

        files_str = [filename for filename in os.listdir("../data")]
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


    def _edit_transaction(self):

        if self.__file_not_loaded():
            print("Nie wczytano pliku z budżetem")
            return

        self._budget()

        id_input = int(input("Podaj numer transakcji, którą chcesz edytować: "))

        transaction = [t for t in self._bc.transactions if t.id == id_input]

        if transaction is None:
            print("Nieprawidłowy numer transakcji")
            str(input("Naciśnij dowolny klawisz aby kontynuować"))
            return

        print(transaction)

        date = None
        category_input = None
        amount_input = None
        description_input = None

        if input("Czy chcesz edytować datę? (y/n): ").lower().strip() == 'y':
            date_input = str(input("Podaj datę w formacie YYYY-MM-DD: "))
            year, month, day = map(int, date_input.split('-'))
            date = datetime(year, month, day)

        if input("Czy chcesz edytować kategorię? (y/n): ").lower().strip() == 'y':
            category_input = str(input("Podaj kategorię: "))
            if category_input not in CATEGORIES:
                category_input = "Inne"

        is_euro = None
        if input("Czy chcesz edytować kwotę? (y/n): ").lower().strip() == 'y':
            amount_input = float(input("Podaj kwotę transakcji: "))
            amount_input = round(amount_input, 2)

            is_euro = input("Czy jest to kwota w Euro? (y/n): ").lower().strip() == 'y'

        if input("Czy chcesz edytować opis? (y/n): ").lower().strip() == 'y':
            description_input = str(input("Podaj opis transakcji: "))

        result = self._bc.edit_transaction(
            id = id_input,
            date = date,
            category = category_input,
            amount = amount_input,
            description = description_input,
            is_euro = is_euro,
        )

        print("Wynik")
        print(result)


    def _filer_transactions(self):
        if self.__file_not_loaded():
            print("Nie wczytano pliku z budżetem")
            return

        print("Wybierz filtry do zastosowania: ")

        t_filter = self.__ask_user_for_filters()

        try:
            result = filter_controller(self._bc, t_filter)
            print(result)

            if input("Zapisać jako raport? (y/n): ").lower().strip() == 'y':
                path = self._bc.get_transaction_file_path()
                base = os.path.basename(path)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                default_report_name = f"{base}_{timestamp}.rep"
                report_name = str(input("Podaj nazwę raportu "))

                if report_name == "":
                    report_name = default_report_name

                generate_report(result, report_name)

        except ValueError as e:
            print(e)
            return





    def __ask_user_for_filters(self) -> TransactionFilter:
        t_filter = TransactionFilter()


        t_filter.by_euro = str(input("y - tylko EURO, n - tylko PLN: ")).lower().strip() == 'y'

        budget_min = self._bc.get_min_amount()
        budget_max = self._bc.get_max_amount()

        amount_min = str(input(f"Dolny zakres kwoty, minimum {budget_min}: "))
        amount_max = str(input(f"Górny zakres kwoty, maksimum: {budget_max}: "))


        if amount_min == "":
            t_filter.amount_min = budget_min
        else:
            t_filter.amount_min = round(float(amount_min),2)

        if amount_max == "":
            t_filter.amount_max = budget_max
        else:
            t_filter.amount_max = round(float(amount_max),2)


        if input("Po kategorii? (y/n): ").lower().strip() == 'y':
            t_filter.by_category = str(input("Podaj nazwę kategorii "))
            return t_filter


        if input("Po dacie? (y/n): ").lower().strip() == 'y':
            if input("y - rosnąco, n - malejąco (y/n): ".lower().strip()) == 'y':
                t_filter.by_date = "desc"
            else:
                t_filter.by_date = "asc"

            return t_filter


        if input("Kwota: y - rosnąco, n - malejąco (y/n): ".lower().strip()) == 'y':
            t_filter.amount_order = "desc"
        else:
            t_filter.amount_order = "asc"

        return t_filter




    def __file_not_loaded(self):
        return self._bc.transactions is None
