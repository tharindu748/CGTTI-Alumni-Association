import tkinter as tk
from tkinter import ttk
from db_manager import DBManager  # Import your DBManager class

class TradeDashboard:
    def __init__(self, parent, controller):
        self.parent = parent  # This is the frame where widgets will be placed
        self.frame = ttk.Frame(self.parent)  # Internal frame
        self.frame.pack(fill="both", expand=True)
        self.controller = controller  # This is the MainApp instance (or controller)
        self.db_manager = DBManager()  # Initialize the database manager

        # Configure the parent window (if it's a Tk or Toplevel window)
        if isinstance(self.parent.master, tk.Tk) or isinstance(self.parent.master, tk.Toplevel):
            self.parent.master.title("CGTTI Alumni Association")
            self.parent.master.geometry("820x600")

        # Create and place widgets
        self.create_widgets()

        # Load data on startup
        self.load_data()

    def create_widgets(self):
        """Create and place widgets on the dashboard."""
        # Main frame for the dashboard
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Frame for trade counts
        trade_frame = ttk.LabelFrame(main_frame, text="Trade Counts", padding=10)
        trade_frame.pack(fill="x", pady=10)

        self.trade_labels = {}
        trades = [
            "TOOL MACHINE TRADE", "MILLWRIGHT TRADE", "AUTO MOBILE TRADE",
            "BRP TRADE", "AUTO ELECTRICAL TRADE", "REF AND A/C TRADE",
            "MECHATRONIC TRADE", "DISAL PUMP TRADE", "WELDING TRADE",
            "POWER ELECTRICAL TRADE"
        ]

        for trade in trades:
            self.trade_labels[trade] = ttk.Label(trade_frame, text=f"{trade}: 0", font=("Arial", 10))
            self.trade_labels[trade].pack(anchor="w", pady=2)

        # Frame for total counts
        total_frame = ttk.LabelFrame(main_frame, text="Total Counts", padding=10)
        total_frame.pack(fill="x", pady=10)

        self.total_count_label = ttk.Label(total_frame, text="Total Members: 0", font=("Arial", 12, "bold"))
        self.total_count_label.pack(pady=5)

        # Frame for payment status
        payment_frame = ttk.LabelFrame(main_frame, text="Payment Status", padding=10)
        payment_frame.pack(fill="x", pady=10)

        self.paid_label = ttk.Label(payment_frame, text="Paid Members: 0", font=("Arial", 10))
        self.paid_label.pack(anchor="w", pady=2)

        self.non_paid_label = ttk.Label(payment_frame, text="Non-Paid Members: 0", font=("Arial", 10))
        self.non_paid_label.pack(anchor="w", pady=2)

        # Frame for living status
        living_frame = ttk.LabelFrame(main_frame, text="Living Status", padding=10)
        living_frame.pack(fill="x", pady=10)

        self.living_label = ttk.Label(living_frame, text="Living Members: 0", font=("Arial", 10))
        self.living_label.pack(anchor="w", pady=2)

        self.deceased_label = ttk.Label(living_frame, text="Deceased Members: 0", font=("Arial", 10))
        self.deceased_label.pack(anchor="w", pady=2)

    def load_data(self):
        """Load data from the database and update the labels."""
        try:
            total_count = 0
            total_paid = 0
            total_non_paid = 0
            total_living = 0
            total_deceased = 0

            # Count members for each trade
            for trade in self.trade_labels.keys():
                count = self.get_trade_count(trade)
                self.trade_labels[trade].config(text=f"{trade}: {count}")
                total_count += count

                # Count paid and non-paid members for each trade
                paid_count = self.get_paid_count(trade)
                total_paid += paid_count
                total_non_paid += (count - paid_count)

                # Count living and deceased members for each trade
                living_count = self.get_living_count(trade)
                total_living += living_count
                total_deceased += (count - living_count)

            # Update total counts
            self.total_count_label.config(text=f"Total Members: {total_count}")
            self.paid_label.config(text=f"Paid Members: {total_paid}")
            self.non_paid_label.config(text=f"Non-Paid Members: {total_non_paid}")
            self.living_label.config(text=f"Living Members: {total_living}")
            self.deceased_label.config(text=f"Deceased Members: {total_deceased}")

        except Exception as e:
            print(f"Error loading data: {e}")

    def get_trade_count(self, trade):
        """Get the count of members for a specific trade."""
        try:
            with self.db_manager.conn:
                cursor = self.db_manager.conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM members WHERE trade = ?", (trade,))
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting trade count for {trade}: {e}")
            return 0

    def get_paid_count(self, trade):
        """Get the count of paid members for a specific trade."""
        try:
            with self.db_manager.conn:
                cursor = self.db_manager.conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM members WHERE trade = ? AND paid_status = 1", (trade,))
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting paid count for {trade}: {e}")
            return 0

    def get_living_count(self, trade):
        """Get the count of living members for a specific trade."""
        try:
            with self.db_manager.conn:
                cursor = self.db_manager.conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM members WHERE trade = ? AND living_status = 'living'", (trade,))
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting living count for {trade}: {e}")
            return 0

    def __del__(self):
        """Close the database connection when the object is destroyed."""
        try:
            if hasattr(self, 'db_manager') and self.db_manager:
                self.db_manager.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")

    def load_data(self):
        """Load data from the database and update the labels."""
        try:
            total_count = 0
            total_paid = 0
            total_non_paid = 0
            total_living = 0
            total_deceased = 0

            # Count members for each trade
            for trade in self.trade_labels.keys():
                count = self.get_trade_count(trade)
                self.trade_labels[trade].config(text=f"{trade}: {count}")
                total_count += count

                # Count paid and non-paid members for each trade
                paid_count = self.get_paid_count(trade)
                total_paid += paid_count
                total_non_paid += (count - paid_count)

                # Count living and deceased members for each trade
                living_count = self.get_living_count(trade)
                total_living += living_count
                total_deceased += (count - living_count)

            # Update total counts
            self.total_count_label.config(text=f"Total Members: {total_count}")
            self.paid_label.config(text=f"Paid Members: {total_paid}")
            self.non_paid_label.config(text=f"Non-Paid Members: {total_non_paid}")
            self.living_label.config(text=f"Living Members: {total_living}")
            self.deceased_label.config(text=f"Deceased Members: {total_deceased}")

        except Exception as e:
            print(f"Error loading data: {e}")

    def get_trade_count(self, trade):
        """Get the count of members for a specific trade."""
        try:
            with self.db_manager.conn:
                cursor = self.db_manager.conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM members WHERE trade = ?", (trade,))
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting trade count for {trade}: {e}")
            return 0

    def get_paid_count(self, trade):
        """Get the count of paid members for a specific trade."""
        try:
            with self.db_manager.conn:
                cursor = self.db_manager.conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM members WHERE trade = ? AND paid_status = 1", (trade,))
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting paid count for {trade}: {e}")
            return 0

    def get_living_count(self, trade):
        """Get the count of living members for a specific trade."""
        try:
            with self.db_manager.conn:
                cursor = self.db_manager.conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM members WHERE trade = ? AND living_status = 'living'", (trade,))
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting living count for {trade}: {e}")
            return 0

    def __del__(self):
        """Close the database connection when the object is destroyed."""
        try:
            if hasattr(self, 'db_manager') and self.db_manager:
                self.db_manager.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradeDashboard(root)
    root.mainloop()