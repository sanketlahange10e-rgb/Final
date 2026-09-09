import tkinter as tk
from tkinter import ttk
import tkintermapview
import osmnx as ox
import networkx as nx
import os
import numpy as np
import csv
from sklearn.cluster import KMeans
BUS_CAPACITY = 41
#new part
def heuristic(a, b):

    lat1 = G.nodes[a]["y"]
    lon1 = G.nodes[a]["x"]

    lat2 = G.nodes[b]["y"]
    lon2 = G.nodes[b]["x"]

    return ((lat1-lat2)**2 + (lon1-lon2)**2) ** 0.5
#1
def get_graph():
    place = "Nashik, Maharashtra, India"
    graph_file = "nashik_network.graphml"

    if os.path.exists(graph_file):
        print("Loading saved Nashik road network...")
        G = ox.load_graphml(graph_file)
    else:
        print("Downloading Nashik road network...")
        G = ox.graph_from_place(
         place,
          network_type="drive",
          simplify=True
        )

        G = ox.add_edge_speeds(G)
        G = ox.add_edge_travel_times(G)
        ox.save_graphml(G, graph_file)

    return G

def load_students():
    students = []
    # Use a portable path relative to this script's location
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'stdcood3.csv')
    with open(csv_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            lat = float(row["latitude"])
            lon = float(row["longitude"])
            name = row["name"]
            students.append((name, lat, lon))
    return students

#def cluster_students(student_data):
    coords = np.array([[s[1], s[2]] for s in student_data])
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    labels = kmeans.fit_predict(coords)
    bus_groups = {i: [] for i in range(5)}
    for student, label in zip(student_data, labels):
        bus_groups[label].append(student)
    return bus_groups
def cluster_students(student_data):
    """Groups students while respecting BUS_CAPACITY."""
    from shapely.geometry import Point, MultiPoint
    from geopy.distance import geodesic
    coords = np.array([[s[1], s[2]] for s in student_data])
    num_buses = int(np.ceil(len(student_data) / BUS_CAPACITY))
    # KMeans clustering
    kmeans = KMeans(n_clusters=num_buses, random_state=42, n_init=10)
    kmeans.fit(coords)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_

    # Build convex hulls for each cluster
    cluster_points = {i: [] for i in range(num_buses)}
    for idx, label in enumerate(labels):
        cluster_points[label].append(Point(coords[idx][0], coords[idx][1]))
    cluster_hulls = {}
    for i in range(num_buses):
        if len(cluster_points[i]) >= 3:
            cluster_hulls[i] = MultiPoint(cluster_points[i]).convex_hull
        else:
            cluster_hulls[i] = MultiPoint(cluster_points[i]).envelope

    # Assign students to their cluster, but enforce area and 2km rule
    bus_groups = {}
    unassigned = []
    unassigned_dict = {}
    area_bus_counter = {i: 0 for i in range(num_buses)}
    area_students = {i: [] for i in range(num_buses)}
    # First, group students by area
    for idx, student in enumerate(student_data):
        label = labels[idx]
        pt = Point(student[1], student[2])
        if cluster_hulls[label].contains(pt) or cluster_hulls[label].distance(pt) < 1e-6:
            area_students[label].append(student)
        else:
            unassigned.append(student)

    # Assign buses for each area, re-cluster if needed
    bus_id = 0
    for area, students_in_area in area_students.items():
        if len(students_in_area) > BUS_CAPACITY:
            # Re-cluster this area
            n_extra = int(np.ceil(len(students_in_area) / BUS_CAPACITY))
            area_coords = np.array([[s[1], s[2]] for s in students_in_area])
            area_kmeans = KMeans(n_clusters=n_extra, random_state=42, n_init=10)
            area_labels = area_kmeans.fit_predict(area_coords)
            for extra_cluster in range(n_extra):
                cluster_students_list = [s for idx, s in enumerate(students_in_area) if area_labels[idx] == extra_cluster]
                for i in range(0, len(cluster_students_list), BUS_CAPACITY):
                    bus_groups[bus_id] = cluster_students_list[i:i+BUS_CAPACITY]
                    bus_id += 1
        else:
            bus_groups[bus_id] = students_in_area
            bus_id += 1

    # Try to assign unassigned students to other clusters if within 2km of hull
    for student in unassigned:
        pt = Point(student[1], student[2])
        assigned = False
        for area in range(num_buses):
            hull = cluster_hulls[area]
            # Sample points along hull boundary for distance check
            if hull.geom_type == 'Polygon':
                boundary_coords = list(hull.exterior.coords)
            else:
                boundary_coords = list(hull.coords)
            min_dist_km = min(geodesic((pt.x, pt.y), (c[0], c[1])).km for c in boundary_coords)
            if min_dist_km <= 2.0:
                # Assign to a new bus for this area if all are full
                assigned = False
                # Find buses for this area
                area_bus_ids = [bid for bid, group in bus_groups.items() if group and group[0] in area_students[area]]
                for bid in area_bus_ids:
                    if len(bus_groups[bid]) < BUS_CAPACITY:
                        bus_groups[bid].append(student)
                        assigned = True
                        break
                if not assigned:
                    # Create new bus for this area
                    bus_groups[bus_id] = [student]
                    bus_id += 1
                    assigned = True
                break
        if not assigned:
            print(f"Warning: Student {student[0]} could not be assigned within area/2km rule.")
            unassigned_dict[student[0]] = {'lat': student[1], 'lon': student[2]}

    return bus_groups, unassigned_dict
# Function to show unassigned students with PNG
def show_unassigned_students(unassigned_dict):
    import tkinter as tk
    from PIL import Image, ImageTk

    window = tk.Toplevel()
    window.title("Unassigned Students")
    window.geometry("600x600")

    # Load PNG
    img_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'std_stop.png')
    img_path = os.path.abspath(img_path)
    img = Image.open(img_path)
    img = img.resize((400, 400))
    photo = ImageTk.PhotoImage(img)

    label_img = tk.Label(window, image=photo)
    label_img.image = photo
    label_img.pack(pady=10)

    # Show unassigned students
    label_title = tk.Label(window, text="Unassigned Students:", font=("Arial", 14))
    label_title.pack()
    for name, info in unassigned_dict.items():
        label = tk.Label(window, text=f"{name}: lat={info['lat']}, lon={info['lon']}")
        label.pack()

    window.mainloop()

