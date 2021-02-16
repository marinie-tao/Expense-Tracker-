from tkinter import ttk, messagebox, StringVar, IntVar
from tkinter.ttk import Label, Button, OptionMenu, Radiobutton, Frame
from tkcalendar import DateEntry
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

from util import budget_pro_rata_temporis

class StatisticsTab:
    def __init__(self, tab_control, expense_controller, user_controller, username):
        """Initializes statistics tab with all visual elements"""
        self.statistics_tab = ttk.Frame(tab_control)
        tab_control.add(self.statistics_tab, text='Statistics')

        self.expense_controller = expense_controller
        self.user_controller = user_controller
        self.username = username

        self.dateformat_menu = StringVar()
        self.start_date = StringVar()
        self.end_date = StringVar()

        Label(self.statistics_tab, text='Graph settings', font='Helvetica 16 bold').grid(row=0, column=0, padx=15,
                                                                                         pady=15, sticky='w')
        Label(self.statistics_tab, text="Show expenses").grid(row=1, column=0, padx=(15, 0), sticky='w')
        option_list_format = ['daily', 'weekly', 'monthly', 'yearly']
        OptionMenu(self.statistics_tab, self.dateformat_menu, option_list_format[2], *option_list_format)\
            .grid(row=1, column=1, sticky='w')

        self.radio_btn_selection = IntVar(value=2)  # has to be part of self, otherwise preselection doesn't work
        Radiobutton(self.statistics_tab, text='Select period:', variable=self.radio_btn_selection, value=1)\
            .grid(row=2, column=0, padx=(15, 0), sticky='w')
        DateEntry(self.statistics_tab, width=9, textvariable=self.start_date, date_pattern='dd/MM/yyyy')\
            .grid(row=2, column=1, sticky='w')
        Label(self.statistics_tab, text='to').grid(row=2, column=2, sticky='w')
        DateEntry(self.statistics_tab, width=9, textvariable=self.end_date, date_pattern='dd/MM/yyyy')\
            .grid(row=2, column=3, sticky='w')
        Radiobutton(self.statistics_tab, text='Entire period', variable=self.radio_btn_selection, value=2) \
            .grid(row=3, column=0, padx=(15, 0), sticky='w')

        Button(self.statistics_tab, text="Update graphs", command=self.display_graph).grid(row=4, column=0,
                                                                                           padx=(15, 0), pady=10,
                                                                                           sticky='w')

        # FIRST FIGURE: Barchart
        self.fig1, self.ax1 = plt.subplots(figsize=(6, 3), dpi=100)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.statistics_tab)
        self.canvas1.get_tk_widget().grid(row=0, column=4, rowspan=8, padx=15, pady=(15, 0))
        self.toolbarFrame = Frame(master=self.statistics_tab)
        self.toolbarFrame.grid(row=8, column=4)
        self.toolbar = NavigationToolbar2Tk(self.canvas1, self.toolbarFrame)

        # SECOND FIGURE: Barchart
        self.fig2, self.ax2 = plt.subplots(figsize=(6, 3), dpi=100)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.statistics_tab)
        self.canvas2.get_tk_widget().grid(row=9, column=4, padx=15, pady=(15, 0))
        self.toolbarFrame2 = Frame(master=self.statistics_tab)
        self.toolbarFrame2.grid(row=10, column=4)
        self.toolbar2 = NavigationToolbar2Tk(self.canvas2, self.toolbarFrame2)

        # THIRD FIGURE: Piechart
        self.fig3, self.ax3 = plt.subplots(figsize=(4, 3), dpi=100)
        self.canvas3 = FigureCanvasTkAgg(self.fig3, master=self.statistics_tab)
        self.canvas3.get_tk_widget().grid(row=9, column=0, columnspan=4, padx=15, pady=(15, 0))
        self.toolbarFrame3 = Frame(master=self.statistics_tab)
        self.toolbarFrame3.grid(row=10, column=0, columnspan=4)
        self.toolbar3 = NavigationToolbar2Tk(self.canvas3, self.toolbarFrame3)

    def display_graph(self):
        """Calculates the information required and displays the three graphs"""
        # clear all figures
        self.ax1.cla()
        self.ax2.cla()
        self.ax3.cla()

        expenses = self.expense_controller.get_expenses_for_user(self.username)
        if not expenses:
            messagebox.showerror('No Expenses', 'There are no expenses to analyse, You can enter a new expense in the '
                                                'expense tab')
            return

        df = pd.DataFrame()
        for v in expenses.values():
            df = df.append(pd.DataFrame.from_dict([v]), ignore_index=True)

        df_reduced = df[['price_in_euro', 'category']]
        df_reduced.index = pd.to_datetime(df['date'], format='%d/%m/%Y')
        df_reduced = df_reduced.sort_index()

        # get selected period
        if self.radio_btn_selection.get() == 1:  # selected period
            start_date = datetime.strptime(self.start_date.get(), '%d/%m/%Y')
            end_date = datetime.strptime(self.end_date.get(), '%d/%m/%Y')
            # Verify if selected start and end dates are correct
            if start_date > end_date:
                messagebox.showerror("Date Selection Error", "Starting date should be smaller than ending date")
                return
            # filter dataframe to only contain selected date period
            df_reduced = df_reduced.loc[(df_reduced.index <= end_date) & (df_reduced.index >= start_date)]

        grouping = self.dateformat_menu.get()  # retrieve how user wants expenses to be grouped
        # group according to user preferences: By day, week, month or year
        if grouping == 'daily':
            sum_for_period = df_reduced.groupby(by=[df_reduced.index.year, df_reduced.index.month,
                                                    df_reduced.index.day]).sum()
            self.ax1.set_title('Your expenses per day')
            self.ax2.set_title('Your remaining budget per day')
            self.ax1.set_xlabel('Year, Month, Day')
        elif grouping == 'weekly':
            sum_for_period = df_reduced.groupby(by=[df_reduced.index.year, df_reduced.index.isocalendar()['week']])\
                .sum()
            self.ax1.set_title('Your expenses per week')
            self.ax2.set_title('Your remaining budget per week')
            self.ax1.set_xlabel('Year, Calendarweek')
        elif grouping == 'monthly':
            sum_for_period = df_reduced.groupby(by=[df_reduced.index.year, df_reduced.index.month]).sum()
            self.ax1.set_title('Your expenses per month')
            self.ax2.set_title('Your remaining budget per month')
            self.ax1.set_xlabel('Year, Month')
        elif grouping == 'yearly':
            sum_for_period = df_reduced.groupby(by=df_reduced.index.year).sum()
            self.ax1.set_title('Your expenses per year')
            self.ax2.set_title('Your remaining budget per year')
            self.ax1.set_xlabel('Year')
        else:
            messagebox.showerror("Selection error", "No grouping selected")
            return

        x_arr = sum_for_period.index.to_numpy()
        for i, x in enumerate(x_arr):
            if str(x)[0] == '(':
                x_arr[i] = str(x)[1:-1]
        y_arr = sum_for_period['price_in_euro'].to_numpy()

        self.ax1.set_ylabel('Total expenses in €')
        self.ax1.set_xticks(np.arange(len(x_arr)))
        self.ax1.set_xticklabels(x_arr)
        self.ax1.bar(np.arange(len(x_arr)), y_arr, 0.5, align='center')
        for i, v in enumerate(y_arr):
            self.ax1.text(i-0.25, v+3, "{:.2f} €".format(v))
        self.fig1.autofmt_xdate()
        # placing the canvas on the Tkinter window
        self.canvas1.draw()
        self.toolbar.update()

        # SECOND FIGURE: Bar chart showing budget difference
        try:
            budget = float(self.user_controller.get_budget(self.username)[0])
            period = self.user_controller.get_budget(self.username)[1]
            budget = budget_pro_rata_temporis(budget, period, grouping)
        except TypeError:
            messagebox.showerror("No budget", "You haven't set a budget. You can do so in the preferences")
            budget = 0
        except ValueError:
            messagebox.showerror("No budget", "You haven't set a budget. You can do so in the preferences")
            budget = 0

        sum_for_period['price_in_euro'] = sum_for_period['price_in_euro'].mul(-1).add(budget)
        sum_for_period['positive'] = sum_for_period['price_in_euro'] > 0
        y_arr_budget = sum_for_period['price_in_euro'].to_numpy()

        self.ax2.set_ylabel("Total in €")
        self.ax2.set_xticks([])
        self.ax2.bar(np.arange(len(x_arr)), y_arr_budget, 0.5, align='center',
                     color=sum_for_period.positive.map({True: 'g', False: 'r'}))
        for i, v in enumerate(y_arr_budget):
            if v >= 0:
                self.ax2.text(i - 0.25, v + 3, "{:.2f} €".format(v))
            else:
                self.ax2.text(i - 0.25, v - 15, "{:.2f} €".format(v))
        self.ax2.spines['bottom'].set_position('zero')
        self.ax2.spines['top'].set_color('none')
        self.ax2.spines['right'].set_color('none')
        self.canvas2.draw()

        # FIGURE 3: Pie chart of expenses per category
        purchases = {}
        category_list = df_reduced['category'].unique()

        if category_list.any():
            for i in category_list:
                c = []
                for idx, row in df_reduced.iterrows():
                    if row["category"] == i:
                        if float(row["price_in_euro"]) > 0:
                            c.append(float(row["price_in_euro"]))
                        purchases[i] = sum(c)

            def func(val):
                return "{:.2f} €".format(np.round(val / 100. * sum(purchases.values()), 2))

            self.ax3.set_title('Your expenses per category')
            self.ax3.pie([float(v) for v in purchases.values()], labels=[k for k in purchases.keys()],
                         autopct=func, shadow=True)
            self.canvas3.draw()
