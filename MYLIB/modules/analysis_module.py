def store_route_analysis(results, algorithm_type, filename="trash_route.csv"):
    """
    Store route analysis results to a CSV file (portable).
    results: dict with keys distance_km, fuel_l, time_min
    algorithm_type: string (e.g. 'greedy', 'sequential')
    filename: CSV file name (default: trash_route.csv)
    """
    import csv
    import os
    # Portable path: store in same directory as this script
    csv_path = os.path.join(os.path.dirname(__file__), filename)
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, mode="a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["algorithm", "distance_km", "fuel_l", "time_min"])
        if not file_exists:
            writer.writeheader()
        row = {
            "algorithm": algorithm_type,
            "distance_km": results["distance_km"],
            "fuel_l": results["fuel_l"],
            "time_min": results["time_min"]
        }
        writer.writerow(row)
import importlib.util
import osmnx as ox
import networkx as nx
import numpy as np
import os

def compare_algorithms(G, students, dest_lat, dest_lon):
    """
    Compare greedy and sequential algorithms for a single bus group.
    Returns dict with distance (km), fuel (L), and time (min) for each.
    """
    # Import greedy_route from Wal_map.py
    spec = importlib.util.spec_from_file_location("Wal_map", os.path.join(os.path.dirname(__file__), "Wal_map.py"))
    Wal_map = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(Wal_map)

    # Greedy route
    greedy_coords = Wal_map.greedy_route(G, students, dest_lat, dest_lon)
    greedy_nodes = [ox.distance.nearest_nodes(G, lon, lat) for lat, lon in greedy_coords]
    greedy_distance = calculate_route_distance(G, greedy_nodes)
    greedy_fuel = calculate_fuel(greedy_distance)
    greedy_time = calculate_time(greedy_distance)

    # Sequential (astar) route
    nodes = [ox.distance.nearest_nodes(G, s[2], s[1]) for s in students]
    current_node = nodes[0]
    remaining_nodes = nodes[1:]
    route_nodes = [current_node]
    while remaining_nodes:
        next_node = min(
            remaining_nodes,
            key=lambda n: nx.shortest_path_length(G, current_node, n, weight='length')
        )
        segment = nx.astar_path(G, current_node, next_node, weight="length")
        route_nodes.extend(segment[1:])
        current_node = next_node
        remaining_nodes.remove(next_node)
    destination_node = ox.distance.nearest_nodes(G, dest_lon, dest_lat)
    segment = nx.astar_path(G, current_node, destination_node, weight="length")
    route_nodes.extend(segment[1:])
    seq_distance = calculate_route_distance(G, route_nodes)
    seq_fuel = calculate_fuel(seq_distance)
    seq_time = calculate_time(seq_distance)

    return {
        "greedy": {"distance_km": greedy_distance, "fuel_l": greedy_fuel, "time_min": greedy_time},
        "sequential": {"distance_km": seq_distance, "fuel_l": seq_fuel, "time_min": seq_time}
    }
from pathlib import Path
import matplotlib.pyplot as plt
import csv
from collections import Counter
def calculate_route_distance(G, route_nodes):

    total_length = 0

    for i in range(len(route_nodes) - 1):
        edge_data = G.get_edge_data(route_nodes[i], route_nodes[i+1])

        if edge_data:
            edge = list(edge_data.values())[0]
            total_length += edge["length"]

    return total_length / 1000   # meters → km
def calculate_fuel(distance_km, mileage=5):

    fuel_used = distance_km / mileage

    return fuel_used
def calculate_time(distance_km, speed=30):

    time_hours = distance_km / speed

    return time_hours * 60   # minutes
def show_diff_alo(main_frame):
    """
    Display a scrollable frame inside main_frame with both the optimization plot and a data table.
    """
    # Example data
    normal_distance = 42
    optimized_distance = 31

    normal_fuel = calculate_fuel(normal_distance)
    optimized_fuel = calculate_fuel(optimized_distance)

    normal_time = calculate_time(normal_distance)
    optimized_time = calculate_time(optimized_distance)

    labels = ["Distance (km)", "Fuel (L)", "Time (min)"]
    normal_values = [normal_distance, normal_fuel, normal_time]
    optimized_values = [optimized_distance, optimized_fuel, optimized_time]


    # If an analysis container already exists, destroy it (toggle behavior)
    if hasattr(main_frame, '_analysis_container') and main_frame._analysis_container is not None:
        main_frame._analysis_container.destroy()
        main_frame._analysis_container = None
        return

    # If a transport analysis container exists, destroy it (only one view at a time)
    if hasattr(main_frame, '_transport_container') and main_frame._transport_container is not None:
        main_frame._transport_container.destroy()
        main_frame._transport_container = None

    # Create a container frame to hold all widgets directly (no scrollable frame)
    container = tk.Frame(main_frame)
    container.pack(fill="both", expand=True)
    main_frame._analysis_container = container

    # Add a close button at the top of the container
    def close_analysis():
        container.destroy()
        if hasattr(main_frame, '_analysis_container'):
            main_frame._analysis_container = None

    close_btn = tk.Button(container, text="Close", command=close_analysis, bg="#d9534f", fg="white")
    close_btn.pack(pady=5, anchor="ne")

    # Add Matplotlib plot
    fig, ax = plt.subplots(figsize=(6, 3))
    x = range(len(labels))
    width = 0.35
    bars1 = ax.barh([i - width/2 for i in x], normal_values, height=width, label="Normal Route", color='tab:blue')
    bars2 = ax.barh([i + width/2 for i in x], optimized_values, height=width, label="Optimized Route", color='tab:green')
    for bars in [bars1, bars2]:
        ax.bar_label(bars, fmt='%.2f', padding=3)
    ax.set_yticks(x)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Value")
    ax.set_title("Transport Optimization Comparison")
    ax.legend()
    plt.tight_layout()

    canvas_plot = FigureCanvasTkAgg(fig, master=container)
    canvas_plot.draw()
    canvas_plot.get_tk_widget().pack(fill="both", expand=True, pady=10)

    # Add data table
    tree = ttk.Treeview(container, columns=("Metric", "Normal", "Optimized"), show="headings", height=4)
    tree.heading("Metric", text="Metric")
    tree.heading("Normal", text="Normal Route")
    tree.heading("Optimized", text="Optimized Route")
    for i, label in enumerate(labels):
        tree.insert("", "end", values=(label, normal_values[i], optimized_values[i]))
    tree.pack(pady=10)

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk

def show_diff_alo_in_frame(main_frame):
    """
    Display the transport comparison bar graph inside a given Tkinter frame.
    """
    normal_distance = 42
    optimized_distance = 31

    normal_fuel = calculate_fuel(normal_distance)
    optimized_fuel = calculate_fuel(optimized_distance)

    normal_time = calculate_time(normal_distance)
    optimized_time = calculate_time(optimized_distance)

    labels = ["Distance (km)", "Fuel (L)", "Time (min)"]
    normal_values = [normal_distance, normal_fuel, normal_time]
    optimized_values = [optimized_distance, optimized_fuel, optimized_time]

    # Create a matplotlib figure
    fig, ax = plt.subplots(figsize=(6, 4))
    
    x = range(len(labels))
    ax.barh(x, normal_values, color='skyblue', label="Normal Route")
    ax.barh(x, optimized_values, left=normal_values, color='orange', label="Optimized Route")
    
    ax.set_yticks(x)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Values")
    ax.set_title("Transport Optimization Comparison")
    ax.legend()

    # Embed in Tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)