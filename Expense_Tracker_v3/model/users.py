class Users:
    # form of the database table:
    # dictionary that holds one dictionary per user
    # userid is key and values are password, firstname, lastname and email address
    # self.database[username] = {'password': ...,
    #                            'firstname': ...,
    #                             ...}

    def __init__(self):
        self.database = {}

    def set_users(self, database_input):
        """Fills user dictionary (self.database) with input data (e.g. at application start from pickle file)"""
        self.database = database_input

    def get_users(self):
        """Returns entire user dictionary (self.database) (e.g. for saving to pickle file)"""
        return dict(self.database)

    def get_user(self, username):
        """Returns information for one user (by username)"""
        return dict(self.database[username])

    def edit_user(self, username, firstname, lastname, email):
        """
        Updates the information for one user in the dictionary.
        Returns True/False to indicate success or failure and a message as result
        """
        try:
            self.database[username]["firstname"] = firstname
            self.database[username]["lastname"] = lastname
            self.database[username]["email"] = email
            return True, "Information successfully changed!"
        except Exception as e:
            return False, f"Database error: {e}"

    def create_user(self, username, password, firstname=None, lastname=None, email=None):
        """
        Creates a new user element in the dictionary. Checks first if user already exists.
        :param username: String: the username that was chosen
        :param password: String: the password, already hashed
        :param firstname: String: First name
        :param lastname: String: Last name
        :param email: String: Email address
        :return: True/False to indicate success or failure and a message as result
        """
        # check if username already exist
        if username in self.database:
            return False, "This username already exists, please choose a different one."

        try:
            self.database[username] = {}
            self.database[username]["password"] = password
            self.database[username]["firstname"] = firstname
            self.database[username]["lastname"] = lastname
            self.database[username]["email"] = email
            self.database[username]["categories"] = ["Transportation", "Food", "Taxes & Bills", "Home", "Health",
                                                     "School", "Travel", "Entertainment", "Pets", "Other Shopping",
                                                     "Gifts"]
            return True, "Account successfully created!"
        except Exception as e:
            return False, f"Database error: {e}"

    def get_password(self, username):
        """
        Returns the hashed password for a user, in order to verify it at the controller level.
        If username doesn't exist, it returns False and a message instead
        """
        # Check if the username is inside the database
        if username in self.database:
            return True, self.database[username]['password']
        else:
            return False, "This username does not exist!"

    def set_new_password(self, username, password):
        """
        Changes the password of a user in the dictionary.
        Returns True/False to indicate success or failure and a message as result
        """
        try:
            self.database[username]['password'] = password
            return True, "Password successfully changed!"
        except Exception as e:
            return False, f"Database error: {e}"

    def set_custom_categories(self, username, category_list):
        """Sets a list of customized categories for a user"""
        self.database[username]['categories'] = category_list

    def get_custom_categories(self, username):
        """Returns either a list of customized categories for a user or an empty list, if there is no customized list"""
        try:
            return self.database[username]['categories']
        except KeyError:
            return []

    def set_budget(self, username, budget, period):
        """
        Sets or removes a budget (including sum and period over which the budget should be set) for a user.
        Returns True/False to indicate success or failure and a message as result.
        """
        try:
            self.database[username]['budget'] = budget
            self.database[username]['budget_period'] = period
            return True, "Budget successfully saved!"
        except Exception as e:
            return False, f"Database error: {e}"

    def get_budget(self, username):
        """
        Returns the budget (float) and the period over which it is valid (string) for one user.
        If this information is not available, returns two empty strings.
        """
        try:
            return self.database[username]['budget'], self.database[username]['budget_period']
        except KeyError:
            return "", ""
