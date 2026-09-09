import customtkinter as ctk 
from MYLIB.modules.Role_loginpage import Role_loginpage
from MYLIB.modules.main_module import show_main_frame
from MYLIB.modules.login_module import Login_page
import tkinter.messagebox as messagebox
def login_controller(refresh=None):
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    screen_h = root.winfo_screenheight()
    screen_w = root.winfo_screenwidth()
    win_w, win_h = 600, 800
    pos_x = int((screen_w - win_w) / 2)
    pos_y = int((screen_h - win_h) / 2)
    root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")

    def log_out():
        if messagebox.askyesno("Logout Confirmation", "Are you sure you want to logout?"):
            for children in root.winfo_children():
                children.destroy()
            Role_loginpage(root, on_hrs=handle_role_selection)

    def relogin(role):
        for children in root.winfo_children():
            children.destroy()
        Login_page(root, Role=role, on_login=lambda details: handle_login(details, role), on_back=lambda: Role_loginpage(root, on_hrs=handle_role_selection))

    login_state = {}

    def handle_role_selection(role):
        if role in ["Admin", "Student", "Driver"]:
            Login_page(root, Role=role, on_login=lambda details: handle_login(details, role), on_back=lambda: Role_loginpage(root, on_hrs=handle_role_selection))

    def handle_login(details, role, refresh=refresh):
        screen_w = root.winfo_screenwidth()
        print("Selected role:", role)
        win_w, win_h = 700, 1000
        pos_x = int((screen_w - win_w) / 2)
        root.geometry(f"{win_w}x{win_h}+{pos_x}+0")
        root.title("Transport Inefficiency Analyzer")
        login_state["details"] = details
        show_main_frame(root, details, logout=log_out, role=role, relogin=lambda: relogin(role), refresh=refresh)

    Role_loginpage(root, on_hrs=handle_role_selection)
    root.mainloop()
