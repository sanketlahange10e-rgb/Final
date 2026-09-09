from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_bus_load(parent_frame):
    module_dir = Path(__file__).resolve().parent
    data_dir = module_dir.parent / "data"
    file_path = data_dir / "stdcood3.csv"
    df = pd.read_csv(file_path)
    area_counts = df["area"].value_counts()

    # Create a container frame for scrollable content
    container = tk.Frame(parent_frame)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Add a close button
    def close_view():
        container.destroy()
        if hasattr(parent_frame, '_transport_container'):
            parent_frame._transport_container = None

    close_btn = tk.Button(scrollable_frame, text="Close", command=close_view, bg="#d9534f", fg="white")
    close_btn.pack(pady=5, anchor="ne")

    # Create the matplotlib plot
    fig, ax = plt.subplots(figsize=(6, 4))
    area_counts.plot(kind="bar", ax=ax)
    ax.set_title("Bus Load Analysis (Students per Area)")
    ax.set_xlabel("Area")
    ax.set_ylabel("Number of Students")
    plt.tight_layout()

    canvas_plot = FigureCanvasTkAgg(fig, master=scrollable_frame)
    canvas_plot.draw()
    canvas_plot.get_tk_widget().pack(pady=10)
