import os
import pickle
import re


def center_window(window):
    """Centers a window a little bit above the middle of the screen"""
    window.update_idletasks()
    window.deiconify()

    position_x = int(window.winfo_screenwidth() / 2 - window.winfo_width() / 2)
    position_y = int(window.winfo_screenheight() / 3 - window.winfo_height() / 2)

    # Positions the window in the center of the page.
    window.geometry("+{}+{}".format(position_x, position_y))

def is_float_number(string):
    """
    To check if string is a floating number
    :param string: The string that is checked
    :return: True if string can be casted to float, False if not
    """
    try:
        float(string)
        return True
    except ValueError:
        return False

def valid_email_format(string):
    """Checks if an email has a valid format using a regular expression"""
    # email validation regex from: http://emailregex.com
    regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(regex, string):
        return False
    else:
        return True


def load_database_from_file(users, expenses):
    """Function to load a pickle file into the users and expenses databases (dictionaries)"""
    filename = 'database.pkl'
    if os.path.isfile(filename):  # if file exist in current folder

        with open(filename, 'rb') as f:  # Python 3: open(..., 'rb')
            user_database, expense_database = pickle.load(f)

            users.set_users(user_database)
            expenses.set_expenses(expense_database)

def save_database_to_file(users, expenses):
    """
    Function to save the users and expenses dictionaries to a pickle file.
    This allows to store data even if the application is closed
    """
    with open('database.pkl', 'wb') as f:
        pickle.dump([users, expenses], f)

def budget_pro_rata_temporis(budget, period, grouping):
    """Convert a budget to a different period; e.g. 100€ per month -> 1200€ per year. Used for the statistics."""
    if period == 'per day':
        if grouping == 'weekly':
            budget = budget * 7
        elif grouping == 'monthly':
            budget = budget * 30
        elif grouping == 'yearly':
            budget = budget * 365
    elif period == 'per week':
        if grouping == 'daily':
            budget = budget / 7
        elif grouping == 'monthly':
            budget = budget * 30 / 7
        elif grouping == 'yearly':
            budget = budget * 52
    elif period == 'per month':
        if grouping == 'daily':
            budget = budget / 30
        elif grouping == 'weekly':
            budget = budget / (30 / 7)
        elif grouping == 'yearly':
            budget = budget * 12
    elif period == 'per year':
        if grouping == 'daily':
            budget = budget / 365
        elif grouping == 'weekly':
            budget = budget / 52
        elif grouping == 'monthly':
            budget = budget / 12
    return budget
