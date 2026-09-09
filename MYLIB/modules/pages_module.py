import customtkinter as ctk
import os
from MYLIB.modules.bus_routing import show_map, animate_bus
from MYLIB.modules.bus_load import show_bus_load
from MYLIB.modules.analysis_module import show_diff_alo
from MYLIB.modules.bus_routing import load_routes, load_unassigned
from MYLIB.modules.bus_routing import show_student_route
map_widget = None

# ---------------- DASHBOARD ----------------
def dashboard_page(main_frame):
    main_frame.configure(fg_color="#1e1e1e")

    routes = load_routes()
    unassigned = load_unassigned()

    total_students = sum(len(v["students"]) for v in routes.values())
    total_buses = len(routes)
    total_unassigned = len(unassigned)

    title = ctk.CTkLabel(main_frame, text="Dashboard", font=("Arial", 28))
    title.pack(pady=10)

    def card(text):
        return ctk.CTkLabel(main_frame, text=text, font=("Arial", 20))

    card(f"Total Students: {total_students}").pack(pady=10)
    card(f"Total Buses: {total_buses}").pack(pady=10)
    card(f"Unassigned: {total_unassigned}").pack(pady=10)

# ---------------- MAP ----------------
def Map_page(main_frame,role,details):
    global map_widget
    if role == "Admin":
        main_frame.configure(fg_color="#1e1e1e")
        map_widget = show_map(main_frame)
    elif role == "Student":
        main_frame.configure(fg_color="#1e1e1e")
        map_widget = show_student_route(main_frame, details)
    elif role == "Driver":
        main_frame.configure(fg_color="#1e1e1e")
        map_widget = show_map(main_frame)

# ---------------- BUSES ----------------
def Bus_page(main_frame,role):
    main_frame.configure(fg_color="#1e1e1e")
    if role == "Admin":
        routes = load_routes()

        def open_bus(bus_id):
            for widget in main_frame.winfo_children():
                widget.destroy()
            bus_details_page(main_frame, bus_id)

        for bus_name, data in routes.items():
            count = len(data["students"])

            btn = ctk.CTkButton(
                main_frame,
                text=f"{bus_name} ({count} students)",
                font=("Arial", 20),
                command=lambda b=bus_name: open_bus(b)
            )
            btn.pack(pady=10, fill="x", padx=20)

    elif role == "Driver":
        routes = load_routes()

        def open_bus(bus_id):
            for widget in main_frame.winfo_children():
                widget.destroy()
            bus_details_page(main_frame, bus_id)

        for bus_name, data in routes.items():
            count = len(data["students"])

            btn = ctk.CTkButton(
                main_frame,
                text=f"{bus_name} ({count} students)",
                font=("Arial", 20),
                command=lambda b=bus_name: open_bus(b)
            )
            btn.pack(pady=10, fill="x", padx=20)
# ---------------- BUS DETAILS ----------------
def bus_details_page(main_frame, bus_name):
    routes = load_routes()
    data = routes[bus_name]

    title = ctk.CTkLabel(main_frame, text=bus_name, font=("Arial", 28))
    title.pack(pady=10)
    bus_details_page_scroll = ctk.CTkScrollableFrame(main_frame, fg_color="#2e2e2e")
    bus_details_page_scroll.configure(fg_color="#2e2e2e")
    bus_detail_frame = ctk.CTkFrame(bus_details_page_scroll, fg_color="#2e2e2e")
    bus_detail_frame.pack(fill="both", expand=True, padx=20, pady=20)
  
    # Students list
    for s in data["students"]:
        name, lat, lon = s
        ctk.CTkLabel(bus_details_page_scroll, text=f"{name} ({lat}, {lon})").pack()

    # Route button
    btn = ctk.CTkButton(
        bus_detail_frame,
        text="Show Route",
        command=lambda: animate_bus(map_widget, bus_name)
    )
    btn.pack(pady=20)
    bus_details_page_scroll.pack(fill="both", expand=True, padx=20, pady=20)

# ---------------- STUDENTS ----------------
def student_page(main_frame):
    main_frame.configure(fg_color="#1e1e1e")

    routes = load_routes()

    title = ctk.CTkLabel(main_frame, text="Students", font=("Arial", 28))
    title.pack(pady=10)
    student_page_scroll = ctk.CTkScrollableFrame(main_frame, fg_color="#2e2e2e")
    student_page_scroll.configure(fg_color="#2e2e2e")
    student_page_frame = ctk.CTkFrame(student_page_scroll, fg_color="#2e2e2e")
    student_page_frame.pack(fill="both", expand=True, padx=20, pady=20)
    for bus, data in routes.items():
        for s in data["students"]:
            name, lat, lon = s
            ctk.CTkLabel(
                student_page_frame,
                text=f"{name}  {bus}"
            ).pack()
    student_page_scroll.pack(fill="both", expand=True, padx=20, pady=20)

