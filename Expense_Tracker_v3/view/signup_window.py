from tkinter import font, messagebox

from view.main_window import *
from util import *

class SignupWindow:

    def __init__(self, user_controller, expense_controller, login_window):
        """Initializes the signup window, where a user can create a new account"""
        self.user_controller = user_controller
        self.expense_controller = expense_controller
        self.login_window = login_window

        # Set signup window
        self.signup_screen = Toplevel(self.login_window.login_window)

        # User input of the login and signup windows
        self.username = StringVar()
        self.password = StringVar()
        self.password_repetition = StringVar()
        self.firstname = StringVar()
        self.lastname = StringVar()
        self.email = StringVar()

        self.define_signup_window()
        center_window(self.signup_screen)

    def back_to_login(self, event=None):
        """
        Function that closes the signup window and goes back to login. After successful account creation or
        clicking the back button
        """
        self.signup_screen.withdraw()
        self.login_window.show_window()

    def account_creation_handler(self):
        """
        Verifies basic constraints, such as if all required fields are filled in and then passes the information to the
        user controller for further verification and account creation in the database.
        Shows a messagebox in case of error.
        Creates a success text on the login window in case of success.
        """
        username = self.username.get().lower()
        password = self.password.get()
        password_repetition = self.password_repetition.get()
        firstname = self.firstname.get()
        lastname = self.lastname.get()
        email = self.email.get()

        if not username or not password or not password_repetition:
            messagebox.showerror("Registration Error", "Please fill all required fields (marked with *)")
            return

        if password != password_repetition:
            messagebox.showerror("Registration Error", "Password wasn't repeated correctly. Please check your password "
                                                       "entry again.")
            return

        #  create id_user account w.r.t to username
        account_created, account_text = self.user_controller.create_account(username, password, firstname, lastname,
                                                                            email)

        if not account_created:
            messagebox.showerror("Registration Error", account_text)
        else:
            Label(self.login_window.login_window, text=account_text, fg="green").grid(row=5, column=0, columnspan=2,
                                                                                      sticky="ew", pady=10)
            # if true, then also create expense database associated to username
            # self.expense_controller.create_account(username, password)
            self.signup_screen.destroy()
            self.login_window.show_window()

    def define_signup_window(self):
        """
        Defines the visual elements of the signup screen (Fields, Buttons, ...)
        """
        self.signup_screen.title("Register")

        # Create the label
        Label(self.signup_screen, text="Please enter your information below:").grid(row=0, column=0, columnspan=2,
                                                                                    sticky="ew", padx=10, pady=10)

        # USERNAME ENTRY
        Label(self.signup_screen, text="Username*").grid(row=1, column=0, sticky="e", padx=10)
        Entry(self.signup_screen, textvariable=self.username).grid(row=1, column=1, sticky="e", padx=10)

        # FIRSTNAME ENTRY
        Label(self.signup_screen, text="First name").grid(row=2, column=0, sticky="e", padx=10)
        Entry(self.signup_screen, textvariable=self.firstname).grid(row=2, column=1, sticky="e", padx=10)

        # LASTNAME ENTRY
        Label(self.signup_screen, text="Last name").grid(row=3, column=0, sticky="e", padx=10)
        Entry(self.signup_screen, textvariable=self.lastname).grid(row=3, column=1, sticky="e", padx=10)

        # EMAIL ENTRY
        Label(self.signup_screen, text="E-Mail").grid(row=4, column=0, sticky="e", padx=10)
        Entry(self.signup_screen, textvariable=self.email).grid(row=4, column=1, sticky="e", padx=10)

        # PASSWORD ENTRY
        Label(self.signup_screen, text="Password*").grid(row=5, column=0, sticky="e", padx=10)
        Entry(self.signup_screen, textvariable=self.password, show='*').grid(row=5, column=1, sticky="e", padx=10)

        Label(self.signup_screen, text="Repeat Password*").grid(row=6, column=0, sticky="e", padx=10)
        Entry(self.signup_screen, textvariable=self.password_repetition, show='*').grid(row=6, column=1, sticky="e",
                                                                                        padx=10)

        # SIGNUP button
        Button(self.signup_screen, text="Sign up!", width=10, height=1, command=self.account_creation_handler)\
            .grid(row=7, column=1, sticky="ew", padx=10, pady=5)

        back_label = Label(self.signup_screen, text="Back to login screen")
        back_label.grid(row=8, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        f = font.Font(back_label, back_label.cget("font"))
        f.configure(underline=True)
        back_label.configure(font=f)
        back_label.bind("<Button-1>", self.back_to_login)

        self.signup_screen.protocol("WM_DELETE_WINDOW", self.back_to_login)