def calculate_sequential_routes(G, bus_groups, destination_node):
    routes = {}
    bus_colors = ["red", "blue", "green", "purple", "orange"]

    for i, (bus_id, students) in enumerate(bus_groups.items()):

        remaining_nodes = []
        for s in students:
            node = ox.distance.nearest_nodes(G, s[2], s[1])
            remaining_nodes.append(node)

        current_node = remaining_nodes.pop(0)
        full_bus_path = []

        while remaining_nodes:

            next_node = min(
                remaining_nodes,
                key=lambda n: nx.shortest_path_length(
                    G, current_node, n, weight='length'
                )
            )

            segment = nx.astar_path(
                G,
                current_node,
                next_node,
                heuristic=heuristic,
                weight="length"
            )

            full_bus_path.extend(segment[:-1])

            current_node = next_node
            remaining_nodes.remove(next_node)

        # final path to college
        to_college = nx.astar_path(
            G,
            current_node,
            destination_node,
            heuristic=heuristic,
            weight="length"
        )

        full_bus_path.extend(to_college)

        path_coords = []

        for u, v in zip(full_bus_path[:-1], full_bus_path[1:]):

            edge = G.get_edge_data(u, v)
            if edge is None:
                continue

            edge_data = list(edge.values())[0]

            if "geometry" in edge_data:
                xs, ys = edge_data["geometry"].xy
                for lat, lon in zip(ys, xs):
                    path_coords.append((lat, lon))
            else:
                path_coords.append((G.nodes[u]["y"], G.nodes[u]["x"]))
                path_coords.append((G.nodes[v]["y"], G.nodes[v]["x"]))

        routes[f"Bus {i+1}"] = {
            "color": bus_colors[i % len(bus_colors)],
            "path": path_coords,
            "students": students
        }

    return routes

