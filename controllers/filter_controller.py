from controllers.budget_controller import BudgetController
from models.transaction import CATEGORIES


class TransactionFilter:
    # Oczekiwane parametry:
    # by_date: None/"desc"/"asc"
    # by_category: None/{nazwa kategorii}
    # amount_min: float
    # amount_max: float
    # amount_order: "desc"/"asc"
    # by_euro: True/False
    def __init__(self):
        self.by_date = None
        self.by_category = None
        self.amount_min = None
        self.amount_max = None
        self.amount_order = None
        self.by_euro = None


def apply_filter_by_date(order):
    def decorator(func):
        def wrapper(transactions: list):
            reverse = (order == 'desc')
            result = sorted(transactions, key=lambda t: t.date, reverse=reverse)
            return func(result)
        return wrapper
    return decorator

def apply_filter_by_category(category):
    def decorator(func):
        def wrapper(transactions: list):
            result = [t for t in transactions if t.category == category]
            return func(result)
        return wrapper
    return decorator

def apply_filter_by_amount(min_amount, max_amount, order):
    def decorator(func):
        def wrapper(transactions: list):
            result = [
                t for t in transactions
                if (t.amount >= min_amount)
                and (t.amount <= max_amount)
            ]
            if order is not None:
                reverse = (order == 'desc')
                result = sorted(result, key=lambda t: t.amount, reverse=reverse)
            return func(result)
        return wrapper
    return decorator

def apply_filter_by_currency(is_euro):
    def decorator(func):
        def wrapper(transactions: list):
            result = [
                t for t in transactions
                if t.is_euro == is_euro
            ]
            return func(result)
        return wrapper
    return decorator

def apply(transactions: list) -> list:
    return transactions


def filter_controller(budget_controller: BudgetController, t_filter: TransactionFilter) -> list:

    # walidacja kategorii czy jest w CATEGORIES


    decorators = []

    if t_filter.by_euro is not None:

        decorators.append(apply_filter_by_currency(
            is_euro=t_filter.by_euro
        ))

    decorators.append(apply_filter_by_amount(
        t_filter.amount_min, t_filter.amount_max, t_filter.amount_order
    ))

    if t_filter.by_category is not None:
        if t_filter.by_category not in CATEGORIES:
            raise ValueError(f"{t_filter.by_category} is not a valid category")

        decorators.append(apply_filter_by_category(
            category=t_filter.by_category
        ))



    if t_filter.by_date is not None:
        decorators.append(apply_filter_by_date(
            order=t_filter.by_date
        ))


    transactions = budget_controller.transactions

    func = apply

    for decorator in reversed(decorators):
        func = decorator(func)

    return func(transactions)