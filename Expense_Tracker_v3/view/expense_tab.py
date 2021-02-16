from datetime import datetime, timedelta, date
from tkinter import StringVar, ttk, messagebox
from tkinter.ttk import Label, Entry, Button, OptionMenu, Style, Scrollbar
from tkcalendar import DateEntry
import requests

from util import is_float_number


class ExpenseTab:

    # Use for option selection for currency
    currency_code_list = ['AUD', 'CAD', 'CHF', 'CNY', 'DKK', 'EUR', 'GBP', 'INR', 'JPY', 'LBP', 'NOK', 'NZD',
                          'MAD', 'USD', 'SEK', 'TND']

    convert_to_EUR = [0.62, 0.65, 0.93, 0.13, 0.13, 1, 1.11, 0.011, 0.008, 0.00056, 0.094, 0.58, 0.092, 0.85,
                      0.098, 0.31]

    def __init__(self, tab_control, expense_controller, user_controller, username):
        """Initializes the expense tab and creates all elements of the visual interface"""
        # Input for the expense interface
        self.expense_controller = expense_controller
        self.user_controller = user_controller
        self.username = username

        self.category_list = self.user_controller.get_categories(self.username)

        self.chosen_currency = StringVar()
        self.chosen_category = StringVar()
        self.description = StringVar()
        self.price = StringVar()
        self.price_in_euro = StringVar()
        self.date = StringVar()

        self.currency_EUR_dict = {self.currency_code_list[i]: self.convert_to_EUR[i]
                                  for i in range(len(self.currency_code_list))}

        try:
            # try to load latest currency conversion codes through an API
            response = requests.get('https://api.ratesapi.io/api/latest')
            for c in self.currency_code_list:
                try:
                    # try to load conversion rate for specific currency
                    self.currency_EUR_dict[c] = 1/response.json()['rates'][c]
                except KeyError:
                    # if not available (e.g. LBP) the hard-coded conversion rate is used
                    pass
        except requests.exceptions.RequestException as e:
            # if no internet connection is available or the server is down, hard-coded conversion rates are used
            print(e)

        self.id_expenseItem = 0
        total = self.expense_controller.total_expenses(self.username)
        self.sum_expenses = StringVar(value=f"Sum of all expenses: {total}€")
        self.budget_message = StringVar()

        self.expense_tab = ttk.Frame(tab_control)
        tab_control.add(self.expense_tab, text='Expenses')

        Label(self.expense_tab, text="New expense:", font='Helvetica 16 bold').grid(row=0, column=0, padx=15,
                                                                                    pady=15, sticky='w')

        # DESCRIPTION
        Label(self.expense_tab, text="Description:").grid(row=1, column=0, padx=(15, 0), pady=2, sticky='w')
        Entry(self.expense_tab, textvariable=self.description).grid(row=1, column=1, pady=2, sticky="ew")

        # CATEGORY
        Label(self.expense_tab, text="Category:").grid(row=1, column=2, pady=2)
        self.category_select = OptionMenu(self.expense_tab, self.chosen_category, self.category_list[0],
                                          *self.category_list)
        self.category_select.grid(row=1, column=3, padx=(0, 15), pady=2, sticky="ew")

        # PRICE
        Label(self.expense_tab, text="Price:").grid(row=2, column=0, padx=(15, 0), pady=2, sticky='w')
        Entry(self.expense_tab, textvariable=self.price).grid(row=2, column=1, pady=2, sticky="ew")

        # CURRENCY OPTION
        Label(self.expense_tab, text="Currency:").grid(row=2, column=2, pady=2)
        OptionMenu(self.expense_tab, self.chosen_currency, self.currency_code_list[5], *self.currency_code_list)\
            .grid(row=2, column=3, padx=(0, 15), pady=2, sticky="ew")

        # DATE
        Label(self.expense_tab, text="Date:").grid(row=3, column=0, padx=(15, 0), pady=2, sticky='w')
        DateEntry(self.expense_tab, background='darkblue', foreground='white', borderwidth=2,
                  textvariable=self.date, date_pattern='dd/MM/yyyy').grid(row=3, column=1, pady=2, sticky="ew")

        # INSERT BUTTON
        Button(self.expense_tab, text="Insert", command=self.insert_expense_data).grid(row=4, column=1, pady=2,
                                                                                       sticky="ew")

        Label(self.expense_tab, text="Your expenses:", font='Helvetica 16 bold').grid(row=5, column=0, padx=15, pady=15,
                                                                                      sticky='w')

        # TOTAL EXPENSE
        Label(self.expense_tab, textvariable=self.sum_expenses).grid(row=6, column=0, padx=(15, 0), sticky='w')

        # BUDGET DIFFERENCE
        self.budgetLabel = Label(self.expense_tab, textvariable=self.budget_message)
        self.budgetLabel.grid(row=7, column=0, columnspan=2, padx=(15, 0), sticky='w')
        # set budget difference value
        budget_message = self.calculate_budget_level()
        self.budget_message.set(budget_message)

        # TREEVIEW WITH SCROLLBAR
        y_scroll = Scrollbar(self.expense_tab, orient='vertical')
        y_scroll.grid(row=8, column=5, padx=(0, 15), pady=(40, 15), sticky='nsw')
        self.treeExpense = ttk.Treeview(self.expense_tab,
                                        columns=('Date',
                                                 'Category',
                                                 'Description',
                                                 'Price',
                                                 'Currency',
                                                 'Price in EUR'),
                                        yscrollcommand=y_scroll.set,
                                        height=20)
        y_scroll['command'] = self.treeExpense.yview
        self.treeExpense.grid(row=8, column=0, columnspan=5, padx=(15, 0), pady=15)

        # Set the treeview columns
        self.treeExpense.heading('#0', text='Item Id')
        self.treeExpense.column("#0", minwidth=0, width=0)

        self.treeExpense.heading('#1', text='Date')
        self.treeExpense.column("#1", minwidth=0, width=120)

        self.treeExpense.heading('#2', text='Category')
        self.treeExpense.column("#2", minwidth=0, width=280)

        self.treeExpense.heading('#3', text='Description')
        self.treeExpense.column("#3", minwidth=0, width=280)

        self.treeExpense.heading('#4', text='Price')
        self.treeExpense.column("#4", minwidth=0, width=100)

        self.treeExpense.heading('#5', text='Currency')
        self.treeExpense.column("#5", minwidth=0, width=100)

        self.treeExpense.heading('#6', text='Price in EUR')
        self.treeExpense.column("#6", minwidth=0, width=100)

        # Restore display in table from the expense database
        self.update_treeview_from_existing_database()

        # DELETE BUTTON
        # Configure delete button style to be red
        style = Style()
        style.configure('W.TButton', foreground='red')
        Button(self.expense_tab, text="Delete", style='W.TButton', command=self.delete_expense_data).grid(row=9,
                                                                                                          column=4,
                                                                                                          padx=15,
                                                                                                          sticky="e")

        # SORT THE PRICE: CALL FUNCTION
        col1 = "Price"
        col2 = "Price in EUR"
        col3 = "Date"
        self.treeExpense.heading(col1, text=col1, command=lambda: self.treeview_sort_price(col1, False))
        self.treeExpense.heading(col2, text=col2, command=lambda: self.treeview_sort_price(col2, False))

        # SORT THE DATE: CALL FUNCTION
        self.treeExpense.heading(col3, text=col3, command=lambda s=col3: self.treeview_sort_date(col3, False))

    def update_treeview_from_existing_database(self):
        """If the database of expenses already exist for this username, display it back into the treeview"""

        database = self.expense_controller.get_expenses_for_user(self.username)

        for id_item in database:
            self.treeExpense.insert('', 0, id_item,
                                    values=(database[id_item]["date"], database[id_item]["category"],
                                            database[id_item]["description"], database[id_item]["price"],
                                            database[id_item]["currency"], database[id_item]["price_in_euro"]))
            self.id_expenseItem = id_item

    def insert_expense_data(self):
        """
        Add a new expense item both to the treeview and to the database. Then update the sum of all expenses and the
        budget difference.
        This function is called when clicking the 'Insert' button
        """
        currency = self.chosen_currency.get()
        category = self.chosen_category.get()
        description = self.description.get()
        price = self.price.get()
        expense_date = self.date.get()

        # replace comma with point in order to make it possible to cast to float
        price = price.replace(',', '.')
        # Check if it is numeric
        if not is_float_number(price):
            messagebox.showerror("INPUT ERROR", "The price must be a (floating) number")
        else:
            self.id_expenseItem = self.id_expenseItem + 1
            price = float(price)
            price_in_euro = self.expense_controller.convert_in_euro(price, currency, self.currency_EUR_dict)

            # display into the Expense gui table
            # https://www.askpython.com/python-modules/tkinter/tkinter-treeview-widget
            self.treeExpense.insert('', 0, self.id_expenseItem,
                                    values=(expense_date,
                                            category,
                                            description,
                                            price,
                                            currency,
                                            price_in_euro))

            # update the expense database through expense controller
            self.expense_controller.create_expense(self.username,
                                                   self.id_expenseItem,
                                                   expense_date,
                                                   category,
                                                   description,
                                                   price,
                                                   currency,
                                                   price_in_euro)
        total = self.expense_controller.total_expenses(self.username)
        self.sum_expenses.set(f"Sum of all expenses: {total}€")
        budget_message = self.calculate_budget_level()
        self.budget_message.set(budget_message)

    def delete_expense_data(self):
        """
        Remove the selected item from the treeview and the database, then update the sum of all expenses and the
        budget difference.
        This function is called when clicking the 'Delete' button
        """
        try:
            id_expense_selected = int(self.treeExpense.focus())
            self.treeExpense.delete(id_expense_selected)
            # remove the selected expense id in the database as well
            self.expense_controller.delete_expense(self.username, id_expense_selected)
        except ValueError:
            messagebox.showerror("Delete Error", "Select an item to be deleted")
        total = self.expense_controller.total_expenses(self.username)
        self.sum_expenses.set(f"Sum of all expenses: {total}€")
        budget_message = self.calculate_budget_level()
        self.budget_message.set(budget_message)

    def refresh_categories(self, category_list):
        """Refresh the category drop-down menu. This is called after configuring categories in the preferences"""
        self.category_list = category_list
        self.category_select = OptionMenu(self.expense_tab, self.chosen_category, self.category_list[0],
                                          *self.category_list)
        self.category_select.grid(row=1, column=3, pady=5, sticky="ew")

    def treeview_sort_price(self, col, reverse: bool):
        """Sort the table by price when clicking on the price column"""
        data_list = [(float(self.treeExpense.set(k, col)), k) for k in self.treeExpense.get_children("")]
        data_list.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(data_list):
            self.treeExpense.move(k, "", index)

        # reverse sort next time
        self.treeExpense.heading(
            column=col,
            text=col,
            command=lambda _col=col: self.treeview_sort_price(
               _col, not reverse
            ),
        )

    def treeview_sort_date(self, date_col, reverse):
        """Sort the table by date when clicking on the date column"""
        l = [(self.treeExpense.set(k, date_col), k) for k in self.treeExpense.get_children('')]

        sortedArray = sorted(l, key=lambda x_lab: datetime.strptime(x_lab[0], '%d/%m/%Y'), reverse=not reverse)

        for index, (val, k) in enumerate(sortedArray):
            self.treeExpense.move(k, '', index)

        self.treeExpense.heading(
            column=date_col,
            text=date_col,
            command=lambda _date_col=date_col: self.treeview_sort_date(
               _date_col, not reverse
            ),
        )

    def calculate_budget_level(self):
        """
        Calculates whether the custom budget (in preferences) is already exceeded or not and generate a message to
        display.
        """
        budget = self.user_controller.get_budget(self.username)
        if budget[0]:
            today = date.today()
            if budget[1] == 'per day':
                start_date = today
            elif budget[1] == 'per week':
                start_date = today - timedelta(days=today.weekday())
            elif budget[1] == 'per month':
                start_date = today.replace(day=1)
            elif budget[1] == 'per year':
                start_date = today.replace(month=1).replace(day=1)
            expenses = self.expense_controller.get_expenses_for_user(self.username)
            delete = []
            for k, v in expenses.items():
                if datetime.date(datetime.strptime(v['date'], '%d/%m/%Y')) < start_date:
                    delete.append(k)
            # we cannot delete items from dictionary while iterating the dict, therefore we store indices to delete in
            # list and delete the corresponding elements later
            for k in delete:
                del expenses[k]
            total = sum([e['price_in_euro'] for e in expenses.values()])
            difference = round((float(budget[0]) - total), 2)
            if difference > 0:
                message = f'You have {difference}€ left from your budget which is {budget[0]}€ {budget[1]}.'
                self.budgetLabel.configure(foreground='green')
            elif difference == 0:
                message = f'Attention! You have nothing left from your budget which is {budget[0]}€ {budget[1]}.'
                self.budgetLabel.configure(foreground='orange')
            else:
                message = f'Attention! You exceeded your budget ({budget[0]}€ {budget[1]}) by {-1*difference}€!'
                self.budgetLabel.configure(foreground='red')
            return message

        return "You haven't set a budget yet. You can do so in the preferences."
