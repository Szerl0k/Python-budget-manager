from datetime import datetime

CATEGORIES = [
    "Zywnosc",
    "Transport",
    "Rozrywka",
    "Mieszkanie",
    "Wynagrodzenie",
    "Restauracja",
    "Samochod",
    "Inne"
]

class Transaction:
    def __init__(self, id: int, date: datetime, category, amount: float, description: str, is_euro: bool):
        self.id = id
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description
        self.is_euro = is_euro

    def __str__(self):
        return f"""
Transaction {self.id}
date: {self.date}, category: "{self.category}" amount: {self.amount} {self.currency_suffix()}
description: 
{self.description}
"""

    def currency_suffix(self) -> str:
        if self.is_euro:
            return "EUR"
        return "PLN"

    def __repr__(self):
        return self.__str__()


    @classmethod
    def from_json(cls, j: dict):
        id = int(j["id"])
        date = datetime.strptime(j["date"], "%Y-%m-%d")
        category = j["category"]
        amount = float(j["amount"])
        description = j["description"]
        is_euro = j["is_euro"]

        return cls(id, date, category, amount, description, is_euro)


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value: int):
        if value < 0:
            raise ValueError('Id must be positive')
        self._id = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value: datetime):
        self._date = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value: str):
        if value not in CATEGORIES:
            raise ValueError('Category must be one of: ' + str(CATEGORIES))
        self._category = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value: float):
        self._amount = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def is_euro(self):
        return self._is_euro

    @is_euro.setter
    def is_euro(self, value: bool):
        self._is_euro = value

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.strftime("%Y-%m-%d"),
            "category": self.category,
            "amount": self.amount,
            "description": self.description,
            "is_euro": self.is_euro
        }
