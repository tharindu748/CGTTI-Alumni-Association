import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from ttkthemes import ThemedTk
import db_manager
import os
import sys
from openpyxl import Workbook  # For exporting data to Excel

def get_absolute_path(relative_path):
    """Get the absolute path for files inside the .exe and when running normally."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)

class DataImportFilterPage:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Set the window icon (access the root window via self.parent.master)
        if hasattr(self.parent.master, "iconbitmap"):
            self.parent.master.iconbitmap(get_absolute_path("asesst/CG.ico"))

        # Create Widgets
        self.create_widgets()

    def create_widgets(self):
        # Title
        ttk.Label(self.frame, text="Export Filtered Data to Excel", font=("Arial", 16, "bold")).pack(pady=10)

        # Filter Section
        filter_frame = ttk.Frame(self.frame)
        filter_frame.pack(fill="x", padx=10, pady=10)

        # District Filter (Combobox)
        ttk.Label(filter_frame, text="Filter by District").pack(side="left", padx=5)
        self.districts = [
            "Ampara", "Anuradhapura", "Badulla", "Batticaloa", "Colombo", "Galle", 
            "Gampaha", "Hambantota", "Jaffna", "Kalutara", "Kandy", "Kegalle", 
            "Kilinochchi", "Kurunegala", "Mannar", "Matale", "Matara", "Monaragala", 
            "Mullaitivu", "Nuwara Eliya", "Polonnaruwa", "Puttalam", "Ratnapura", 
            "Trincomalee", "Vavuniya"
        ]
        self.filter_district = ttk.Combobox(filter_frame, values=self.districts, width=28)
        self.filter_district.pack(side="left", padx=5)

        # Trade Filter (Combobox)
        ttk.Label(filter_frame, text="Filter by Trade").pack(side="left", padx=5)
        self.trades = [
            "TOOL MACHINE TRADE", "MILLWRIGHT TRADE", "AUTO MOBILE TRADE", "BRP TRADE", 
            "AUTO ELECTRICAL TRADE", "REF AND A/C TRADE", "MECHATRONIC TRADE", 
            "DISAL PUMP TRADE", "WELDING TRADE", "POWER ELECTRICAL TRADE"
        ]
        self.filter_trade = ttk.Combobox(filter_frame, values=self.trades, width=28)
        self.filter_trade.pack(side="left", padx=5)

        # Membership Year Filter (Entry)
        ttk.Label(filter_frame, text="Filter by Membership Year").pack(side="left", padx=5)
        self.filter_member_year = ttk.Entry(filter_frame, width=30)
        self.filter_member_year.pack(side="left", padx=5)

        # Export Button
        export_button = ttk.Button(self.frame, text="Export to Excel", command=self.export_filtered_data)
        export_button.pack(pady=10)

    def export_filtered_data(self):
        """Export filtered data to an Excel file"""
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if not file_path:
            return

        try:
            # Get filter values
            filter_district = self.filter_district.get().strip().lower()
            filter_trade = self.filter_trade.get().strip().lower()
            filter_member_year = self.filter_member_year.get().strip().lower()

            # Fetch data from the database
            with db_manager.DBManager() as db:
                members = db.fetch_members()

                # Apply filters
                filtered_data = []
                for member in members:
                    district_match = filter_district in str(member.get("district", "")).lower()
                    trade_match = filter_trade in str(member.get("trade", "")).lower()
                    member_year_match = filter_member_year in str(member.get("member_year", "")).lower()

                    if district_match and trade_match and member_year_match:
                        filtered_data.append(member)

                if not filtered_data:
                    messagebox.showinfo("Info", "No data matches the filters.")
                    return

                # Create a new Excel workbook and add a worksheet
                workbook = Workbook()
                sheet = workbook.active

                # Write headers
                headers = [
                    "Training number", "Membership year", "Membership number", "Name", "Nic",
                    "Trade", "District", "Address", "Mobile", "Paide", "LivingorDead"
                ]
                sheet.append(headers)

                # Write data rows
                for member in filtered_data:
                    row = [
                        member["training_number"],
                        member["member_year"],
                        member["membership_number"],
                        member["member_name"],
                        member["nic"],
                        member["trade"],
                        member["district"],
                        member["address"],
                        member["mobile"],
                        "Paid Up" if member["paid_status"] == 1 else "Non-Paid",
                        member["living_status"]
                    ]
                    sheet.append(row)

                # Save the workbook
                workbook.save(file_path)
                messagebox.showinfo("Success", f"Filtered data successfully exported to {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")


# Example usage
if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = DataImportFilterPage(root)
    root.mainloop()