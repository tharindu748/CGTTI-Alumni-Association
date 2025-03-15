import tkinter as tk
from tkinter import messagebox
from db_manager import DBManager  # Import the DBManager class

class AdminRegistration:
    def __init__(self, parent):
        self.parent = parent
        # self.parent.title("Admin Registration")
        # self.parent.geometry("400x300")
        # self.parent.configure(bg="#f0f0f0")

        # Add widgets to the parent frame
        tk.Label(self.parent, text="Admin Registration", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)
        tk.Label(self.parent, text="Username:", font=("Arial", 10), bg="#f0f0f0").pack()
        self.username_entry = tk.Entry(self.parent, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(self.parent, text="Password:", font=("Arial", 10), bg="#f0f0f0").pack()
        self.password_entry = tk.Entry(self.parent, width=30, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.parent, text="Register", command=self.register_user, width=20, bg="#4CAF50", fg="white").pack(pady=10)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            self.clear_input_fields()
            # Add your registration logic here
            messagebox.showinfo("Success", "Admin registered successfully!")
        else:
            messagebox.showerror("Error", "Username and password cannot be empty!")

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    admin_registration = AdminRegistration(root)
    root.mainloop()