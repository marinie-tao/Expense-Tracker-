from tkinter import ttk, Listbox, StringVar, messagebox
from tkinter.ttk import Label, Entry, Button, Scrollbar, OptionMenu

period_list = ['per day', 'per week', 'per month', 'per year']
currency_list = ['AUD', 'CAD', 'CHF', 'CNY', 'DKK', 'EUR', 'GBP', 'INR', 'JPY', 'LBP', 'NOK', 'NZD', 'MAD', 'USD',
                 'SEK', 'TND']

class PreferencesTab:

    def __init__(self, tab_control, username, user_controller, expense_tab):
        """Initializes the preferences tab, where the user can customise the application, with all visual elements"""
        # create preference tab with title 'Preferences'
        self.preferences_tab = ttk.Frame(tab_control)
        tab_control.add(self.preferences_tab, text='Preferences')

        self.expense_tab = expense_tab
        self.username = username
        self.user_controller = user_controller

        # Category list is saved as list variable and as StringVar instance:
        # The list represents the custom categories of the user and is loaded from the database,
        # the StringVar is the TK representation and is the object containing the values for the Listbox
        self.category_list = self.user_controller.get_categories(self.username)
        self.category_var = StringVar(value=self.category_list)

        # Previously set budget is loaded from the database
        new_category = StringVar()
        b, p = self.user_controller.get_budget(self.username)
        budget = StringVar(value=b)
        chosen_period = StringVar(value=p)

        Label(self.preferences_tab, text="Your categories:", font='Helvetica 16 bold').grid(row=0, column=0, padx=15,
                                                                                            pady=15, sticky='w')

        y_scroll = Scrollbar(self.preferences_tab, orient='vertical')
        y_scroll.grid(row=1, column=0, pady=15, padx=(0, 15), sticky='nse')
        listbox = Listbox(self.preferences_tab, listvar=self.category_var, yscrollcommand=y_scroll.set, bd=0, height=15)
        listbox.grid(row=1, column=0, padx=(15, 0), pady=15, sticky='w')
        y_scroll['command'] = listbox.yview

        Button(self.preferences_tab, text='Remove', command=lambda: self.remove_category(listbox), style='W.TButton')\
            .grid(row=1, column=1, padx=15, pady=15, sticky='s')

        Label(self.preferences_tab, text='Add category:').grid(row=2, column=0, padx=15, sticky='w')
        Entry(self.preferences_tab, textvariable=new_category).grid(row=3, column=0, padx=15, sticky='ew')
        Button(self.preferences_tab, text='Add', command=lambda: self.add_category(new_category)).grid(row=3, column=1)

        Label(self.preferences_tab, text="Set yourself a budget!", font='Helvetica 16 bold')\
            .grid(row=6, column=0, padx=(15, 0), pady=20, sticky='w')

        Entry(self.preferences_tab, textvariable=budget).grid(row=7, column=0, padx=(15, 0), sticky='w')
        Label(self.preferences_tab, text='€').grid(row=7, column=0, sticky='e')
        OptionMenu(self.preferences_tab, chosen_period, p, *period_list).grid(row=7, column=1)
        Button(self.preferences_tab, text='Set budget', command=lambda: self.set_budget(budget, chosen_period))\
            .grid(row=7, column=2)

    def add_category(self, new_category):
        """
        Verifies the new category name, adds it to the list and calls the user controller to add it to the DB
        Shows a messagebox in case the category already exists
        """
        new_category = new_category.get()
        if new_category in self.category_list:
            messagebox.showerror('Error', 'Category already exists')
            return
        else:
            self.category_list.insert(0, new_category)
            self.category_var.set(self.category_list)
            self.user_controller.set_categories(self.username, self.category_list)
            self.expense_tab.refresh_categories(self.category_list)

    def remove_category(self, listbox):
        """
        Removes a selected category from the list and calls the user controller to remove it from the DB.
        Shows a messagebox in case of failure
        """
        try:
            selected_category = listbox.curselection()[0]
            del self.category_list[selected_category]
            self.category_var.set(self.category_list)
            self.user_controller.set_categories(self.username, self.category_list)
            self.expense_tab.refresh_categories(self.category_list)
        except IndexError:
            messagebox.showerror('Selection Error', 'Please select an element to remove')

    def set_budget(self, budget, chosen_period):
        """
        Passes the chosen budget and period to the user controller, to add it to the database.
        Shows a messagebox for success/failure
        """
        success, message = self.user_controller.set_budget(self.username, budget.get(), chosen_period.get())
        if success:
            messagebox._show("Success!", message)
            budget_message = self.expense_tab.calculate_budget_level()
            self.expense_tab.budget_message.set(budget_message)
        else:
            messagebox.showerror("Error", message)
        return
