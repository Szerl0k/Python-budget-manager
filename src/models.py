from datetime import datetime

CATEGORIES = [
    "Zywnosc",
    "Transport",
    "Rozrywka",
    "Mieszkanie",
    "Pensja",
    "Restauracja",
    "Samochod",
    "Inne"
]

class Transaction:
    def __init__(self, id: int, date: datetime, category, amount: float, description: str):
        self.id = id
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

    def __str__(self):
        return f"{self.id} {self.date} {self.category} {self.amount} {self.description}"


    @classmethod
    def from_json(cls, j: dict):
        id = int(j["id"])
        date = datetime.strptime(j["date"], "%Y-%m-%d")
        category = j["category"]
        amount = float(j["amount"])
        description = j["description"]

        return cls(id, date, category, amount, description)


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if value < 0:
            raise ValueError('Id must be positive')
        self._id = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value not in CATEGORIES:
            raise ValueError('Category must be one of: ' + str(CATEGORIES))
        self._category = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.strftime("%Y-%m-%d"),
            "category": self.category,
            "amount": self.amount,
            "description": self.description
        }




class BudgetManager:
    def __init__(self, data: list):
        self.transactions = data

    @property
    def transactions(self):
        return self._transactions

    @transactions.setter
    def transactions(self, value):
        self._transactions = value

    def add_transaction(self, transaction: Transaction):
        self.transactions[transaction.id] = transaction

    def remove_transaction(self, id: int):
        self.transactions.pop(id)

    def edit_transaction(self,transaction: Transaction):
        if self.transactions.__contains__(transaction.id):
            self.transactions[transaction.id] = transaction



class ReportManager:
    def __init__(self, budget: BudgetManager):
        self._budget = budget
        self._transactions = self._budget.transactions

    def get_monthly_report(self, month: int, year: int):
        result = dict()
        for k,v in self._transactions.items():
            if v.date.month == month and v.date.year == year:
                result[k] = v

        return result

    def get_yearly_report(self, year: int):
        result = dict()
        for k,v in self._transactions.items():
            if v.date.year == year:
                result[k] = v

        return result



