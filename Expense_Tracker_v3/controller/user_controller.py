import hashlib
import binascii
import os

from util import valid_email_format, is_float_number


def check_password(password):
    """
    Checks if a password fulfils the required constraints: only alphanumerical characters and at least 6 characters.
    """
    # security in password (more than 6 characters)
    if len(password) < 6:
        return False, "Password should contain at least 6 characters."

    # Check if password contains only alphanumerical character (a-z, A-Z and 0-9)
    if not password.isalnum():
        return False, "Password should contain only alphanumerical characters (a-z, A-Z and 0-9)"

    return True, "Correct password format"

def check_user_info(firstname, lastname, email):
    """
    Checks if user information (Firstname, Lastname, Email) fulfils the required constraints
    """
    if not all(x.isalpha() or x.isspace() for x in firstname):
        return False, "Firstname should contain only letters and spaces"

    if not all(x.isalpha() or x.isspace() for x in lastname):
        return False, "Lastname should contain only letters and spaces"

    if email and not valid_email_format(email):
        return False, "Invalid email"

    return True, "Correct user info format"

def hash_password(password):
    """
    Hashes a password for storing in the database using sha256 standard
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """
    Verifies a stored, hashed password against one provided by user
    """
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


class UserController:

    def __init__(self, users):
        self.users = users

    def get_user_database(self):
        """
        Returns databases in form of dictionary containing all users and their information. Should be used carefully.
        """
        return dict(self.users.get_users())

    def get_user(self, username):
        """Returns all information for one user"""
        return dict(self.users.get_user(username))

    def create_account(self, username, password, firstname=None, lastname=None, email=None):
        """
        Creates a new user instance in the database/dictionary.
        Returns True/False to indicate success or failure and a message as result
        """
        # with .isalnum(): Check if password contains only alphanumerical character (a-z, A-Z and 0-9)
        if not username.isalnum():
            return False, "Username should contain only alphanumerical characters (a-z, A-Z and 0-9)"

        success, message = check_password(password)
        if not success:
            return success, message

        success, message = check_user_info(firstname, lastname, email)
        if not success:
            return success, message

        pw_hash = hash_password(password)

        # if all sanity checks above are passed, username and password are sent to the database for account creation
        return self.users.create_user(username, pw_hash, firstname, lastname, email)

    def login(self, username, password):
        """
        Checks if a username exists and if the provided password is correct.
        Returns True/False to indicate success or failure and a message as result
        """
        # check directly with database if credentials are correct
        success, message = self.users.get_password(username)
        if success:
            stored_pw_hash = message
            if verify_password(stored_pw_hash, password):
                return True, 'Login successful!'
            else:
                return False, 'Password incorrect!'
        else:
            return success, message

    def edit_user(self, username, firstname, lastname, email):
        """
        Modifies the information (firstname, lastname, email) for one user.
        Returns True/False to indicate success or failure and a message as result
        """
        success, message = check_user_info(firstname, lastname, email)
        if not success:
            return success, message

        return self.users.edit_user(username, firstname, lastname, email)

    def edit_password(self, username, password):
        """
        Modifies the password for one user. The new password is hashed before stored to database.
        Returns True/False to indicate success or failure and a message as result
        """
        success, message = check_password(password)
        if not success:
            return success, message

        pw_hash = hash_password(password)
        return self.users.set_new_password(username, pw_hash)

    def set_categories(self, username, category_list):
        """Sets a customized list of categories for one user"""
        self.users.set_custom_categories(username, category_list)

    def get_categories(self, username):
        """
        Loads the (customized) list of categories for one user.
        Returns True/False to indicate success or failure and a message as result
        """
        return self.users.get_custom_categories(username)

    def set_budget(self, username, budget, period):
        """
        Sets or removes a budget (including sum and period over which the budget should be set) for a user
        :param username: username
        :param budget: Float value indicating the amount of money that should not be exceeded. In Euro. E.g. 50
        :param period: String value indicating the amount of time over which the budget should not be exceeded.
        E.g. 'per week'
        :return: True/False to indicate success or failure and a message as result
        """
        budget = budget.replace(',', '.')
        if is_float_number(budget):
            return self.users.set_budget(username, budget, period)
        elif budget == '':
            _, _ = self.users.set_budget(username, '', '')
            return True, 'Budget has been removed'
        else:
            return False, 'Budget should be a float number'

    def get_budget(self, username):
        """Returns the budget (float number) and the period over which it counts (string) for a user as a tuple"""
        return self.users.get_budget(username)
