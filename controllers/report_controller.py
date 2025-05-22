from controllers.budget_controller import BudgetController

class ReportService:
    def __init__(self, budget: BudgetController):
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
