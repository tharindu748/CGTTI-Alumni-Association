import tkinter as tk
from tkinter import messagebox
from db_manager import DBManager  # Import the DBManager class

class AdminRegistration:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill="both", expand=True)

        # Title
        tk.Label(self.frame, text="Admin Registration", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

        # Username
        tk.Label(self.frame, text="Username:", font=("Arial", 10), bg="#f0f0f0").pack()
        self.username_entry = tk.Entry(self.frame, width=30)
        self.username_entry.pack(pady=5)

        # Password
        tk.Label(self.frame, text="Password:", font=("Arial", 10), bg="#f0f0f0").pack()
        self.password_entry = tk.Entry(self.frame, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Register Button
        tk.Button(self.frame, text="Register", command=self.register_user, width=20, bg="#4CAF50", fg="white").pack(pady=10)

    def register_user(self):
        """Register a new user."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            with DBManager() as db:
                if db.register_user(username, password):
                    messagebox.showinfo("Success", "User registered successfully!")
                    self.parent.destroy()  # Close the registration window
                else:
                    messagebox.showerror("Error", "Username already exists or registration failed!")
        else:
            messagebox.showerror("Error", "Username and password cannot be empty!")

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    admin_registration = AdminRegistration(root)
    root.mainloop()