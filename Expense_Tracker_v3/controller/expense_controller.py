class ExpenseController:

    def __init__(self, expenses):
        self.expenses = expenses

    def get_expense_database(self):
        """
        Returns databases in form of dictionary including all expenses for all users. Should be used carefully
        """
        return dict(self.expenses.get_expenses())

    def get_expenses_for_user(self, username):
        """
        Returns a dictionary of all expenses for one user. The keys are expense ids and the values are expense details.
        """
        # dict2 = dict(dict1) makes dict2 a real copy of dict1. It can be modified without risking to modify the DB
        return dict(self.expenses.get_expenses_for_user(username))

    def create_expense(self, username, item_id, date, category, description, price, currency, price_in_eur):
        """
        To insert a new expense for a user
        :param username: username
        :param item_id: id of the expense item
        :param date: date when the expense occurred (chosen by the user)
        :param category: expense category
        :param description: expense description
        :param price: price of the expense
        :param currency: currency in which the price is given
        :param price_in_eur: price converted to euro
        :return: returns nothing
        """
        self.expenses.create_expense(username, item_id, date, category, description, price, currency, price_in_eur)

    def delete_expense(self, username, item_id):
        """Remove an expense item for a user by expense id"""
        self.expenses.delete_expense(username, item_id)

    def total_expenses(self, username):
        """Calculate the sum of all expenses for one user. Returns a float number."""
        sum = 0
        data = self.get_expenses_for_user(username)
        for k, v in data.items():
            sum += float(v["price_in_euro"])
        return round(sum, 2)

    def convert_in_euro(self, price, currency, currency_EUR_dict):
        """
        Convert an expense in a given currency to Euro
        :param price: price that was paid in the original currency
        :param currency: currency in which the price was paid
        :param currency_EUR_dict: dictionary containing the conversion rates from foreign currencies to Euro
        :return: price in Euro (float number)
        """
        EUR_price = float(currency_EUR_dict[currency])*float(price)
        return round(EUR_price, 2)
