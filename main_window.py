import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from PIL import Image, ImageTk
from ttkthemes import ThemedTk  # Import ThemedTk from ttkthemes

def get_absolute_path(relative_path):
    """Get the absolute path for files inside the .exe and when running normally."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x300")
        self.root.iconbitmap(get_absolute_path("asesst/CG.ico"))
        self.root.configure(bg="#f0f0f0")

        # Title
        tk.Label(root, text="Get started!", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

        # Username
        tk.Label(root, text="User name", font=("Arial", 10), bg="#f0f0f0").pack()
        self.username_entry = tk.Entry(root, width=30)
        self.username_entry.pack(pady=5)

        # Password
        tk.Label(root, text="Password", font=("Arial", 10), bg="#f0f0f0").pack()
        self.password_entry = tk.Entry(root, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Remember Me and Forgot Password
        self.remember_me = tk.BooleanVar()
        tk.Checkbutton(root, text="Remember me", variable=self.remember_me, bg="#f0f0f0").pack(pady=5)
        tk.Label(root, text="Forgot your password", fg="blue", cursor="hand2", bg="#f0f0f0").pack()
        tk.Label(root, text="").pack()  # Spacer

        # Login Button
        tk.Button(root, text="Login", command=self.login, width=20, bg="#4CAF50", fg="white").pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Dummy validation (replace with actual logic)
        if username == "admin" and password == "password":
            self.root.destroy()  # Close the login window
            self.open_main_app()  # Open the main application
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def open_main_app(self):
        main_window = ThemedTk(theme="arc")
        app = MainApp(main_window)
        main_window.mainloop()

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CGTTI Alumni Association")
        self.root.geometry("1000x600")
        self.root.state("zoomed")
        
        self.root.iconbitmap(get_absolute_path("asesst/CG.ico"))
        self.current_frame = None
        self.menu_bar = None
        self.build_menu()
        self.image_path = get_absolute_path("asesst/cgtti.jpg")  # Use the function to get the correct path
        self.set_background_image()
        self.root.bind("<Configure>", self.on_resize)  # Bind the resize event

    def set_background_image(self):
        """Set the background image for the application."""
        try:
            # Load the image
            self.original_image = Image.open(self.image_path)
            self.bg_image = ImageTk.PhotoImage(self.original_image)
            
            # Create a label with the image
            self.bg_label = tk.Label(self.root, image=self.bg_image)
            self.bg_label.place(relwidth=1, relheight=1)
            
            # Ensure the label is behind other widgets
            self.bg_label.lower()
        except Exception as e:
            print(f"Error loading background image: {e}")

    def on_resize(self, event):
        """Handle window resize event."""
        try:
            # Get the new window size
            new_width = event.width
            new_height = event.height
            
            # Resize the image using LANCZOS resampling
            resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(resized_image)
            
            # Update the label with the new image
            self.bg_label.config(image=self.bg_image)
        except Exception as e:
            print(f"Error resizing background image: {e}")

    def build_menu(self):
        """Build the navigation menu."""
        self.menu_bar = tk.Menu(self.root)

        # Registration menu
        registration_menu = tk.Menu(self.menu_bar, tearoff=0)
        registration_menu.add_command(label="Member Registration", command=self.show_member_registration)
        
        # Dashboard menu
        self.dashboard_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.dashboard_menu.add_command(label="Dashboard", command=self.show_dashboard)
        
        # Add menus to the menu bar
        self.menu_bar.add_cascade(label="Menu", menu=registration_menu)
        self.menu_bar.add_cascade(label="Dashboard", menu=self.dashboard_menu)

        # Add the menu to the window
        self.root.config(menu=self.menu_bar)
        
    def show_member_registration(self):
        from member_ragistation import MemberRegistration
        self.switch_frame(MemberRegistration)
        
    def show_dashboard(self):
        from all_member import TradeDashboard
        self.switch_frame(TradeDashboard)

    def switch_frame(self, FrameClass):
        """Destroy the current frame and load a new one."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Pass only the parent argument to MemberRegistration
        if FrameClass.__name__ == "MemberRegistration":
            FrameClass(self.current_frame)  # Only pass parent
        else:
            FrameClass(self.current_frame, self)  # Pass both parent and controller for other frames

if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    login_app = LoginWindow(root)
    root.mainloop()