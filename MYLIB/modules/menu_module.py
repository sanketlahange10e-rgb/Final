
from logging import root
import customtkinter as ctk
from MYLIB.modules.bottom_module import show_bottom
import MYLIB.modules.profile_module
import MYLIB.modules.setting_module
from MYLIB.modules.setting_module import show_settings
from MYLIB.modules.profile_module import show_profile
import MYLIB.modules.login_module
from MYLIB.modules.pages_module import (
    about_page,
    driver_info_page,
    timetable_page,
    announcements_page,
    bus_info_page
)


def toggle_Menu(root,main_frame, toggle_menu,head_frame,bottom_frame,details,relogin,role,themecolor,Themecolor):
    # Set a default text color
    text_color = "white"

    # Helper to close the menu
    def Collapse_Menu():
        if hasattr(main_frame, 'toggle_menu_frame'):
            main_frame.toggle_menu_frame.destroy()
            delattr(main_frame, 'toggle_menu_frame')
        toggle_menu.configure(
            text="☰",
            command=lambda: toggle_Menu(root, main_frame, toggle_menu,
                                        head_frame, bottom_frame,
                                        details, relogin, role,
                                        themecolor, Themecolor)
        )

    # If menu is already open, do nothing
    if hasattr(main_frame, 'toggle_menu_frame'):
        return

    toggle_menu_frame = ctk.CTkFrame(
        main_frame,
        fg_color=themecolor,
        height=-45,
        width=200,
        border_color="black",
        border_width=1
    )
    main_frame.toggle_menu_frame = toggle_menu_frame

    # ---------------- PROFILE ----------------
    profile_button = ctk.CTkButton(
        toggle_menu_frame,
        text="Profile",
        fg_color=themecolor,
        hover_color="#333333",
        text_color="white",
        font=("Times New Roman", 28),
        command=lambda: [show_profile(root, main_frame, head_frame,
                                      bottom_frame, details, role,
                                      relogin, themecolor), Collapse_Menu()]
    )
    profile_button.pack(pady=10, fill=ctk.X)
    profile_button.bind("<Enter>", lambda e: profile_button.configure(cursor="hand2"))

    # ---------------- ABOUT ----------------
    about_button = ctk.CTkButton(
        toggle_menu_frame,
        text="About",
        fg_color=themecolor,
        hover_color="#333333",
        text_color="white",
        font=("Times New Roman", 20),
        command=lambda: [about_page(main_frame), Collapse_Menu()]
    )
    about_button.pack(pady=5, fill=ctk.X)
    about_button.bind("<Enter>", lambda e: about_button.configure(cursor="hand2"))

    # ---------------- NOTES ----------------
    driver_button = ctk.CTkButton(
        toggle_menu_frame,
        text="Driver Info",
        fg_color=themecolor,
        hover_color="#333333",
        text_color=text_color,
        font=("Times New Roman", 20),
        command=lambda: driver_info_page(main_frame)
    )
    driver_button.pack(pady=5, fill=ctk.X)

    # ---------------- TIME ----------------
    timetable_button = ctk.CTkButton(
        toggle_menu_frame,
        text="Time Table",
        fg_color=themecolor,
        hover_color="#333333",
        text_color=text_color,
        font=("Times New Roman", 20),
        command=lambda: timetable_page(main_frame)
    )
    timetable_button.pack(pady=5, fill=ctk.X)

    # ---------------- ANNOUNCEMENTS ----------------
    ann_button = ctk.CTkButton(
        toggle_menu_frame,
        text="Announcements",
        fg_color=themecolor,
        hover_color="#333333",
        text_color="white",
        font=("Times New Roman", 20),
        command=lambda: [announcements_page(main_frame), Collapse_Menu()]
    )
    ann_button.pack(pady=5, fill=ctk.X)
    ann_button.bind("<Enter>", lambda e: ann_button.configure(cursor="hand2"))

    # ---------------- TEST NOTIFICATION ----------------
    notif_button = ctk.CTkButton(
        toggle_menu_frame,
        text="Bus Info Page",
        fg_color=themecolor,
        hover_color="#333333",
        text_color="white",
        font=("Times New Roman", 20),
        command=lambda: [bus_info_page(main_frame), Collapse_Menu()]
    )
    notif_button.pack(pady=5, fill=ctk.X)
    notif_button.bind("<Enter>", lambda e: notif_button.configure(cursor="hand2"))

    # ---------------- FINAL UI ----------------
    toggle_menu_frame.place(x=0, y=0, relheight=1)

    toggle_menu.configure(text="✖")
    toggle_menu.configure(command=lambda: Collapse_Menu())

def toggle_Account(main_frame,head_Frame,themecolor,logout,refresh):
    def Close_Profile_Menu():
        toggle_profile_frame.destroy() 

    close_job = None
    def schedule_close(_event=None):
        nonlocal close_job
        if close_job is None:
            close_job = toggle_profile_frame.after(150, Close_Profile_Menu)
    def cancel_close(_event=None):
        nonlocal close_job
        if close_job is not None:
            toggle_profile_frame.after_cancel(close_job)
            close_job = None

    toggle_profile_frame=ctk.CTkFrame(main_frame,fg_color=themecolor,border_color="black",border_width=1,width=180)
    
    refresh_button=ctk.CTkButton(toggle_profile_frame,
                                 text="Refresh",
                                 fg_color=themecolor,
                                 hover_color="#1680c2",
                                 text_color="white",
                                 border_width=0.4,
                                 font=("Times New Roman",28),
                                 command=refresh)
    refresh_button.pack(fill=ctk.X, pady=(0, 5))

    log_out_button=ctk.CTkButton(toggle_profile_frame,text="Logout",fg_color=themecolor,hover_color="#333333",text_color="white",border_width=0.4,font=("Times New Roman",28),command=logout)
    log_out_button.pack(fill=ctk.X)
    
    toggle_profile_frame.place(relx=1.01,rely=0,x=-150,y=0)
    toggle_profile_frame.propagate(True)
    toggle_profile_frame.bind("<Leave>", schedule_close)
    toggle_profile_frame.bind("<Enter>", cancel_close)

    refresh_button.bind("<Leave>", schedule_close)
    refresh_button.bind("<Enter>", cancel_close)
    log_out_button.bind("<Leave>", schedule_close)
    log_out_button.bind("<Enter>", cancel_close)
    
