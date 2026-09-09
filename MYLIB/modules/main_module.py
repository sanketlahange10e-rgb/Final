import customtkinter as ctk
from MYLIB.modules.head_module import show_head
global root
def theme_color(color):
        global themecolor
        
        if color == "Light":
            themecolor="#f0f0f0"
            update_frame_colors(main_frame, themecolor)
        elif color == "Dark":
            themecolor="#1e1e1e"
            update_frame_colors(main_frame, themecolor)           
            

themecolor="#1e1e1e"


def show_main_frame(root, details, logout, relogin, refresh, Themecolor=theme_color, role=None):
    global main_frame
    main_frame = ctk.CTkFrame(root, fg_color=themecolor)
    main_frame.configure(fg_color=themecolor) 
    show_head(root, main_frame, details, logout, relogin, refresh, Themecolor, themecolor, role)
    main_frame.pack(fill=ctk.BOTH, expand=True)
   
    

def update_frame_colors(frame, themecolor):
    frame.configure(fg_color=themecolor)
    for child in frame.winfo_children():
        if isinstance(child, ctk.CTkFrame):
            update_frame_colors(child, themecolor)

