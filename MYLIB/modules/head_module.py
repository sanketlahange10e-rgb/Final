from logging import root
import customtkinter as ctk
import MYLIB.modules.menu_module
from MYLIB.modules.menu_module import toggle_Menu
from MYLIB.modules.menu_module import toggle_Account
import MYLIB.modules.bottom_module
from MYLIB.modules.bottom_module import  show_bottom

def show_head(root, main_frame, details, logout, relogin, refresh, Themecolor, themecolor,role):
    def on_hover(event):
        if toggle_menu.cget("text") == "✖":
            event.widget.configure(cursor="hand2")
            title_label = ctk.CTkLabel(head_frame, text="Close", fg_color=themecolor, text_color="white", font=("BOLD", 28))
            title_label.pack(side=ctk.LEFT)
            toggle_menu.bind("<Leave>", lambda e: title_label.destroy())
        if toggle_menu.cget("text") == "☰":
            event.widget.configure(cursor="hand2")
            title_label = ctk.CTkLabel(head_frame, text="Menu", fg_color=themecolor, text_color="white", font=("BOLD", 28))
            title_label.pack(side=ctk.LEFT)
            toggle_menu.bind("<Leave>", lambda e: title_label.destroy())

    # Make head_frame a child of main_frame
    head_frame = ctk.CTkFrame(root, fg_color=themecolor)
    main_frame.head_frame = head_frame
    head_frame.pack(side=ctk.TOP, fill=ctk.X)
    head_frame.pack_propagate(False)
    head_frame.configure(height=50)

    toggle_menu = ctk.CTkButton(head_frame, text="☰", fg_color=themecolor, hover_color="#333333", text_color="white", font=("BOLD", 28), width=25, command=lambda: toggle_Menu(root, main_frame, toggle_menu, head_frame, main_frame.bottom_frame, details, relogin,role, themecolor, Themecolor))
    toggle_menu.pack(side=ctk.LEFT, padx=5, pady=0)
    toggle_menu.bind("<Enter>", on_hover)

    Account_Button = ctk.CTkButton(head_frame, text="👤", fg_color=themecolor, hover_color="#333333", text_color="white", font=("BOLD", 28), width=50, command=lambda: toggle_Account(main_frame, head_frame, themecolor, logout, refresh))
    Account_Button.pack(side=ctk.RIGHT, padx=10, pady=5)

    # Create bottom_frame as a child of main_frame
    bottom_frame = show_bottom(root, main_frame, role, details)
    main_frame.bottom_frame = bottom_frame
    bottom_frame.pack(side=ctk.BOTTOM, fill=ctk.X)
    bottom_frame.configure(height=50)
    
    return head_frame
