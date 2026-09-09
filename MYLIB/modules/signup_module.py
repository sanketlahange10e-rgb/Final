import customtkinter as ctk
import tkinter.messagebox as messagebox
import re
from MYLIB.modules.AccDetails_module import save_account_details
from MYLIB.modules.addset import change


def signup_page(root, Login_Frame, Role):
    role = Role
    root.title(f"{role} Sign Up Page")

    def toggle_password():
        if Password_entry.cget('show') == '*':
            Password_entry.configure(show='')
            peek.configure(text="hide")
        else:
            Password_entry.configure(show='*')
            peek.configure(text="show")

    Signup_Frame = ctk.CTkFrame(root, fg_color="#1e1e1e")

    Signup_Label = ctk.CTkLabel(Signup_Frame, text="Sign Up", font=("Bold", 32))
    Signup_Label.pack(pady=30)

    Signup_page_Frame = ctk.CTkScrollableFrame(
        Signup_Frame,
        fg_color="#2a2a2a",
        width=500,
        height=500,
        corner_radius=10,
        border_width=2,
        border_color="black"
    )
    Signup_page_Frame.place(relx=0.5, rely=0.5, anchor="center")

    form = ctk.CTkFrame(Signup_page_Frame, fg_color="#2a2a2a")
    form.pack(pady=20, padx=20, fill="both", expand=True)

    # ✅ IMPORTANT GRID FIX
    form.grid_columnconfigure(0, weight=1)
    form.grid_columnconfigure(1, weight=3)

    row = 0

    # -----------------------
    # STUDENT FIELDS
    # -----------------------
    if role == "Student":
        Name_label = ctk.CTkLabel(form, text="Full Name:")
        Name_label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

        Name_entry = ctk.CTkEntry(form)
        Name_entry.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        row += 1

        PrnNo_label = ctk.CTkLabel(form, text="PrnNo:")
        PrnNo_label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

        PrnNo_entry = ctk.CTkEntry(form)
        PrnNo_entry.grid(row=row, column=1, sticky="ew", padx=10, pady=5)

        def validate_prn():
            if not re.fullmatch(r"PRN\d{7}", PrnNo_entry.get()):
                messagebox.showwarning("Invalid PRN", "Format: PRN1234567")
                PrnNo_entry.delete(0, ctk.END)

        PrnNo_entry.bind("<FocusOut>", lambda e: validate_prn())
        row += 1

        Latitude_label = ctk.CTkLabel(form, text="Latitude:")
        Latitude_label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

        Latitude_entry = ctk.CTkEntry(form)
        Latitude_entry.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        row += 1

        Longitude_label = ctk.CTkLabel(form, text="Longitude:")
        Longitude_label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

        Longitude_entry = ctk.CTkEntry(form)
        Longitude_entry.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        row += 1

    # -----------------------
    # COMMON FIELDS
    # -----------------------
    UserName_label = ctk.CTkLabel(form, text="Username:")
    UserName_label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

    UserName_entry = ctk.CTkEntry(form)
    UserName_entry.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
    row += 1

    Password_label = ctk.CTkLabel(form, text="Password:")
    Password_label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

    pw_frame = ctk.CTkFrame(form, fg_color="#2a2a2a")
    pw_frame.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
    pw_frame.grid_columnconfigure(0, weight=1)

    Password_entry = ctk.CTkEntry(pw_frame, show="*")
    Password_entry.pack(side="left", fill="x", expand=True)

    peek = ctk.CTkLabel(pw_frame, text="show", cursor="hand2")
    peek.pack(side="left", padx=5)
    peek.bind("<Button-1>", lambda e: toggle_password())

    row += 1

    CPassword_label = ctk.CTkLabel(form, text="Confirm Password:")
    CPassword_label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

    CPassword_entry = ctk.CTkEntry(form, show="*")
    CPassword_entry.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
    row += 1

    # -----------------------
    # SIGNUP FUNCTION
    # -----------------------
    def ifclicked():
        username = UserName_entry.get().strip()
        password = Password_entry.get().strip()
        cpassword = CPassword_entry.get().strip()

        if not username or not password or not cpassword:
            messagebox.showwarning("Error", "All fields required")
            return

        if password != cpassword:
            messagebox.showwarning("Error", "Passwords do not match")
            return

        if role == "Student":
            name = Name_entry.get().strip()
            prn = PrnNo_entry.get().strip()
            lat = Latitude_entry.get().strip()
            lon = Longitude_entry.get().strip()

            if not name or not prn or not lat or not lon:
                messagebox.showwarning("Error", "All fields required")
                return

            try:
                lat = float(lat)
                lon = float(lon)
            except:
                messagebox.showwarning("Error", "Latitude & Longitude must be numbers")
                return

            result = save_account_details(prn, name, username, password, lat, lon, role)

            if result.get("success"):
                change(prn, username, lat, lon)

        else:
            result = save_account_details(None, None, username, password, None, None, role)

        if not result.get("success"):
            return

        messagebox.showinfo("Success", "Account created successfully")

        Signup_Frame.pack_forget()
        Login_Frame.pack(fill=ctk.BOTH, expand=True)

    # -----------------------
    # BUTTONS
    # -----------------------
    Signup_button = ctk.CTkButton(form, text="Sign Up", command=ifclicked)
    Signup_button.grid(row=row, column=0, columnspan=2, sticky="ew", padx=20, pady=15)

    login_label = ctk.CTkLabel(
        form,
        text="Already have an account? Login",
        text_color="#7aa2ff",
        cursor="hand2"
    )
    login_label.grid(row=row + 1, column=0, columnspan=2, pady=5)

    login_label.bind(
        "<Button-1>",
        lambda e: (Signup_Frame.pack_forget(), Login_Frame.pack(fill=ctk.BOTH, expand=True))
    )

    Signup_Frame.pack(fill=ctk.BOTH, expand=True)