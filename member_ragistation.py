import tkinter as tk
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk
import db_manager
from main_window import MainApp

class MemberRegistration:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill="both", expand=True)
        self.current_page = 1
        self.items_per_page = 50

        if isinstance(self.parent.master, (tk.Tk, tk.Toplevel)):
            self.parent.master.title("CGTTI Alumni Association")
            self.parent.master.geometry("1000x600")
            self.parent.master.state("zoomed")
            self.parent.master.configure(bg="lightyellow")

        self.create_widgets()
        self.load_members()

    def create_widgets(self):
        left_frame = ttk.Frame(self.parent, width=350, relief="solid", padding=(10, 10))

        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(left_frame, text="CGTTI Alumni", font=("Arial", 14, "bold")).pack(pady=5)
        ttk.Label(left_frame, text="MEMBER REGISTRATION", font=("Arial", 12, "bold"), foreground="blue").pack()

        fields = ["Training number", "Membership year", "Trade", "Name", "District", "Membership number", "Address", "Mobile", "Nic"]
        self.entries = {}

        # Create the input fields and bind arrow keys for navigation
        for field in fields:
            ttk.Label(left_frame, text=field, font=("Arial", 10)).pack(anchor="w", padx=10, pady=2)
            if field == "Trade":
                entry = ttk.Combobox(left_frame, values=[ 
                    "TOOL MACHINE TRADE", "MILLWRIGHT TRADE", "AUTO MOBILE TRADE", "BRP TRADE", 
                    "AUTO ELECTRICAL TRADE", "REF AND A/C TRADE", "MECHATRONIC TRADE", 
                    "DISAL PUMP TRADE", "WELDING TRADE", "POWER ELECTRICAL TRADE"])
            elif field == "District":
                entry = ttk.Combobox(left_frame, values=[ 
                    "Ampara", "Anuradhapura", "Badulla", "Batticaloa", "Colombo", "Galle", 
                    "Gampaha", "Hambantota", "Jaffna", "Kalutara", "Kandy", "Kegalle", 
                    "Kilinochchi", "Kurunegala", "Mannar", "Matale", "Matara", "Monaragala", 
                    "Mullaitivu", "Nuwara Eliya", "Polonnaruwa", "Puttalam", "Ratnapura", 
                    "Trincomalee", "Vavuniya"])
            else:
                entry = ttk.Entry(left_frame)
            entry.pack(padx=10, pady=2, fill="x")
            self.entries[field] = entry

            # Bind arrow keys for navigation
            entry.bind("<Up>", self.move_focus)
            entry.bind("<Down>", self.move_focus)

        self.payment_status = tk.StringVar(value="Paid Up")
        ttk.Radiobutton(left_frame, text="PAID UP", variable=self.payment_status, value="Paid Up").pack(anchor="w", padx=10)
        ttk.Radiobutton(left_frame, text="NON-PAID", variable=self.payment_status, value="Non-Paid").pack(anchor="w", padx=10)

        self.dead_var = tk.BooleanVar()
        self.alive_var = tk.BooleanVar()
        ttk.Label(left_frame, text="Member Status", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=2)
        ttk.Checkbutton(left_frame, text="Deceased", variable=self.dead_var).pack(anchor="w", padx=10)
        ttk.Checkbutton(left_frame, text="Alive", variable=self.alive_var).pack(anchor="w", padx=10)

        # Button frame with grid layout for better alignment
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(pady=10, fill="x")
        for text, command in zip(["SAVE", "UPDATE", "DELETE", "LOAD"], 
                                [self.save_member, self.update_member, self.delete_member, self.load_members]):
            button = ttk.Button(btn_frame, text=text, width=10, command=command)
            button.pack(side="left", padx=5, pady=5)

        right_frame = ttk.Frame(self.parent)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.search_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.search_var, width=50).pack(pady=10, fill="x")
        ttk.Button(right_frame, text="SEARCH", command=self.search_member).pack(pady=5)

        tree_frame = ttk.Frame(right_frame)
        tree_frame.pack(fill="both", expand=True)

        columns = ["Trainingnumber", "Memberyear", "Trade", "MemberName", "District", "Membershipnumber",
                "Address", "Mobile", "Nic", "Paide", "LivingorDead"]
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        for col, width in zip(columns, [120, 100, 150, 200, 120, 150, 250, 120, 120, 100, 120]):
            self.tree.heading(col, text=col, anchor=tk.CENTER)
            self.tree.column(col, width=width, anchor=tk.CENTER)

        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)

        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.on_row_select)

        pagination_frame = ttk.Frame(right_frame)
        pagination_frame.pack(fill="x", pady=10)

        self.prev_button = ttk.Button(pagination_frame, text="Previous", command=self.prev_page)
        self.prev_button.pack(side="left", padx=10)

        self.page_label = ttk.Label(pagination_frame, text="Page 1 of 1", font=("Arial", 12))
        self.page_label.pack(side="left", padx=10)

        self.next_button = ttk.Button(pagination_frame, text="Next", command=self.next_page)
        self.next_button.pack(side="left", padx=10)

        ttk.Label(right_frame, text="CGTTI Alumni Association", font=("Arial", 12)).pack(pady=10)

        # Add the arrow key bindings globally to allow navigation
        self.parent.bind("<Up>", self.move_focus)
        self.parent.bind("<Down>", self.move_focus)


    def move_focus(self, event):
        # Move focus to the next or previous widget based on the key pressed
        current_widget = self.parent.focus_get()

        # If Up key is pressed, move focus to the previous field
        if event.keysym == "Up":
            widget_list = list(self.entries.values())
            current_index = widget_list.index(current_widget)
            if current_index > 0:
                widget_list[current_index - 1].focus_set()

        # If Down key is pressed, move focus to the next field
        elif event.keysym == "Down":
            widget_list = list(self.entries.values())
            current_index = widget_list.index(current_widget)
            if current_index < len(widget_list) - 1:
                widget_list[current_index + 1].focus_set()

    def focus_prev_field(self, event):
        current_widget = self.parent.focus_get()
        fields = list(self.entries.values())
        current_index = fields.index(current_widget)
        if current_index > 0:
            fields[current_index - 1].focus_set()

    def focus_next_field(self, event):
        current_widget = self.parent.focus_get()
        fields = list(self.entries.values())
        current_index = fields.index(current_widget)
        if current_index < len(fields) - 1:
            fields[current_index + 1].focus_set()

    def on_row_select(self, event):
        selected_item = self.tree.selection()[0]
        selected_values = self.tree.item(selected_item, "values")
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

        if selected_values[9] == "Paid Up":
            self.payment_status.set("Paid Up")
        else:
            self.payment_status.set("Non-Paid")

        if selected_values[10] == "living":
            self.dead_var.set(False)
            self.alive_var.set(True)
        else:
            self.dead_var.set(True)
            self.alive_var.set(False)

    def save_member(self):
        # Collect member data from the input fields
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

        # Save member data to the database
        with db_manager.DBManager() as db:
            if db.insert_member(member_data):
                # Show success message
                messagebox.showinfo("Success", "Member saved successfully!")
                
                # Clear input fields after saving
                self.clear_input_fields()

                # Reload the list of members
                self.load_members()
            else:
                # Show error message if saving fails
                messagebox.showerror("Error", "Failed to save member.")

    def clear_input_fields(self):
        # Clear all the input fields (entries and comboboxes)
        for field in self.entries.values():
            if isinstance(field, ttk.Combobox):
                field.set("")  # Reset combobox
            else:
                field.delete(0, tk.END)  # Clear entry field

        # Reset radio buttons and check buttons
        self.payment_status.set("Paid Up")
        self.dead_var.set(False)
        self.alive_var.set(True)


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
                self.load_members()
                                # Clear input fields after saving
                self.clear_input_fields()

            else:
                messagebox.showerror("Error", "Failed to update member.")

    def delete_member(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select at least one member to delete.")
            return
        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected members?")
        if response:
            for selected_item in selected_items:
                selected_values = self.tree.item(selected_item, "values")
                member_id = selected_values[5]
                with db_manager.DBManager() as db:
                    if not db.delete_member(member_id):
                        messagebox.showerror("Error", f"Failed to delete member with ID {member_id}.")
            self.load_members()

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
