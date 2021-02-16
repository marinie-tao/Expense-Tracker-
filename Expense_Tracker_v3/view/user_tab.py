from tkinter import ttk, StringVar, messagebox
from tkinter.ttk import Label, Button, Entry


class UserTab:

    def __init__(self, main_window, tab_control, username, user_controller):
        """Initializes the user tab with all visual elements"""
        self.main_window = main_window
        self.username = username
        self.user_controller = user_controller

        self.user_info = self.user_controller.get_user(self.username)

        self.user_tab = ttk.Frame(tab_control)
        tab_control.add(self.user_tab, text='User')

        self.new_password = StringVar()
        self.new_password_repeat = StringVar()
        self.new_firstname = StringVar(value=self.user_info['firstname'])
        self.new_lastname = StringVar(value=self.user_info['lastname'])
        self.new_email = StringVar(value=self.user_info['email'])

        # USER INFORMATION
        Label(self.user_tab, text="Your information:", font='Helvetica 16 bold').grid(row=0, column=0, padx=15, pady=15,
                                                                                      sticky='w')

        Label(self.user_tab, text="Username:").grid(row=1, column=0, sticky='w', padx=15, pady=5)
        Label(self.user_tab, text=username).grid(row=1, column=1, sticky='w', pady=5)

        Label(self.user_tab, text="First name:").grid(row=2, column=0, sticky='w', padx=15, pady=5)
        Label(self.user_tab, textvariable=self.new_firstname).grid(row=2, column=1, sticky='w', pady=5)

        Label(self.user_tab, text="Last name:").grid(row=3, column=0, sticky='w', padx=15, pady=5)
        Label(self.user_tab, textvariable=self.new_lastname).grid(row=3, column=1, sticky='w', pady=5)

        Label(self.user_tab, text="Email:").grid(row=4, column=0, sticky='w', padx=15, pady=5)
        Label(self.user_tab, textvariable=self.new_email).grid(row=4, column=1, sticky='w', pady=5)

        # CHANGE USER INFORMATION BUTTON
        Button(self.user_tab, text='Modify information', command=self.change_information).grid(row=5, column=1,
                                                                                               pady=10, sticky='w')

        # CHANGE PASSWORT FIELDS AND BUTTON
        Label(self.user_tab, text="Change password:", font='Helvetica 16 bold').grid(row=6, column=0, padx=15, pady=15,
                                                                                     sticky='w')
        Label(self.user_tab, text="New password:").grid(row=7, column=0, padx=15, sticky='w')
        Entry(self.user_tab, textvariable=self.new_password, show='*').grid(row=7, column=1, sticky='w')
        Label(self.user_tab, text="Repeat password:").grid(row=8, column=0, padx=15, sticky='w')
        Entry(self.user_tab, textvariable=self.new_password_repeat, show='*').grid(row=8, column=1, sticky='w')
        Button(self.user_tab, text='Submit new password', command=self.change_password).grid(row=9, column=1, pady=10,
                                                                                             sticky='w')

        # LOGOUT BUTTON
        Button(self.user_tab, text='Logout', command=self.logout).grid(row=10, column=3, padx=120, pady=50)

    def change_information(self):
        """Creates fields where new user information can be typed and button to save it"""
        self.nameentry = Entry(self.user_tab, textvariable=self.new_firstname)
        self.nameentry.grid(row=2, column=1, sticky='w')
        self.lnameentry = Entry(self.user_tab, textvariable=self.new_lastname)
        self.lnameentry.grid(row=3, column=1, sticky='w')
        self.mailentry = Entry(self.user_tab, textvariable=self.new_email)
        self.mailentry.grid(row=4, column=1, sticky='w')
        self.btn = Button(self.user_tab, text='Submit changes', command=self.submit_changes)
        self.btn.grid(row=5, column=1, pady=10, sticky='ew')

    def submit_changes(self):
        """
        Passes the new user information to user controller. If successful, fields are destroyed.
        If not, a messagebox is shown and the user can continue editing the information in the fields
        """
        success, message = self.user_controller.edit_user(self.username, self.new_firstname.get(),
                                                          self.new_lastname.get(), self.new_email.get())

        if success:
            self.user_info = self.user_controller.get_user(self.username)
            self.new_firstname.set(self.user_info['firstname'])
            self.new_lastname.set(self.user_info['lastname'])
            self.new_email.set(self.user_info['email'])
            print(self.new_firstname.get(), self.new_lastname.get(), self.new_email.get())
            self.nameentry.destroy()
            self.lnameentry.destroy()
            self.mailentry.destroy()
            self.btn.destroy()
            return
        else:
            messagebox.showerror("Input error", message)

    def change_password(self):
        """
        Verifies basic conditions, such that password is repeated correctly and then passes the password to the
        user controller to change it in the DB.
        Shows messagebox for success and failure.
        """
        if self.new_password.get() != self.new_password_repeat.get():
            messagebox.showerror("Error", "Password wasn't repeated correctly. Please check your password entry again.")
            return

        password_changed, message = self.user_controller.edit_password(self.username, self.new_password.get())
        if password_changed:
            self.new_password.set('')
            self.new_password_repeat.set('')
            messagebox._show("Success", message)
        else:
            messagebox.showerror("Input error", message)

    def logout(self):
        """Function that is called when the logout button is clicked. Triggers the closing of the window"""
        self.main_window.close_main_window()
