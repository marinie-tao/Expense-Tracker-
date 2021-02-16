from controller.expense_controller import ExpenseController
from controller.user_controller import UserController
from model.expenses import Expenses
from model.users import Users
from view.login_window import *
from view.main_window import *


if __name__ == "__main__":
    # Create databases
    users = Users()
    expenses = Expenses()

    # Load database content from file
    load_database_from_file(users, expenses)

    # Create controller instances
    user_controller = UserController(users)
    expense_controller = ExpenseController(expenses)

    # Create login windows, other windows are created from there
    login_window = LoginWindow(user_controller, expense_controller)
    login_window.execute()
