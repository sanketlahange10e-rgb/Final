import customtkinter as ctk
import MYLIB.modules.head_module
import MYLIB.modules.menu_module
import MYLIB.modules.bottom_module
from MYLIB.modules.bottom_module import show_bottom


def show_settings(root, main_frame, head_frame, bottom_frame,Themecolor,themecolor,showmainframe):
    main_frame.pack_forget()
    head_frame.pack_forget()
    bottom_frame.pack_forget()

    def settings_close():
        setting_frame.destroy()
        head_frame.pack(side=ctk.TOP, fill=ctk.X)
        main_frame.pack(fill=ctk.BOTH, expand=True)
        bottom_frame.pack(side=ctk.BOTTOM, fill=ctk.X)

    setting_frame = ctk.CTkFrame(root, fg_color=themecolor)
    settings_window = ctk.CTkFrame(setting_frame, fg_color=themecolor, border_color="black", border_width=1)

    settings_close_button = ctk.CTkButton(
        settings_window,
        text="⇐",
        fg_color=themecolor,
        hover_color="#333333",
        text_color="white",
        border_width=0.4,
        font=("Times New Roman", 28),
        command=settings_close
    )
    settings_close_button.pack(side=ctk.LEFT, pady=5)

    title_label = ctk.CTkLabel(
        settings_window,
        text="Settings",
        fg_color=themecolor,
        text_color="white",
        font=("Times New Roman", 32)
    )
    title_label.pack(pady=10)
    settings_window.pack(side=ctk.TOP, fill=ctk.X)
    settings_window.pack_propagate(False)
    settings_window.configure(height=50)
    setting_page_frame=ctk.CTkScrollableFrame(setting_frame,fg_color=themecolor,border_color="#333333",border_width=1)
    setting_page_frame.pack(fill=ctk.BOTH,expand=True,padx=20,pady=20)

    Theme_label = ctk.CTkLabel(
        setting_page_frame,
        text="Select Theme",
        fg_color=themecolor,
        text_color="white",
        font=("Times New Roman", 20)
    )
    Theme_label.pack(pady=10)
    def change_theme(choice):
        if choice == "Light":
            Themecolor("Light")
            
            
            ctk.set_appearance_mode("light")
        elif choice == "Dark":
            Themecolor("Dark")
           
            ctk.set_appearance_mode("dark")
        else:    
            Themecolor("Dark")
            
            
            ctk.set_appearance_mode("dark")

    Theme_option = ctk.CTkOptionMenu(
        setting_page_frame,
        values=["Dark", "Light"],
        command=change_theme
    )
    # Set initial value to match current appearance mode
    Theme_option.pack(padx=10, pady=10)

    
    setting_frame.pack(fill=ctk.BOTH, expand=True)
