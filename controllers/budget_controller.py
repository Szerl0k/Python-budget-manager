from models.transaction import Transaction
from utils.serialization_handler import SerializationHandler


class BudgetController:
    def __init__(self):
        self.transactions = None
        self._sh = SerializationHandler()

    def load_transactions(self, path):
        self._sh.path = path
        self.transactions = self._sh.deserialize()

    def save_transactions(self):
        self._sh.serialize(self.transactions)

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

    @property
    def transactions(self):
        return self._transactions

    @transactions.setter
    def transactions(self, value):
        self._transactions = value

    def add_transaction(self, transaction: Transaction):
        self.transactions[transaction.id] = transaction
        self.save_transactions()

    def remove_transaction(self, id: int):
        self.transactions.pop(id)
        self.save_transactions()

    def edit_transaction(self,transaction: Transaction):
        if self.transactions.__contains__(transaction.id):
            self.transactions[transaction.id] = transaction

        self.save_transactions()




