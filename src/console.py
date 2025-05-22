import os

from controllers.budget_controller import BudgetController
from utils.serialization_handler import SerializationHandler


class Console:
    header = "---- [ MANAGER BUDŻETU ] ----"
    def __init__(self):
        self._bc = BudgetController()

    def run(self):
        self.__main_loop()

    def __main_loop(self):
        user_input = 1

        while user_input != 0:
            self.__print_main_menu()
            user_input = int(input())

            match user_input:
                case 1:
                    self.__print_load_budget()
                    user_input = str(input())
                    self._bc.load_transactions(user_input)

                case 2:
                    self.__print_budget()
                    input()


            os.system('cls')

    def __print_main_menu(self):
        menu = f"""
{self.header}
Działasz na pliku budżetowym: {self._bc.get_transaction_file_path()}
Dostępne środki {self._bc.get_funds()}
[1] Wczytaj budżet
[2] Wyświetl budżet


[0] Wyjdź
"""

        print(menu)

    def __print_load_budget(self):

        files_str = [filename for filename in os.listdir("data")]
        s = f"""
{self.header}
Dostępne pliki:
{files_str}

Podaj nazwę pliku:
"""
        print(s)

    def __print_budget(self):
        transactions_str = self._bc.transactions
        if transactions_str is None:
            transactions_str = "Nie wczytano pliku z budżetem"
        s = f"""
{self.header}
Transakcje:
{transactions_str}

Naciśnij dowolny klawisz aby kontynuować
"""
        print(s)