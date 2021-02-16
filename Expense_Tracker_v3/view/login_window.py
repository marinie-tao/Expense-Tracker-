from tkinter.ttk import Label

from view.signup_window import *

class LoginWindow:

    def __init__(self, user_controller, expense_controller):
        """Initialize the Login Window"""
        # Class used for in the windows
        self.user_controller = user_controller
        self.expense_controller = expense_controller

        # Set login window
        self.login_window = Tk()

        # User input of the login window
        self.username_login = StringVar()
        self.password_login = StringVar()

        self.login_window.withdraw()
        self.define_login_window()
        center_window(self.login_window)

    def close_login_window(self):
        """Triggers the saving of all data to a pickle file and then closes the login_window, thus the application"""
        save_database_to_file(self.user_controller.get_user_database(), self.expense_controller.get_expense_database())
        self.login_window.destroy()

    def show_window(self):
        """Makes the window reappear"""
        self.login_window.deiconify()

    def login_handler(self):
        """
        Passes information for login to the user controller after basic verification.
        If login is successful, generates the main window (= logs the user in).
        Unless, shows login error.
        """
        username = self.username_login.get().lower()  # username is non-case sensitive
        password = self.password_login.get()

        is_login, login_text = self.user_controller.login(username, password)

        if not is_login:
            messagebox.showerror("Login Error", login_text)
        else:
            # CREATION DATABASE GUI WINDOWS
            self.username_login.set('')
            self.password_login.set('')
            MainWindow(self.user_controller, self.expense_controller, username, self.login_window)

    def generate_signup_window(self, event=None):
        """Generates a signup screen. Function is called when clicking on the signup text"""
        SignupWindow(self.user_controller, self.expense_controller, self)
        self.login_window.withdraw()

    def define_login_window(self):
        """
        Define login screen with all visual elements (Fields, Buttons, ...)
        """
        self.login_window.title("Login")

        # Create the label
        Label(self.login_window, text="Please enter login details:").grid(row=0, column=0, columnspan=2, sticky="ew",
                                                                          padx=10, pady=10)

        # USERNAME ENTRY
        Label(self.login_window, text="Username").grid(row=1, column=0, sticky="e", padx=10)
        Entry(self.login_window, textvariable=self.username_login).grid(row=1, column=1, sticky="e", padx=10)

        # PASSWORD ENTRY
        Label(self.login_window, text="Password").grid(row=2, column=0, sticky="e", padx=10)
        Entry(self.login_window, textvariable=self.password_login, show='*').grid(row=2, column=1, sticky="e", padx=10)

        # LOGIN button
        Button(self.login_window, text="Login", width=10, height=1, command=self.login_handler).grid(row=3, column=1,
                                                                                                     sticky="ew",
                                                                                                     padx=10, pady=5)

        # NEW ACCOUNT Label
        new_account_label = Label(self.login_window, text="No account yet? Sign up!")
        new_account_label.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        f = font.Font(new_account_label, new_account_label.cget("font"))
        f.configure(underline=True)
        new_account_label.configure(font=f)
        new_account_label.bind("<Button-1>", self.generate_signup_window)

        # This function self.close_login_window,
        # is called when pushing the cross button right top to close the window,
        self.login_window.protocol("WM_DELETE_WINDOW", self.close_login_window)

    def execute(self):
        """Function that makes the Tkinter application responsive"""
        self.login_window.mainloop()
