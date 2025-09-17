from tkinter import *
from tkinter import ttk, messagebox
from random import choice, randint, shuffle
import pyperclip
import json
import os
import time

# ---------------------------- CONSTANTS ------------------------------- #
FONT_NAME = "Segoe UI"
BG_COLOR = "#2c3e50"  
ACCENT_COLOR = "#e74c3c" 
BUTTON_COLOR = "#3498db"  
SECONDARY_BUTTON = "#2ecc71"  
ENTRY_BG = "#ecf0f1"  
TEXT_COLOR = "#2c3e50"  
LIGHT_TEXT = "#ecf0f1"  
SUCCESS_COLOR = "#27ae60"  
WARNING_COLOR = "#f39c12"  
INFO_COLOR = "#3498db"  

# ---------------------------- MODERN ALERT BOX ------------------------------- #
class ModernAlert:
    def __init__(self, parent, alert_type="info", title="", message="", timeout=None):
        self.parent = parent
        self.alert_type = alert_type
        self.title = title
        self.message = message
        self.timeout = timeout
        
        # Set colors based on alert type
        if alert_type == "success":
            self.color = SUCCESS_COLOR
            self.icon = "✅"
        elif alert_type == "warning":
            self.color = WARNING_COLOR
            self.icon = "⚠️"
        elif alert_type == "error":
            self.color = ACCENT_COLOR
            self.icon = "❌"
        else:  # info
            self.color = INFO_COLOR
            self.icon = "ℹ️"
        
        self.create_alert()
    
    def create_alert(self):
        # Create overlay
        self.overlay = Toplevel(self.parent)
        self.overlay.title(self.title)
        self.overlay.geometry("400x250")
        self.overlay.configure(bg='#000000')
        self.overlay.attributes('-alpha', 0.0)  # Start transparent
        self.overlay.overrideredirect(True)
        self.overlay.grab_set()  # Make it modal
        
        # Center the alert
        self.overlay.update_idletasks()
        width = self.overlay.winfo_width()
        height = self.overlay.winfo_height()
        x = (self.overlay.winfo_screenwidth() // 2) - (width // 2)
        y = (self.overlay.winfo_screenheight() // 2) - (height // 2)
        self.overlay.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Create alert container
        self.container = Frame(self.overlay, bg='white', relief='flat', bd=0)
        self.container.place(relx=0.5, rely=0.5, anchor=CENTER, width=380, height=200)
        
        # Add icon
        icon_label = Label(self.container, text=self.icon, font=("Arial", 24), 
                          bg='white', fg=self.color)
        icon_label.place(x=30, y=30)
        
        # Add title
        title_label = Label(self.container, text=self.title, font=(FONT_NAME, 16, "bold"), 
                           bg='white', fg=self.color, justify=LEFT)
        title_label.place(x=70, y=30)
        
        # Add message
        msg_label = Label(self.container, text=self.message, font=(FONT_NAME, 12), 
                         bg='white', fg=TEXT_COLOR, wraplength=300, justify=LEFT)
        msg_label.place(x=30, y=70)
        
        # Add OK button
        ok_btn = Button(self.container, text="OK", font=(FONT_NAME, 10, "bold"),
                       bg=self.color, fg="white", relief=FLAT, cursor="hand2",
                       command=self.close_alert, padx=20, pady=5)
        ok_btn.place(x=150, y=150)
        
        # Add some styling
        self.container.configure(highlightbackground=self.color, highlightcolor=self.color, highlightthickness=2)
        
        # Animate in
        self.animate_in()
        
        # Set timeout if specified
        if self.timeout:
            self.overlay.after(self.timeout, self.close_alert)
    
    def animate_in(self):
        for i in range(10):
            self.overlay.attributes('-alpha', i/10)
            self.overlay.update()
            time.sleep(0.02)
    
    def animate_out(self):
        for i in range(10, -1, -1):
            self.overlay.attributes('-alpha', i/10)
            self.overlay.update()
            time.sleep(0.02)
        self.overlay.destroy()
    
    def close_alert(self):
        self.animate_out()

# ---------------------------- MODERN CONFIRM BOX ------------------------------- #
class ModernConfirm:
    def __init__(self, parent, title="", message="", callback=None):
        self.parent = parent
        self.title = title
        self.message = message
        self.callback = callback
        self.result = None
        
        self.create_confirm()
    
    def create_confirm(self):
        # Create overlay
        self.overlay = Toplevel(self.parent)
        self.overlay.title(self.title)
        self.overlay.geometry("400x250")
        self.overlay.configure(bg='#000000')
        self.overlay.attributes('-alpha', 0.0)  # Start transparent
        self.overlay.overrideredirect(True)
        self.overlay.grab_set()  # Make it modal
        
        # Center the confirm
        self.overlay.update_idletasks()
        width = self.overlay.winfo_width()
        height = self.overlay.winfo_height()
        x = (self.overlay.winfo_screenwidth() // 2) - (width // 2)
        y = (self.overlay.winfo_screenheight() // 2) - (height // 2)
        self.overlay.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Create confirm container
        self.container = Frame(self.overlay, bg='white', relief='flat', bd=0)
        self.container.place(relx=0.5, rely=0.5, anchor=CENTER, width=380, height=200)
        
        # Add icon
        icon_label = Label(self.container, text="❓", font=("Arial", 24), 
                          bg='white', fg=INFO_COLOR)
        icon_label.place(x=30, y=30)
        
        # Add title
        title_label = Label(self.container, text=self.title, font=(FONT_NAME, 16, "bold"), 
                           bg='white', fg=INFO_COLOR, justify=LEFT)
        title_label.place(x=70, y=30)
        
        # Add message
        msg_label = Label(self.container, text=self.message, font=(FONT_NAME, 12), 
                         bg='white', fg=TEXT_COLOR, wraplength=300, justify=LEFT)
        msg_label.place(x=30, y=70)
        
        # Add buttons
        cancel_btn = Button(self.container, text="Cancel", font=(FONT_NAME, 10, "bold"),
                           bg="#95a5a6", fg="white", relief=FLAT, cursor="hand2",
                           command=lambda: self.set_result(False), padx=15, pady=5)
        cancel_btn.place(x=100, y=150)
        
        ok_btn = Button(self.container, text="OK", font=(FONT_NAME, 10, "bold"),
                       bg=INFO_COLOR, fg="white", relief=FLAT, cursor="hand2",
                       command=lambda: self.set_result(True), padx=20, pady=5)
        ok_btn.place(x=200, y=150)
        
        # Add some styling
        self.container.configure(highlightbackground=INFO_COLOR, highlightcolor=INFO_COLOR, highlightthickness=2)
        
        # Animate in
        self.animate_in()
    
    def animate_in(self):
        for i in range(10):
            self.overlay.attributes('-alpha', i/10)
            self.overlay.update()
            time.sleep(0.02)
    
    def animate_out(self):
        for i in range(10, -1, -1):
            self.overlay.attributes('-alpha', i/10)
            self.overlay.update()
            time.sleep(0.02)
        self.overlay.destroy()
        if self.callback:
            self.callback(self.result)
    
    def set_result(self, result):
        self.result = result
        self.animate_out()

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    ModernAlert(window, "success", "Password Copied", "Password generated and copied to clipboard!", 2000)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    
    if len(website) == 0 or len(password) == 0:
        ModernAlert(window, "warning", "Empty Fields", "Please make sure you haven't left any fields empty.")
        return
    
    # Confirm before saving with modern dialog
    def handle_confirmation(result):
        if result:
            new_data = {
                website: {
                    "email": email,
                    "password": password,
                }
            }

            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}

            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
                
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            ModernAlert(window, "success", "Success", "Password saved successfully!", 2000)
    
    ModernConfirm(window, website, f"These are the details entered: \nEmail: {email} \nPassword: {password} \nIs it ok to save?", handle_confirmation)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get().strip()
    if len(website) == 0:
        ModernAlert(window, "warning", "Input Error", "Please enter a website name to search.")
        return
        
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        ModernAlert(window, "error", "Error", "No Data File Found.")
        return
    except json.JSONDecodeError:
        ModernAlert(window, "error", "Error", "Data file is corrupted.")
        return

    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        ModernAlert(window, "info", website, f"Email: {email}\nPassword: {password}\n\nPassword copied to clipboard!")
        pyperclip.copy(password)
    else:
        ModernAlert(window, "info", "Not Found", f"No details for '{website}' exists.")

# ---------------------------- VIEW ALL PASSWORDS ------------------------------- #
def view_all_passwords():
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        ModernAlert(window, "error", "Error", "No Data File Found.")
        return
    except json.JSONDecodeError:
        ModernAlert(window, "error", "Error", "Data file is corrupted.")
        return
        
    if not data:
        ModernAlert(window, "info", "No Passwords", "No passwords saved yet.")
        return
        
    # Create a new window to display all passwords
    view_window = Toplevel(window)
    view_window.title("All Saved Passwords")
    view_window.config(padx=20, pady=20, bg=BG_COLOR)
    view_window.geometry("500x400")
    view_window.resizable(True, True)
    
    # Center the view window
    view_window.update_idletasks()
    width = view_window.winfo_width()
    height = view_window.winfo_height()
    x = (view_window.winfo_screenwidth() // 2) - (width // 2)
    y = (view_window.winfo_screenheight() // 2) - (height // 2)
    view_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    # Create a frame for the list
    frame = Frame(view_window, bg=BG_COLOR)
    frame.pack(fill=BOTH, expand=True)
    
    # Title for the view window
    title_label = Label(frame, text="🔐 All Saved Passwords", font=(FONT_NAME, 16, "bold"), 
                       fg=LIGHT_TEXT, bg=BG_COLOR, pady=10)
    title_label.pack()
    
    # Create a text widget with scrollbar
    text_frame = Frame(frame, bg=BG_COLOR)
    text_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    scrollbar = Scrollbar(text_frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    text_widget = Text(text_frame, yscrollcommand=scrollbar.set, wrap=WORD, 
                      bg="#34495e", fg=LIGHT_TEXT, font=(FONT_NAME, 10), padx=10, pady=10)
    text_widget.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=text_widget.yview)
    
    # Insert passwords into the text widget
    for website, details in data.items():
        text_widget.insert(END, f"🌐 Website: {website}\n", "website")
        text_widget.insert(END, f"📧 Email: {details['email']}\n")
        text_widget.insert(END, f"🔑 Password: {details['password']}\n")
        text_widget.insert(END, "―" * 40 + "\n\n")
    
    # Configure tags for styling
    text_widget.tag_configure("website", foreground="#3498db")
    text_widget.config(state=DISABLED)  # Make it read-only
    
    # Close button
    close_btn = Button(frame, text="Close", command=view_window.destroy, 
                      bg=ACCENT_COLOR, fg="white", font=(FONT_NAME, 10, "bold"),
                      relief=FLAT, padx=20, pady=5, cursor="hand2")
    close_btn.pack(pady=10)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Vault")
window.config(bg=BG_COLOR)
window.resizable(False, False)

# Set proper window size to fit all UI elements
window_width = 550
window_height = 550
window.geometry(f"{window_width}x{window_height}")

# Center the window on screen
window.update_idletasks()
x = (window.winfo_screenwidth() // 2) - (window_width // 2)
y = (window.winfo_screenheight() // 2) - (window_height // 2)
window.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))

# Create a gradient background canvas
canvas = Canvas(window, width=window_width, height=window_height, highlightthickness=0)
canvas.pack(fill=BOTH, expand=True)

# Draw gradient background
for i in range(window_height):
    r = int(44 + (i * (52 - 44) / window_height))
    g = int(62 + (i * (73 - 62) / window_height))
    b = int(80 + (i * (94 - 80) / window_height))
    color = f'#{r:02x}{g:02x}{b:02x}'
    canvas.create_line(0, i, window_width, i, fill=color)

# Create a main frame with proper padding
main_frame = Frame(canvas, bg=BG_COLOR, padx=30, pady=30)
main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Logo
logo_frame = Frame(main_frame, bg=BG_COLOR)
logo_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20))

logo_label = Label(logo_frame, text="🔐 Password Vault", 
                  font=(FONT_NAME, 24, "bold"), fg=LIGHT_TEXT, bg=BG_COLOR)
logo_label.pack()

subtitle_label = Label(logo_frame, text="Secure Password Management", 
                      font=(FONT_NAME, 10), fg="#bdc3c7", bg=BG_COLOR)
subtitle_label.pack(pady=(5, 0))

# Labels with icons
website_label = Label(main_frame, text="🌐 Website:", 
                     font=(FONT_NAME, 10, "bold"), fg=LIGHT_TEXT, bg=BG_COLOR)
website_label.grid(row=1, column=0, sticky="w", pady=(20, 5), padx=(0, 10))

email_label = Label(main_frame, text="📧 Email/Username:", 
                   font=(FONT_NAME, 10, "bold"), fg=LIGHT_TEXT, bg=BG_COLOR)
email_label.grid(row=2, column=0, sticky="w", pady=(10, 5), padx=(0, 10))

password_label = Label(main_frame, text="🔑 Password:", 
                      font=(FONT_NAME, 10, "bold"), fg=LIGHT_TEXT, bg=BG_COLOR)
password_label.grid(row=3, column=0, sticky="w", pady=(10, 5), padx=(0, 10))

# Entries with modern styling
website_entry = Entry(main_frame, width=25, font=(FONT_NAME, 10), 
                     bg=ENTRY_BG, fg=TEXT_COLOR, relief=FLAT, highlightthickness=1, 
                     highlightcolor=ACCENT_COLOR, highlightbackground="#34495e")
website_entry.grid(row=1, column=1, pady=(20, 5))
website_entry.focus()

email_entry = Entry(main_frame, width=35, font=(FONT_NAME, 10), 
                   bg=ENTRY_BG, fg=TEXT_COLOR, relief=FLAT, highlightthickness=1, 
                   highlightcolor=ACCENT_COLOR, highlightbackground="#34495e")
email_entry.grid(row=2, column=1, columnspan=2, pady=(10, 5), sticky="ew")
email_entry.insert(0, "example@gmail.com")

password_entry = Entry(main_frame, width=25, font=(FONT_NAME, 10), show="•", 
                      bg=ENTRY_BG, fg=TEXT_COLOR, relief=FLAT, highlightthickness=1, 
                      highlightcolor=ACCENT_COLOR, highlightbackground="#34495e")
password_entry.grid(row=3, column=1, pady=(10, 5))

# Buttons with modern styling
search_button = Button(main_frame, text="🔍 Search", width=10, 
                      font=(FONT_NAME, 9, "bold"), command=find_password,
                      bg=BUTTON_COLOR, fg="white", relief=FLAT, cursor="hand2",
                      activebackground="#2980b9")
search_button.grid(row=1, column=2, padx=(5, 0), pady=(20, 5))

generate_password_button = Button(main_frame, text="🎲 Generate", 
                                 font=(FONT_NAME, 9, "bold"), command=generate_password,
                                 bg=SECONDARY_BUTTON, fg="white", relief=FLAT, 
                                 cursor="hand2", activebackground="#27ae60")
generate_password_button.grid(row=3, column=2, padx=(5, 0), pady=(10, 5))

add_button = Button(main_frame, text="💾 Save Password", 
                   font=(FONT_NAME, 12, "bold"), command=save,
                   bg=ACCENT_COLOR, fg="white", relief=FLAT, pady=10, 
                   cursor="hand2", activebackground="#c0392b")
add_button.grid(row=4, column=0, columnspan=3, pady=20, sticky="ew")

view_all_button = Button(main_frame, text="📋 View All Passwords",
                        font=(FONT_NAME, 10), command=view_all_passwords,
                        bg="#9b59b6", fg="white", relief=FLAT, pady=8, 
                        cursor="hand2", activebackground="#8e44ad")
view_all_button.grid(row=5, column=0, columnspan=3, pady=(0, 10), sticky="ew")

# Configure grid weights to make the layout responsive
main_frame.columnconfigure(1, weight=1)

# Footer
footer_label = Label(main_frame, text="© 2025 Password Vault • Secure Your Digital Life", 
                    font=(FONT_NAME, 8), fg="#95a5a6", bg=BG_COLOR)
footer_label.grid(row=6, column=0, columnspan=3, pady=(20, 0))

# Add some decorative elements
# Decorative line
canvas.create_line(50, 80, window_width-50, 80, fill=ACCENT_COLOR, width=2)

# Bind Enter key to save function
window.bind('<Return>', lambda event: save())

# Add hover effects to buttons
def on_enter(e):
    e.widget['background'] = e.widget.hover_color

def on_leave(e):
    if e.widget == search_button:
        e.widget['background'] = BUTTON_COLOR
    elif e.widget == generate_password_button:
        e.widget['background'] = SECONDARY_BUTTON
    elif e.widget == add_button:
        e.widget['background'] = ACCENT_COLOR
    elif e.widget == view_all_button:
        e.widget['background'] = "#9b59b6"

# Apply hover effects
search_button.hover_color = "#2980b9"
search_button.bind("<Enter>", on_enter)
search_button.bind("<Leave>", on_leave)

generate_password_button.hover_color = "#27ae60"
generate_password_button.bind("<Enter>", on_enter)
generate_password_button.bind("<Leave>", on_leave)

add_button.hover_color = "#c0392b"
add_button.bind("<Enter>", on_enter)
add_button.bind("<Leave>", on_leave)

view_all_button.hover_color = "#8e44ad"
view_all_button.bind("<Enter>", on_enter)
view_all_button.bind("<Leave>", on_leave)

window.mainloop()