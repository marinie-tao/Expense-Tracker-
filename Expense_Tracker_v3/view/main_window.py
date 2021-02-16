"""
Gui interface with tkinter inspired from:
https://www.sharptutorial.com/login-page-using-tkinter/

# for the table
https://www.askpython.com/python-modules/tkinter/tkinter-treeview-widget
"""

from tkinter import *
from tkinter import ttk

from util import *
from view.expense_tab import ExpenseTab
from view.preferences_tab import PreferencesTab
from view.statistics_tab import StatisticsTab
from view.user_tab import UserTab


class MainWindow:

    def __init__(self, user_controller, expense_controller, username, login_window):
        """Initializes the main window, which is a 'frame' for the different tabs."""
        # Class used for in the windows
        self.user_controller = user_controller
        self.expense_controller = expense_controller
        self.username = username

        self.window = Toplevel(login_window)
        self.window.title("Expense Tracker")
        self.window.withdraw()

        # CREATE TAB CONTROL
        tab_parent = ttk.Notebook(self.window)
        expense_tab = ExpenseTab(tab_parent, self.expense_controller, self.user_controller, self.username)
        UserTab(self, tab_parent, self.username, self.user_controller)
        PreferencesTab(tab_parent, self.username, self.user_controller, expense_tab)
        StatisticsTab(tab_parent, self.expense_controller, self.user_controller, self.username)
        # https://www.homeandlearn.uk/python-database-form-tabs2.html
        # The expand and fill option between pack ensure that the tabs fill the entire tab window
        tab_parent.pack(expand=1, fill="both")

        center_window(self.window)

        # This function is called when clicking the cross button to close the window
        self.window.protocol("WM_DELETE_WINDOW", self.close_main_window)

    def close_main_window(self):
        """Triggers saving of all data to the database and then destroys the main window = logs the user out"""
        # withdraw window first in order to prevent strange visual effects, because saving data takes quite some time
        self.window.withdraw()
        # then save data
        save_database_to_file(self.user_controller.get_user_database(),
                              self.expense_controller.get_expense_database())
        # then destroy the window
        self.window.destroy()
