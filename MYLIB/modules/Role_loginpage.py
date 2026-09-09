import customtkinter as ctk
import tkinter as tk
def Role_loginpage(root, on_hrs=None):
    global Role
    # Appearance
    root.title("Transportation Inefficiency Analyzer")

    # Title
    title = ctk.CTkLabel(root, text="Welcome to Transportation Inefficiency Analyzer", 
                        font=ctk.CTkFont(size=24, weight="bold"))
    title.pack(pady=(20, 5))

    subtitle = ctk.CTkLabel(root, text="Select Your Role", 
                            font=ctk.CTkFont(size=16))
    subtitle.pack(pady=(0, 20))

    # Frame for grid
    frame = ctk.CTkFrame(root)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    def create_button(parent, text, color):
        return ctk.CTkButton(
            parent,
            text=text,
            height=100,
            corner_radius=15,
            fg_color=color,
            hover_color="gray70",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=lambda: select_role(text)
        )

    # Button click function
    def select_role(role):
        Role=role
        frame.destroy()
        title.destroy()
        subtitle.destroy()
        if on_hrs is not None:
            on_hrs(Role)
            return
        else:
            print(f"Selected role: {role}")
            return

    # Create buttons
    btn_admin = create_button(frame, "Admin", "#8B5CF6")     # purple
    btn_student = create_button(frame, "Student", "#3B82F6") # blue   # green
    btn_driver = create_button(frame, "Driver", "#F59E0B")   # orange

    # Grid layout (2x2)
    btn_admin.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    btn_student.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
    btn_driver.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

    # Make grid responsive
    frame.grid_rowconfigure((0,1), weight=1)
    frame.grid_columnconfigure((0,1), weight=1)

    # No blocking wait; role selection is handled by callback
    # Button style
    
    
    # Wait for user to select a role