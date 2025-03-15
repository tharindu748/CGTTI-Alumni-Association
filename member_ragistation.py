import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk  # type: ignore # Use ThemedTk for enhanced look and feel
import db_manager # Importing the database management module
from main_window import MainApp

class MemberRegistration:
    def __init__(self, parent):
        self.parent = parent  # This is the frame where widgets will be placed
        self.frame = ttk.Frame(self.parent)  # Internal frame
        self.frame.pack(fill="both", expand=True)
        self.current_page = 1
        self.items_per_page = 50

        # Configure the parent window (if it's a Tk or Toplevel window)
        if isinstance(self.parent.master, tk.Tk) or isinstance(self.parent.master, tk.Toplevel):
            self.parent.master.title("CGTTI Alumni Association")
            self.parent.master.geometry("1000x600")
            self.parent.master.state("zoomed")
            self.parent.master.configure(bg="lightyellow")

        self.create_widgets()
        self.load_members()

    def create_widgets(self):
        # === LEFT PANEL (Dark Gray Background) ===
        left_frame = ttk.Frame(self.parent, width=300, height=600, relief="solid")  # Use self.parent
        left_frame.pack(side="left", fill="y")

        # Logo
        logo_label = ttk.Label(left_frame, text="CGTTI Alumni", font=("Arial", 14, "bold"))
        logo_label.pack(pady=10)

        # Title
        title_label = ttk.Label(left_frame, text="MEMBER REGISTRATION", font=("Arial", 12, "bold"), foreground="blue")
        title_label.pack()

        # === Form Fields ===
        fields = ["Training number", "Membership year", "Trade", "Name", "District", "Membership number", "Address", "Mobile", "Nic"]
        self.entries = {}

        for field in fields:
            lbl = ttk.Label(left_frame, text=field, font=("Arial", 10), foreground="black")
            lbl.pack(anchor="w", padx=10, pady=2)

            if field == "Trade":
                # List of Trades
                trades = [
                    "TOOL MACHINE TRADE",
                    "MILLWRIGHT TRADE",
                    "AUTO MOBILE TRADE",
                    "BRP TRADE",
                    "AUTO ELECTRICAL TRADE",
                    "REF AND A/C TRADE",
                    "MECHATRONIC TRADE",
                    "DISAL PUMP TRADE",
                    "WELDING TRADE",
                    "POWER ELECTRICAL TRADE"
                ]
                entry = ttk.Combobox(left_frame, values=trades)
            
            elif field == "District":
                # List of Sri Lankan districts
                districts = [
                    "Ampara", "Anuradhapura", "Badulla", "Batticaloa", "Colombo", "Galle", "Gampaha",
                    "Hambantota", "Jaffna", "Kalutara", "Kandy", "Kegalle", "Kilinochchi", "Kurunegala",
                    "Mannar", "Matale", "Matara", "Moneragala", "Mullaitivu", "Nuwara Eliya", "Polonnaruwa",
                    "Puttalam", "Ratnapura", "Trincomalee", "Vavuniya"
                ]
                entry = ttk.Combobox(left_frame, values=districts)
            
            else:
                entry = ttk.Entry(left_frame)

            entry.pack(padx=10, pady=2, fill="x")
            self.entries[field] = entry

        # === Payment Status (Radio Buttons) ===
        self.payment_status = tk.StringVar(value="Paid Up")
        ttk.Radiobutton(left_frame, text="PAID UP",  variable=self.payment_status, value="Paid Up").pack(anchor="w", padx=10)
        ttk.Radiobutton(left_frame, text="NON-PAID", variable=self.payment_status, value="Non-Paid").pack(anchor="w", padx=10)

        # === Member Status (Checkboxes) ===
        ttk.Label(left_frame, text="This member is dead", font=("Arial", 10, "bold"), foreground="black").pack(anchor="w", padx=10, pady=2)
        self.dead_var = tk.BooleanVar()
        self.alive_var = tk.BooleanVar()
        ttk.Checkbutton(left_frame, text="(Click this only if dead)", variable=self.dead_var).pack(anchor="w", padx=10)
        ttk.Checkbutton(left_frame, text="(Click this only if alive)", variable=self.alive_var).pack(anchor="w", padx=10)

        # === Buttons (SAVE, UPDATE, DELETE, LOAD) ===
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(pady=10)

        # Define a style for the buttons
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10, "bold"), foreground="black")

        # Create buttons with the defined style
        ttk.Button(btn_frame, text="SAVE", width=10, command=self.save_member, style="TButton").pack(side="left", padx=3, pady=3)
        ttk.Button(btn_frame, text="UPDATE", width=10, command=self.update_member, style="TButton").pack(side="left", padx=3, pady=3)
        ttk.Button(btn_frame, text="DELETE", width=10, command=self.delete_member, style="TButton").pack(side="left", padx=3, pady=3)
        ttk.Button(btn_frame, text="LOAD", width=10, command=self.load_members, style="TButton").pack(side="left", padx=3, pady=3)

        # === Treeview Section ===
        right_frame = ttk.Frame(self.parent)  # Use self.parent
        right_frame.pack(side="right", fill="both", expand=True)

        # Search bar
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(right_frame, textvariable=self.search_var, width=50)
        search_entry.pack(pady=10)
        ttk.Button(right_frame, text="SEARCH", command=self.search_member).pack(pady=5)

        # Create the Treeview
        columns = ("Trainingnumber", "Memberyear", "Trade", "MemberName", "District", "Membershipnumber", "Address", "Mobile", "Nic", "Paide", "LivingorDead")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings")

        # Add headings and columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)

        # Vertical Scrollbar
        v_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        v_scrollbar.pack(side="right", fill="y")

        # Horizontal Scrollbar
        h_scrollbar = ttk.Scrollbar(right_frame, orient="horizontal", command=self.tree.xview)
        h_scrollbar.pack(side="bottom", fill="x")

        # Configure the Treeview to use the scrollbars
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack the Treeview (ensure it expands to fill the space)
        self.tree.pack(fill="both", expand=True)

        # Bind the selection event of the Treeview to the row selection handler
        self.tree.bind("<ButtonRelease-1>", self.on_row_select)

        # Pagination controls
        pagination_frame = ttk.Frame(right_frame)
        pagination_frame.pack(fill="x", pady=10)

        # Define a style for the buttons
        style = ttk.Style()
        style.configure("Pagination.TButton", font=("Arial", 10, "bold"), foreground="white")  # White text on blue background

        # Previous Button
        self.prev_button = ttk.Button(pagination_frame, text="Previous", command=self.prev_page, style="Pagination.TButton")
        self.prev_button.pack(side="left", padx=10)

        # Page Label
        self.page_label = ttk.Label(pagination_frame, text="Page 1 of 1", font=("Arial", 12), foreground="black")  # Dark blue text
        self.page_label.pack(side="left", padx=10)

        # Next Button
        self.next_button = ttk.Button(pagination_frame, text="Next", command=self.next_page, style="Pagination.TButton")
        self.next_button.pack(side="left", padx=10)

        # Section below Treeview
        bottom_frame = ttk.Frame(right_frame)
        bottom_frame.pack(fill="x", pady=10)
        ttk.Label(bottom_frame, text="CGTTI Alumni Association", font=("Arial", 12)).pack()

    def on_row_select(self, event):
        """
        This function will fill the input fields with the selected row's data from the Treeview.
        """
        selected_item = self.tree.selection()[0]  # Get selected row
        selected_values = self.tree.item(selected_item, "values")

        # Fill the input fields with the selected row's data
        self.entries["Training number"].delete(0, tk.END)
        self.entries["Training number"].insert(0, selected_values[0])

        self.entries["Membership year"].delete(0, tk.END)
        self.entries["Membership year"].insert(0, selected_values[1])

        self.entries["Trade"].set(selected_values[2])
        self.entries["Name"].delete(0, tk.END)
        self.entries["Name"].insert(0, selected_values[3])

        self.entries["District"].set(selected_values[4])
        self.entries["Membership number"].delete(0, tk.END)
        self.entries["Membership number"].insert(0, selected_values[5])

        self.entries["Address"].delete(0, tk.END)
        self.entries["Address"].insert(0, selected_values[6])

        self.entries["Mobile"].delete(0, tk.END)
        self.entries["Mobile"].insert(0, selected_values[7])

        self.entries["Nic"].delete(0, tk.END)
        self.entries["Nic"].insert(0, selected_values[8])

        # Assuming 'Paid Up' or 'Non-Paid' is the 9th column in the treeview
        if selected_values[9] == "Paid Up":
            self.payment_status.set("Paid Up")
        else:
            self.payment_status.set("Non-Paid")

        # Assuming 'Living' or 'Deceased' is the 10th column in the treeview
        if selected_values[10] == "living":
            self.dead_var.set(False)
            self.alive_var.set(True)
        else:
            self.dead_var.set(True)
            self.alive_var.set(False)

    def save_member(self):
        member_data = {
            "training_number": self.entries["Training number"].get(),
            "member_year": self.entries["Membership year"].get(),
            "trade": self.entries["Trade"].get(),
            "member_name": self.entries["Name"].get(),
            "district": self.entries["District"].get(),
            "membership_number": self.entries["Membership number"].get(),
            "address": self.entries["Address"].get(),
            "mobile": self.entries["Mobile"].get(),
            "nic": self.entries["Nic"].get(),
            "paid_status": 1 if self.payment_status.get() == "Paid Up" else 0,
            "living_status": "deceased" if self.dead_var.get() else "living"
        }
        
        with db_manager.DBManager() as db:
            if db.insert_member(member_data):
                # messagebox.showinfo("Success", "Member saved successfully!")
                self.load_members()
            else:
                messagebox.showerror("Error", "Failed to save member.")

    def update_member(self):
        member_id = self.entries["Membership number"].get()
        if not member_id:
            messagebox.showerror("Error", "Please enter a membership number to update.")
            return
        member_data = {
            "training_number": self.entries["Training number"].get(),
            "member_year": self.entries["Membership year"].get(),
            "trade": self.entries["Trade"].get(),
            "member_name": self.entries["Name"].get(),
            "membership_number": self.entries["Membership number"].get(),
            "district": self.entries["District"].get(),
            "address": self.entries["Address"].get(),
            "mobile": self.entries["Mobile"].get(),
            "nic": self.entries["Nic"].get(),
            "paid_status": 1 if self.payment_status.get() == "Paid Up" else 0,
            "living_status": "deceased" if self.dead_var.get() else "living"
        }
        
        with db_manager.DBManager() as db:
            if db.update_member(member_id, member_data):
                # messagebox.showinfo("Success", "Member updated successfully!")
                self.load_members()
            else:
                messagebox.showerror("Error", "Failed to update member.")

    def delete_member(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a member to delete.")
            return  # Return early if no item is selected

        # Get the membership number from the selected row
        selected_values = self.tree.item(selected_item, "values")
        member_id = selected_values[5]  # Membership number is the 6th column (index 5)

        with db_manager.DBManager() as db:
            if db.delete_member(member_id):
                # messagebox.showinfo("Success", "Member deleted successfully!")
                self.load_members()
            else:
                messagebox.showerror("Error", "Failed to delete member.")

    def load_members(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        with db_manager.DBManager() as db:
            members = db.fetch_members()
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        for member in members[start_index:end_index]:
            self.tree.insert("", "end", values=( 
                member["training_number"], member["member_year"], member["trade"], member["member_name"],
                member["district"], member["membership_number"], member["address"], member["mobile"],
                member["nic"], "Paid Up" if member["paid_status"] else "Non-Paid", member["living_status"]
            ))
        self.update_pagination_buttons(len(members))

    def search_member(self):
        query = self.search_var.get().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        with db_manager.DBManager() as db:
            members = db.fetch_members()
        filtered_members = [
            member for member in members
            if query in member["training_number"].lower() or
               query in member["member_year"].lower() or
               query in member["trade"].lower() or
               query in member["member_name"].lower() or
               query in member["district"].lower() or
               query in member["membership_number"].lower() or
               query in member["address"].lower() or
               query in member["mobile"].lower() or
               query in member["nic"].lower()
        ]
        for member in filtered_members:
            self.tree.insert("", "end", values=( 
                member["training_number"], member["member_year"], member["trade"], member["member_name"],
                member["district"], member["membership_number"], member["address"], member["mobile"],
                member["nic"], "Paid Up" if member["paid_status"] else "Non-Paid", member["living_status"]
            ))

    def update_pagination_buttons(self, total_items):
        total_pages = (total_items + self.items_per_page - 1) // self.items_per_page
        self.prev_button.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_page < total_pages else tk.DISABLED)
        self.page_label.config(text=f"Page {self.current_page} of {total_pages}")

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_members()

    def next_page(self):
        with db_manager.DBManager() as db:
            members = db.fetch_members()
        total_pages = (len(members) + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_members()

if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = MemberRegistration(root)
    root.mainloop()