print("Loading road network...")
G = get_graph()

print("Loading students from CSV...")
students = load_students()

dest_lat = 20.0119
dest_lon = 73.7535

destination_node = ox.distance.nearest_nodes(G, dest_lon, dest_lat)

print("Clustering students...")
bus_groups, unassigned_dict = cluster_students(students)


print("Calculating routes...")
routes = calculate_sequential_routes(G, bus_groups, destination_node)

# Show unassigned students with PNG if any
if unassigned_dict:
    show_unassigned_students(unassigned_dict)


root = tk.Tk()
root.title("Transport Inefficiency Analyzer")
root.geometry("1200x700")

control_frame = ttk.Frame(root, width=250, padding=10)
control_frame.pack(side="left", fill="y")

map_frame = ttk.Frame(root)
map_frame.pack(side="right", fill="both", expand=True)

map_widget = tkintermapview.TkinterMapView(map_frame)
map_widget.set_position(dest_lat, dest_lon)
map_widget.set_zoom(13)
map_widget.pack(fill="both", expand=True)

'''road_points = calculate_sequential_routes()
map_widget.set_path(road_points)

bus_marker = map_widget.set_marker(
    road_points[0][0], road_points[0][1], text="Bus 1"
)

def move_bus(index=0):
    """Recursively moves the bus along the route using Tkinter's safe .after() method"""
    if index < len(road_points):
        lat, lon = road_points[index]
        bus_marker.set_position(lat, lon)
        
        # Call this function again after 50 milliseconds with the next index
        root.after(50, move_bus, index + 1)
    else:
        print("Bus has arrived at the destination!")

# Start the animation loop safely on the main thread
move_bus()
'''
def draw_routes(event=None):
    selected_bus = bus_combobox.get()
    map_widget.delete_all_path()
    map_widget.delete_all_marker()  
    map_widget.set_marker(dest_lat, dest_lon, text="Bhonsala Military College")

    if selected_bus == "All Buses":
        for bus_name, bus_info in routes.items():
            map_widget.set_path(
                bus_info["path"], 
                color=bus_info["color"], 
                width=3 )
            for student in bus_info["students"]:
                name, lat, lon = student
                map_widget.set_marker(lat, lon, text=f"{name} ({bus_name})")
        # Show unassigned students as dots
        for name, info in unassigned_dict.items():
            map_widget.set_marker(info['lat'], info['lon'], text=f"{name} (Unassigned)", marker_color_circle="black", marker_color_outside="black")
    else:
        bus_info = routes[selected_bus]
        map_widget.set_path(
            bus_info["path"], 
            color=bus_info["color"], 
            width=5 )
        for student in bus_info["students"]:
            name, lat, lon = student
            map_widget.set_marker(lat, lon, text=name)
        # Show unassigned students as dots
        for name, info in unassigned_dict.items():
            map_widget.set_marker(info['lat'], info['lon'], text=f"{name} (Unassigned)", marker_color_circle="black", marker_color_outside="black")

ttk.Label(control_frame, text="Select Bus Route", font=("Arial", 14)).pack(pady=20)

bus_options = ["All Buses", "Bus 1", "Bus 2", "Bus 3", "Bus 4"]

bus_combobox = ttk.Combobox(
    control_frame,
    values=bus_options,
    state="readonly")

bus_combobox.pack(fill="x")
bus_combobox.set("All Buses")
bus_combobox.bind("<<ComboboxSelected>>", draw_routes)

draw_routes()

root.mainloop()