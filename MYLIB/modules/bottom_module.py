import customtkinter as ctk
from MYLIB.modules.pages_module import (
    dashboard_page, Map_page, Bus_page, export_page, help_page,
    student_page, analysis_page, export_page
)

def show_bottom(root, main_frame,role,details):
    if role == "Admin":
        def switch(page):
            for widget in main_frame.winfo_children():
                widget.destroy()

            if page == "Dashboard":
                dashboard_page(main_frame)
            elif page == "Map":
                Map_page(main_frame,role,details)
            elif page == "Buses":
                Bus_page(main_frame,role)
            elif page == "Students":
                student_page(main_frame)
            elif page == "Analysis":
                analysis_page(main_frame)
            elif page == "Export Data":
                export_page(main_frame)

        bottom = ctk.CTkFrame(root, fg_color="#222222")

        buttons = ["Dashboard", "Map", "Buses", "Students", "Analysis", "Export Data"]

        for i, name in enumerate(buttons):
            btn = ctk.CTkButton(bottom, text=name,
                                command=lambda n=name: switch(n))
            btn.place(relx=i/6, rely=0, relwidth=1/6)

        bottom.pack(side=ctk.BOTTOM, fill=ctk.X)
        bottom.configure(height=50)

        root.after(200, lambda: switch("Dashboard"))

        return bottom
    elif role == "Student":
        def switch(page):
            for widget in main_frame.winfo_children():
                widget.destroy()

            if page == "Dashboard":
                dashboard_page(main_frame)
            elif page == "Map":
                Map_page(main_frame,role,details)
            elif page == "Driver":
                student_page(main_frame)
            elif page == "Help":
                help_page(main_frame)
                

        bottom = ctk.CTkFrame(root, fg_color="#222222")

        buttons = ["Dashboard", "Map", "Help"]

        for i, name in enumerate(buttons):
            btn = ctk.CTkButton(bottom, text=name,
                                command=lambda n=name: switch(n))
            btn.place(relx=i/3, rely=0, relwidth=1/3 )

        bottom.pack(side=ctk.BOTTOM, fill=ctk.X)
        bottom.configure(height=50)

        root.after(200, lambda: switch("Dashboard"))

        return bottom
    
    elif role == "Driver":
        def switch(page):
            for widget in main_frame.winfo_children():
                widget.destroy()

            if page == "Dashboard":
                dashboard_page(main_frame)
            elif page == "Map":
                Map_page(main_frame,role,details)

        bottom = ctk.CTkFrame(root, fg_color="#222222")

        buttons = ["Dashboard", "Map"]

        for i, name in enumerate(buttons):
            btn = ctk.CTkButton(bottom, text=name,
                                command=lambda n=name: switch(n))
            btn.place(relx=i/2, rely=0, relwidth=1/2)

        bottom.pack(side=ctk.BOTTOM, fill=ctk.X)
        bottom.configure(height=50)

        root.after(200, lambda: switch("Dashboard"))

        return bottom