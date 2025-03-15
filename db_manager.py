import sqlite3
import os
import sys
from tkinter import messagebox
from typing import Optional, List, Tuple
import pandas as pd  # Import pandas for data manipulation and exporting to Excel

class DBManager:
    @staticmethod
    def get_db_path():
        """ Get a persistent database path in the user's home directory. """
        if sys.platform == "win32":
            base_dir = os.path.join(os.getenv("APPDATA"), "MyApp")  # Windows
        else:
            base_dir = os.path.join(os.path.expanduser("~"), ".myapp")  # Linux/Mac

        # Ensure the directory exists
        os.makedirs(base_dir, exist_ok=True)

        return os.path.join(base_dir, "member.db")  # Store DB in a fixed location

    def __init__(self):
        self.db_path = self.get_db_path()
        self.conn = self.create_connection()
        self.create_tables()
        
    def create_connection(self) -> sqlite3.Connection:
        """Create and return a database connection with error handling"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA foreign_keys = ON;")
            return conn
        except sqlite3.Error as e:
            messagebox.showerror("Connection Error", f"Failed to create database connection: {str(e)}")
            raise

    def create_tables(self):
        """Create database tables with schema versioning"""
        schema_version = 1  # Increment when changing schema
        
        with self.conn:
            self.conn.execute(""" CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                training_number TEXT UNIQUE NOT NULL,            
                member_year TEXT NOT NULL,
                trade TEXT,
                member_name TEXT NOT NULL,
                district TEXT,
                membership_number TEXT UNIQUE NOT NULL, 
                address TEXT,
                nic TEXT UNIQUE NOT NULL,
                mobile TEXT,
                paid_status INTEGER DEFAULT 0 CHECK(paid_status IN (0, 1)),
                living_status TEXT DEFAULT 'living' CHECK(living_status IN ('living', 'deceased')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) """)
            
            self.conn.execute(""" CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) """)
            
            # Add indexes for common search fields
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_member_name ON members(member_name)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_membership_number ON members(membership_number)")
            
            # Store schema version
            self.conn.execute("PRAGMA user_version = {}".format(schema_version))

    # Export Data to Excel ------------------------------------------------------
    def export_to_excel(self, file_path: str) -> bool:
        """Export all member data to an Excel file"""
        try:
            # Fetch all members from the database
            cursor = self.conn.execute("SELECT * FROM members")
            columns = [column[0] for column in cursor.description]
            
            # Convert the data to a list of dictionaries
            members_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            # Convert the data into a pandas DataFrame
            df = pd.DataFrame(members_data)
            
            # Write the DataFrame to an Excel file
            df.to_excel(file_path, index=False, engine='openpyxl')
            
            messagebox.showinfo("Success", f"Data successfully exported to {file_path}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")
            return False

    # CRUD Operations ----------------------------------------------------------
    def insert_member(self, member_data: dict) -> bool:
        """Insert a new member into the database"""
        required_fields = [
            'training_number', 'member_year', 'membership_number', 'member_name', 'nic'
        ]
        
        if not all(field in member_data for field in required_fields):
            messagebox.showerror("Input Error", "Missing required fields")
            return False

        try:
            query = """
                INSERT INTO members (
                    training_number, member_year, membership_number,
                    member_name, trade, address, district, nic, mobile,
                    paid_status, living_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                member_data['training_number'],
                member_data['member_year'],
                member_data['membership_number'],
                member_data['member_name'],
                member_data.get('trade', ''),
                member_data.get('address', ''),
                member_data.get('district', ''),
                member_data['nic'],
                member_data.get('mobile', ''),
                member_data.get('paid_status', 0),
                member_data.get('living_status', 'living')
            )
            
            self.conn.execute(query, params)
            self.conn.commit()
            return True
            
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Database Error", f"Duplicate entry: {str(e)}")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Insert failed: {str(e)}")
            return False

    def update_member(self, membership_number: str, member_data: dict) -> bool:
        """Update an existing member in the database"""
        try:
            query = """
                UPDATE members SET
                    training_number = ?, member_year = ?, membership_number = ?,
                    member_name = ?, trade = ?, address = ?, district = ?, nic = ?,
                    mobile = ?, paid_status = ?, living_status = ?
                WHERE membership_number = ?
            """
            params = (
                member_data['training_number'],
                member_data['member_year'],
                member_data['membership_number'],
                member_data['member_name'],
                member_data.get('trade', ''),
                member_data.get('address', ''),
                member_data.get('district', ''),
                member_data['nic'],
                member_data.get('mobile', ''),
                member_data.get('paid_status', 0),
                member_data.get('living_status', 'living'),
                membership_number
            )
            
            self.conn.execute(query, params)
            self.conn.commit()
            return True
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Update failed: {str(e)}")
            return False

    def delete_member(self, membership_number: str) -> bool:
        """Delete a member from the database"""
        try:
            self.conn.execute("DELETE FROM members WHERE membership_number = ?", (membership_number,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Delete failed: {str(e)}")
            return False

    def fetch_members(self) -> List[dict]:
        """Fetch all members from the database"""
        try:
            cursor = self.conn.execute("SELECT * FROM members")
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Fetch failed: {str(e)}")
            return []

    def get_member(self, membership_number: str) -> Optional[Tuple]:
        """Retrieve a member by membership number"""
        try:
            cursor = self.conn.execute(
                "SELECT * FROM members WHERE membership_number = ?",
                (membership_number,)
            )
            return cursor.fetchone()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Query failed: {str(e)}")
            return None

    # Admin User Management ----------------------------------------------------
    def register_user(self, username: str, password: str) -> bool:
        """Register a new admin user"""
        try:
            query = "INSERT INTO admins (username, password) VALUES (?, ?)"
            self.conn.execute(query, (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Registration Error", "Username already exists.")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Registration failed: {str(e)}")
            return False

    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate an admin user"""
        try:
            query = "SELECT * FROM admins WHERE username = ? AND password = ?"
            cursor = self.conn.execute(query, (username, password))
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Authentication failed: {str(e)}")
            return False

    # Utility Methods ----------------------------------------------------------
    def backup_database(self, backup_path: str) -> bool:
        """Create a database backup"""
        try:
            with sqlite3.connect(backup_path) as backup_conn:
                self.conn.backup(backup_conn)
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Backup Failed", f"Could not create backup: {str(e)}")
            return False

    def close(self) -> None:
        """Close the database connection"""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# Example usage to export to Excel:
if __name__ == "__main__":
    # Initialize DBManager and export data to Excel
    with DBManager() as db:
        db.export_to_excel("members_data.xlsx")  # Specify your desired file path