# ---------------- ANALYSIS ----------------
def analysis_page(main_frame):
    main_frame.configure(fg_color="#1e1e1e")
    analysis_options = [
        ("Distance Analysis", "distance"),
        ("Distance Analysis (In Frame)", "distance_in_frame"),
        # Add more options here as needed
    ]

    # Button panel (always visible)
    button_frame = ctk.CTkFrame(main_frame, fg_color="#222")
    button_frame.pack(pady=20, fill="x")

    # Content frame for analysis output
    content_frame = ctk.CTkFrame(main_frame, fg_color="#1e1e1e")
    content_frame.pack(fill="both", expand=True)

    def show_analysis(option):
        print(f"[DEBUG] show_analysis called with option: {option}")
        for widget in content_frame.winfo_children():
            widget.destroy()
        if option == "distance":
            from MYLIB.modules.analysis_module import show_diff_alo
            print("[DEBUG] Calling show_diff_alo(content_frame)")
            show_diff_alo(content_frame)
        elif option == "distance_in_frame":
            from MYLIB.modules.analysis_module import show_diff_alo_in_frame
            print("[DEBUG] Calling show_diff_alo_in_frame(content_frame)")
            show_diff_alo_in_frame(content_frame)
        # Add more elifs for other analysis types

    for i, (label, key) in enumerate(analysis_options):
        btn = ctk.CTkButton(
            button_frame,
            text=label,
            command=lambda k=key: show_analysis(k),
            height=40,
            width=180,
            corner_radius=10,
            fg_color="#5216c2" if i == 0 else "#333",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        btn.pack(side="left", padx=10, pady=10)

    # Show default analysis in content_frame
    show_analysis("distance")
    # Always destroy old analysis container if it exists
    if hasattr(main_frame, '_analysis_container') and main_frame._analysis_container is not None:
        main_frame._analysis_container.destroy()
    main_frame._analysis_container = None

# ---------------- REPORTS ----------------
def export_page(main_frame):
    main_frame.configure(fg_color="#1e1e1e")

    path = os.path.join("MYLIB", "data", "bus_routes.csv")

    ctk.CTkLabel(main_frame, text="Download Bus Routes", font=("Arial", 28)).pack(pady=10)


    def download_csv():
        import tkinter.filedialog as fd
        try:
            dest = fd.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile="bus_routes.csv",
                title="Save CSV as..."
            )
            if dest:
                with open(path, "rb") as src_file:
                    with open(dest, "wb") as dst_file:
                        dst_file.write(src_file.read())
        except Exception as e:
            import tkinter.messagebox as mb
            mb.showerror("Download Error", f"Failed to download file:\n{e}")


    ctk.CTkButton(
        main_frame,
        text="Download CSV",
        command=download_csv,
        font=("Arial", 18),
        fg_color="#5216c2"
    ).pack(pady=10)


    # --- Generate analysis graphs in memory (not shown to user) ---
    import matplotlib.pyplot as plt
    from io import BytesIO
    analysis_graphs = {}

    # Distance Analysis graph
    try:
        from MYLIB.modules.analysis_module import calculate_fuel, calculate_time
        labels = ["Distance (km)", "Fuel (L)", "Time (min)"]
        normal_distance = 42
        optimized_distance = 31
        normal_fuel = calculate_fuel(normal_distance)
        optimized_fuel = calculate_fuel(optimized_distance)
        normal_time = calculate_time(normal_distance)
        optimized_time = calculate_time(optimized_distance)
        normal_values = [normal_distance, normal_fuel, normal_time]
        optimized_values = [optimized_distance, optimized_fuel, optimized_time]
        fig1, ax1 = plt.subplots(figsize=(6, 3))
        x = range(len(labels))
        width = 0.35
        bars1 = ax1.barh([i - width/2 for i in x], normal_values, height=width, label="Normal Route", color='tab:blue')
        bars2 = ax1.barh([i + width/2 for i in x], optimized_values, height=width, label="Optimized Route", color='tab:green')
        for bars in [bars1, bars2]:
            ax1.bar_label(bars, fmt='%.2f', padding=3)
        ax1.set_yticks(list(x))
        ax1.set_yticklabels(labels)
        ax1.set_xlabel("Value")
        ax1.set_title("Transport Optimization Comparison")
        ax1.legend()
        plt.tight_layout()
        analysis_graphs['distance'] = fig1
    except Exception:
        analysis_graphs['distance'] = None

    # Distance Analysis In Frame graph
    try:
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.barh(x, normal_values, color='skyblue', label="Normal Route")
        ax2.barh(x, optimized_values, left=normal_values, color='orange', label="Optimized Route")
        ax2.set_yticks(list(x))
        ax2.set_yticklabels(labels)
        ax2.set_xlabel("Values")
        ax2.set_title("Transport Optimization Comparison")
        ax2.legend()
        plt.tight_layout()
        analysis_graphs['distance_in_frame'] = fig2
    except Exception:
        analysis_graphs['distance_in_frame'] = None

    def download_analysis_graph_distance():
        import tkinter.filedialog as fd
        try:
            fig = analysis_graphs.get('distance')
            if fig is None:
                import tkinter.messagebox as mb
                mb.showerror("Download Error", "Distance Analysis graph could not be generated.")
                return
            dest = fd.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Image", "*.png"), ("All files", "*.*")],
                initialfile="distance_analysis_graph.png",
                title="Save Distance Analysis Graph as..."
            )
            if dest:
                fig.savefig(dest)
        except Exception as e:
            import tkinter.messagebox as mb
            mb.showerror("Download Error", f"Failed to download Distance Analysis graph:\n{e}")

    def download_analysis_graph_distance_in_frame():
        import tkinter.filedialog as fd
        try:
            fig = analysis_graphs.get('distance_in_frame')
            if fig is None:
                import tkinter.messagebox as mb
                mb.showerror("Download Error", "Distance Analysis In Frame graph could not be generated.")
                return
            dest = fd.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Image", "*.png"), ("All files", "*.*")],
                initialfile="distance_analysis_in_frame_graph.png",
                title="Save Distance Analysis In Frame Graph as..."
            )
            if dest:
                fig.savefig(dest)
        except Exception as e:
            import tkinter.messagebox as mb
            mb.showerror("Download Error", f"Failed to download Distance Analysis In Frame graph:\n{e}")

    ctk.CTkButton(
        main_frame,
        text="Download Distance Analysis Graph",
        command=download_analysis_graph_distance,
        font=("Arial", 18),
        fg_color="#1680c2"
    ).pack(pady=10)

    ctk.CTkButton(
        main_frame,
        text="Download Distance Analysis In Frame Graph",
        command=download_analysis_graph_distance_in_frame,
        font=("Arial", 18),
        fg_color="#c28016"
    ).pack(pady=10)


