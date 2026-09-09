import customtkinter as ctk
import tkinter.messagebox as messagebox
from MYLIB.modules.AccDetails_module import get_account_details
from MYLIB.modules.signup_module import signup_page


def Login_page(root, Role, on_login=None, on_back=None):  # ✅ added on_back
    role = Role
    root.title(f"{role} Login Page")

    Login_Frame = ctk.CTkFrame(root, fg_color="#1e1e1e")

    # -----------------------
    # 🔙 BACK BUTTON
    # -----------------------
    def go_back():
        Login_Frame.pack_forget()
        if on_back:
            on_back()

    Back_button = ctk.CTkButton(
        Login_Frame,
        text="← Back",
        width=80,
        command=go_back
    )
    Back_button.place(relx=0.02, rely=0.02)

    # -----------------------
    # TITLE
    # -----------------------
    Login_Label = ctk.CTkLabel(
        Login_Frame,
        text="Login",
        font=("Bold", 32)
    )
    Login_Label.pack(pady=50)

    # -----------------------
    # MAIN FRAME
    # -----------------------
    Login_page_Frame = ctk.CTkFrame(
        Login_Frame,
        fg_color="#2a2a2a",
        width=350,
        height=400,
        corner_radius=10,
        border_width=2,
        border_color="black"
    )
    Login_page_Frame.place(anchor="center", relx=0.5, rely=0.55)

    # -----------------------
    # USERNAME
    # -----------------------
    UserName_label = ctk.CTkLabel(Login_page_Frame, text="Username:")
    UserName_label.place(relx=0.1, rely=0.2)

    UserName_entry = ctk.CTkEntry(Login_page_Frame, width=250, height=40)
    UserName_entry.place(relx=0.1, rely=0.3)

    UserName_entry.bind("<Return>", lambda e: Password_entry.focus())

    # -----------------------
    # PASSWORD
    # -----------------------
    Password_label = ctk.CTkLabel(Login_page_Frame, text="Password:")
    Password_label.place(relx=0.1, rely=0.45)

    Password_entry = ctk.CTkEntry(Login_page_Frame, show="*", width=250, height=40)
    Password_entry.place(relx=0.1, rely=0.55)

    def toggle_password():
        if Password_entry.cget('show') == '*':
            Password_entry.configure(show='')
            peek.configure(text="hide")
        else:
            Password_entry.configure(show='*')
            peek.configure(text="show")

    peek = ctk.CTkLabel(Password_entry, text="show", cursor="hand2")
    peek.place(relx=0.9, rely=0.5, anchor="center")
    peek.bind("<Button-1>", lambda e: toggle_password())

    Password_entry.bind("<Return>", lambda e: Login_button.invoke())

    # -----------------------
    # LOGIN FUNCTION
    # -----------------------
    def ifclicked():
        Details = get_account_details(
            UserName_entry.get(),
            Password_entry.get(),
            role
        )

        if Details.get('success'):
            Login_Frame.pack_forget()
            if on_login:
                on_login(Details)
            return
        else:
            messagebox.showwarning("Login Failed", "Invalid Username or Password")
            Password_entry.delete(0, ctk.END)

    # -----------------------
    # LOGIN BUTTON
    # -----------------------
    Login_button = ctk.CTkButton(
        Login_page_Frame,
        text="Login",
        width=150,
        height=50,
        command=ifclicked
    )
    Login_button.place(relx=0.5, rely=0.75, anchor="center")

    # -----------------------
    # SIGNUP REDIRECT
    # -----------------------
    signup_redirect_label = ctk.CTkLabel(
        Login_page_Frame,
        text="Don't have an account? Sign Up",
        text_color="#7aa2ff",
        cursor="hand2"
    )
    signup_redirect_label.place(relx=0.5, rely=0.9, anchor="center")

    signup_redirect_label.bind(
        "<Button-1>",
        lambda e: (Login_Frame.pack_forget(), signup_page(root, Login_Frame, role))
    )

    Login_page_Frame.pack_propagate(False)
    Login_Frame.pack(fill=ctk.BOTH, expand=True)

    return Login_Frame