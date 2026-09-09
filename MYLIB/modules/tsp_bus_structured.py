import tkinter as tk
from tkinter import ttk
import tkintermapview
import osmnx as ox
import networkx as nx
import numpy as np
import csv
import os
from sklearn.cluster import KMeans
from networkx.algorithms.approximation import greedy_tsp
from tkinter import PhotoImage
# GLOBAL VARIABLES
map_widget = None
routes = {}
G = None


# ------------------------------------------------
# 1️⃣ LOAD MAP FUNCTION
# ------------------------------------------------
def show_map(main_frame):

    global map_widget
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(script_dir, '..', 'data'))
    file_name = os.path.join(data_dir, "stdcood3.csv")
    data_dir = os.path.abspath(os.path.join(script_dir, '..', 'data'))
    icon_img_path = os.path.join(data_dir, "std_stop.png")
    map_widget = tkintermapview.TkinterMapView(main_frame, corner_radius=0)
    map_widget.pack(fill="both", expand=True)
    map_widget.set_position(20.0119, 73.7535)
    map_widget.set_zoom(13)
    icon_img = PhotoImage(file=icon_img_path).subsample(10,10)
    with open(file_name, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            lat = float(row["latitude"])
            lon = float(row["longitude"])
            name = row["name"]
            m = map_widget.set_marker(lat, lon, icon=icon_img, text=name)

    # Show routes if available
    global routes
    if routes:
        colors = ["red", "blue", "green", "purple", "orange"]
        for idx, (bus_name, coords_path) in enumerate(routes.items()):
            color = colors[idx % len(colors)]
            map_widget.set_path(coords_path, color=color, width=4)

    


# ------------------------------------------------
# 2️⃣ FAST ROUTE CALCULATION
# ------------------------------------------------
def calculate_routes():

    global routes, G

    print("Loading graph...")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(script_dir, '..', 'data'))
    graph_file = os.path.join(data_dir, "nashik_network.graphml")

    if G is None:
        G = ox.load_graphml(graph_file)

    print("Loading students...")

    students = []

    students_file = os.path.join(data_dir, "stdcood3.csv")
    with open(students_file) as file:

        reader = csv.DictReader(file)

        for row in reader:

            students.append(
                (
                    row["name"],
                    float(row["latitude"]),
                    float(row["longitude"])
                )
            )


    # -----------------------------
    # CLUSTER STUDENTS
    # -----------------------------
    coords = np.array([[s[1], s[2]] for s in students])

    kmeans = KMeans(n_clusters=5, n_init=5)

    labels = kmeans.fit_predict(coords)

    bus_groups = {i: [] for i in range(5)}

    for student, label in zip(students, labels):
        bus_groups[label].append(student)


    # -----------------------------
    # COLLEGE NODE
    # -----------------------------
    college_lat = 20.0119
    college_lon = 73.7535

    college_node = ox.distance.nearest_nodes(G, college_lon, college_lat)

    routes = {}

    print("Calculating optimized routes...")


    # ------------------------------------------------
    # ROUTE CALCULATION
    # ------------------------------------------------
    for i, (bus_id, group_students) in enumerate(bus_groups.items()):

        nodes = []

        for s in group_students:

            node = ox.distance.nearest_nodes(G, s[2], s[1])
            nodes.append(node)

        nodes.append(college_node)

        n = len(nodes)

        # -----------------------------
        # DISTANCE MATRIX
        # -----------------------------
        dist_matrix = np.zeros((n, n))

        for a in range(n):

            lengths = nx.shortest_path_length(
                G,
                nodes[a],
                weight="length"
            )

            for b in range(n):

                if nodes[b] in lengths:
                    dist_matrix[a][b] = lengths[nodes[b]]
                else:
                    dist_matrix[a][b] = 1e9

        print("")
        # -----------------------------
        # CREATE GRAPH FROM MATRIX
        # -----------------------------
        small_graph = nx.from_numpy_array(dist_matrix)

        tsp_order = nx.approximation.traveling_salesman_problem(
            small_graph,
            weight="weight",
            method=greedy_tsp
        )
        # Rotate tsp_order so college (last index) is first
        college_idx = len(nodes) - 1
        if college_idx in tsp_order:
            idx = tsp_order.index(college_idx)
            tsp_order = tsp_order[idx:] + tsp_order[:idx]
        # convert index → node
        tsp_nodes = [nodes[i] for i in tsp_order]

# Build full road path
        full_path = []

        for j in range(len(tsp_nodes) - 1):

            segment = nx.shortest_path(
                G,
                tsp_nodes[j],
                tsp_nodes[j+1],
                weight="length"
            )

            full_path.extend(segment[:-1])

        full_path.append(tsp_nodes[-1])

        coords_path = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in full_path]

        routes[f"Bus {i+1}"] = coords_path


    # -----------------------------
    # SAVE CSV
    # -----------------------------
    bus_routes_file = os.path.join(data_dir, "bus_routes_tsp.csv")
    with open(bus_routes_file, "w", newline="") as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow(["bus_name", "lat", "lon"])

        for bus_name, coords in routes.items():

            for lat, lon in coords:

                writer.writerow([bus_name, lat, lon])


    print("Routes calculated successfully")

    return routes


# ------------------------------------------------
# 3️⃣ BUS ANIMATION
# ------------------------------------------------
def animate_bus(bus_name):

    global map_widget

    map_widget.delete_all_path()
    map_widget.delete_all_marker()
    
    path = []

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(script_dir, '..', 'data'))
    bus_routes_file = os.path.join(data_dir, "bus_routes_tsp.csv")
    with open(bus_routes_file) as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:

            if row["bus_name"] == bus_name:

                path.append(
                    (float(row["lat"]), float(row["lon"]))
                )

    if not path:
        print("No route found")
        return

    # Ensure animation starts at college
    college_lat = 20.0119
    college_lon = 73.7535
    # Find index of college in path
    start_idx = None
    for idx, (lat, lon) in enumerate(path):
        if abs(lat - college_lat) < 1e-5 and abs(lon - college_lon) < 1e-5:
            start_idx = idx
            break
    if start_idx is not None:
        path = path[start_idx:] + path[:start_idx]

    colors = ["red", "blue", "green", "purple", "orange"]
    index = int(bus_name.split()[-1]) - 1
    map_widget.set_path(path, color=colors[index], width=5)
    marker = map_widget.set_marker(path[0][0], path[0][1], text=bus_name)

    def move(i=0):
        if i < len(path):
            marker.set_position(path[i][0], path[i][1])
            map_widget.after(50, move, i + 1)
    move()