import datetime
from models.transaction import Transaction
from utils.serialization_handler import SerializationHandler


class BudgetController:
    def __init__(self):
        self.transactions = None
        self._sh = SerializationHandler("../data/")

    def load_transactions(self, path):
        self._sh = SerializationHandler("../data/"+path)
        self.transactions = self._sh.deserialize()

    def save_transactions(self):
        self._sh.serialize(self._transactions)
        self._transactions = self._sh.deserialize()

    def get_transaction_file_path(self):
        return self._sh.path

    def get_funds(self):

        if self.transactions is None:
            return ""

        pln_sum = 0.0
        eur_sum = 0.0

        for transaction in self.transactions:
            if transaction.is_euro:
                eur_sum += transaction.amount
            else:
                pln_sum += transaction.amount


        return f"{round(pln_sum,2)} PLN, {round(eur_sum,2)} EUR"

    def get_min_amount(self):
        return min(t.amount for t in self.transactions)

    def get_max_amount(self):
        return max(t.amount for t in self.transactions)

    @property
    def transactions(self):
        if self._transactions is None:
            return None
        return self._transactions

    @transactions.setter
    def transactions(self, value):
        self._transactions = value

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        self.save_transactions()

    def remove_transaction(self, id: int):

        if not any(t.id == id for t in self.transactions):
            raise ValueError(f"Transakcja o id {id} nie istnieje")

        self.transactions = [t for t in self.transactions if t.id != id]
        self.save_transactions()

    def edit_transaction(
            self,
            id:int,
            date:datetime,
            category: str,
            amount:float,
            description: str,
            is_euro:bool,
    ):

        transaction = next((t for t in self.transactions if t.id == id), None)

        # walidacja id już zachodzi w widoku, ale w razie czego tutaj też niech będzie
        if transaction is None:
            raise ValueError("Coś poszło nie tak")

        if date is not None:
            transaction.date = date

        if category is not None:
            transaction.category = category

        if amount is not None:
            transaction.amount = amount

        if description is not None:
            transaction.description = description

        if is_euro is not None:
            transaction.is_euro = is_euro

        self.save_transactions()

        return [t for t in self.transactions if t.id == id]