# ---------------- UNASSIGNED ----------------
def unassigned_page(main_frame):
    main_frame.configure(fg_color="#1e1e1e")

    unassigned = load_unassigned()

    title = ctk.CTkLabel(main_frame, text="Unassigned Students", font=("Arial", 28))
    title.pack(pady=10)

    if not unassigned:
        ctk.CTkLabel(main_frame, text="No unassigned students").pack()
        return

    for name, info in unassigned.items():
        ctk.CTkLabel(
            main_frame,
            text=f"{name} ({info['lat']}, {info['lon']})"
        ).pack()
    
    

import customtkinter as ctk

def help_page(frame, show_frame=None):
    """
    CustomTkinter Help Page
    frame: main container passed from your app
    show_frame: optional navigation function
    """

    # Clear existing content
    for widget in frame.winfo_children():
        widget.destroy()

    # Main container
    container = ctk.CTkFrame(frame)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    # Title
    title = ctk.CTkLabel(container, text="Help & Support",
                         font=ctk.CTkFont(size=20, weight="bold"))
    title.pack(pady=10)

    # ---------- HOW TO USE ----------
    ctk.CTkLabel(container, text="How to Use",
                 font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10)

    ctk.CTkLabel(container, text="1. Select your role (Student / Driver / Admin)").pack(anchor="w", padx=20)
    ctk.CTkLabel(container, text="2. Login or Signup").pack(anchor="w", padx=20)
    ctk.CTkLabel(container, text="3. Open map to view bus routes").pack(anchor="w", padx=20)
    ctk.CTkLabel(container, text="4. Track bus in real-time").pack(anchor="w", padx=20)

    # ---------- FAQ ----------
    ctk.CTkLabel(container, text="FAQ",
                 font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=(10, 0))

    ctk.CTkLabel(container, text="Q: Bus not updating?").pack(anchor="w", padx=20)
    ctk.CTkLabel(container, text="A: Check internet or refresh settings").pack(anchor="w", padx=40)

    ctk.CTkLabel(container, text="Q: How do I reset my password?").pack(anchor="w", padx=20)
    ctk.CTkLabel(container, text="A: Use the 'Forgot Password' option on the login page and follow the instructions sent to your email.").pack(anchor="w", padx=40)

    ctk.CTkLabel(container, text="Q: Why can't I see my assigned bus?").pack(anchor="w", padx=20)
    ctk.CTkLabel(container, text="A: Make sure you are logged in with the correct role and your assignment is updated by the admin.").pack(anchor="w", padx=40)

    ctk.CTkLabel(container, text="Q: The map is not loading.").pack(anchor="w", padx=20)
    ctk.CTkLabel(container, text="A: Please check your internet connection and try refreshing the page.").pack(anchor="w", padx=40)
    
    # ---------- CONTACT ----------
    ctk.CTkLabel(container, text="Contact",
                 font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=(10, 0))

    ctk.CTkLabel(container, text="Email: support@busapp.com").pack(anchor="w", padx=20)
    ctk.CTkLabel(container, text="Phone: +91-XXXXXXXXXX").pack(anchor="w", padx=20)

    # ---------- BACK BUTTON ----------
    if show_frame:
        ctk.CTkButton(container, text="⬅ Back",
                      command=lambda: show_frame("MainMenu")
        ).pack(pady=20)
