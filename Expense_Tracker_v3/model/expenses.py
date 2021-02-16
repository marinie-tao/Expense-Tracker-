class Expenses:
    # form of the database table:
    # dictionary that holds many dictionaries per user. One for every expense.
    # user_id is key of the outer dictionary and item_id key of the inner dictionaries; values are the expense infos
    # database['username']['id_item']  = {'date': ...,
    #                                     'price': ...,
    #                                      ...}

    def __init__(self):
        self.database = {}

    def set_expenses(self, database_input):
        """Fills expense dictionary (self.database) with input data (e.g. at application start from pickle file)"""
        self.database = database_input

    def get_expenses(self):
        """Returns entire expense dictionary (self.database) for all users (e.g. for saving to pickle file)"""
        return self.database

    def get_expenses_for_user(self, username):
        """Returns database for a specific user. Returns empty dict if user doesn't exist"""
        if username in self.database:
            return self.database[username]
        else:
            return {}

    def create_expense(self, username, id_item, date, category, description, price, currency, price_in_euro):
        """Writes a new expense item for one user to the dictionary"""
        if username not in self.database:
            # If it is the first expense that the user creates, the username is not as a key in the database.
            # Therefore, check first if the username already exists, if not, add it as a key.
            self.database[username] = {}
        # First create the key containing the item id, then fill all values at that key (date, category, ...)
        self.database[username][id_item] = {}
        self.database[username][id_item]["date"] = date
        self.database[username][id_item]["category"] = category
        self.database[username][id_item]["description"] = description
        self.database[username][id_item]["price"] = price
        self.database[username][id_item]["currency"] = currency
        self.database[username][id_item]["price_in_euro"] = price_in_euro

    def delete_expense(self, username, id_item):
        """Deletes an expense item for one user (by expense item id)"""
        # look if the key "id_item" is inside the dictionary first
        if id_item in self.database[username]:
            # delete the key from the dictionary
            del self.database[username][id_item]