import customtkinter as ctk

def about_page(frame, show_frame=None):
    for widget in frame.winfo_children():
        widget.destroy()

    container = ctk.CTkFrame(frame)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(container, text="About App",
                 font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

    ctk.CTkLabel(container, text="Bus Tracking System").pack(pady=5)
    ctk.CTkLabel(container, text="Version: 1.0").pack(pady=5)
    ctk.CTkLabel(container, text="Developed by: Your Name").pack(pady=5)

    if show_frame:
        ctk.CTkButton(container, text="⬅ Back",
                      command=lambda: show_frame("MainMenu")).pack(pady=20)
        
def driver_info_page(frame):
    import pandas as pd
    import customtkinter as ctk
    # Clear UI
    for widget in frame.winfo_children():
        widget.destroy()

    container = ctk.CTkScrollableFrame(frame)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(container, text="Driver Information",
                 font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

    try:
        import os
        df = pd.read_csv(os.path.join("MYLIB", "data", "Driver.csv"))

        for _, row in df.iterrows():
            card = ctk.CTkFrame(container)
            card.pack(fill="x", padx=10, pady=5)

            ctk.CTkLabel(card, text=f"Bus: {row['bus_assigned']}").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Driver: {row['name']}").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Phone: {row['phone']}").pack(anchor="w", padx=10)

    except Exception as e:
        ctk.CTkLabel(container, text="Error loading driver data").pack(pady=20)
        print("CSV Error:", e)
        


def bus_info_page(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    container = ctk.CTkFrame(frame)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(container, text="Bus Information",
                 font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

    # Sample Data (you can replace later)
    buses = [
        ("Bus 101", "On Time"),
        ("Bus 102", "Delayed"),
        ("Bus 103", "Arriving Soon"),
        ("Bus 104", "Cancelled")
    ]

    for bus, status in buses:
        row = ctk.CTkFrame(container)
        row.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(row, text=bus).pack(side="left", padx=10)
        ctk.CTkLabel(row, text=status).pack(side="right", padx=10)
import customtkinter as ctk

def timetable_page(frame):
    # Clear screen
    for widget in frame.winfo_children():
        widget.destroy()

    container = ctk.CTkScrollableFrame(frame)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(container, text="Bus Time Table",
                 font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

    # Sample timetable data (replace later with real data)
    timetable = [
        ("Bus 101", "City Center", "08:00 AM"),
        ("Bus 102", "College Road", "08:30 AM"),
        ("Bus 103", "Panchavati", "09:00 AM"),
        ("Bus 104", "CBS", "09:30 AM"),
        ("Bus 105", "Gangapur", "10:00 AM"),
    ]

    # Header
    header = ctk.CTkFrame(container)
    header.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(header, text="Bus", width=100).pack(side="left", padx=5)
    ctk.CTkLabel(header, text="Destination", width=150).pack(side="left", padx=5)
    ctk.CTkLabel(header, text="Time", width=100).pack(side="right", padx=5)

    # Data rows
    for bus, dest, time in timetable:
        row = ctk.CTkFrame(container)
        row.pack(fill="x", padx=10, pady=3)

        ctk.CTkLabel(row, text=bus, width=100).pack(side="left", padx=5)
        ctk.CTkLabel(row, text=dest, width=150).pack(side="left", padx=5)
        ctk.CTkLabel(row, text=time, width=100).pack(side="right", padx=5)
def announcements_page(frame, show_frame=None):
    for widget in frame.winfo_children():
        widget.destroy()

    container = ctk.CTkScrollableFrame(frame)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(container, text="Announcements",
                 font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

    announcements = [
        "Bus 101 delayed today",
        "New route added from City Center",
        "Holiday on Monday",
        "Maintenance scheduled tomorrow"
    ]

    for msg in announcements:
        ctk.CTkLabel(container, text="• " + msg).pack(anchor="w", padx=10, pady=2)

    if show_frame:
        ctk.CTkButton(container, text="⬅ Back",
                      command=lambda: show_frame("MainMenu")).pack(pady=20)