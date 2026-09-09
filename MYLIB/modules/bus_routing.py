from time import time
import tkinter as tk
from tkinter import ttk
import tkintermapview
import osmnx as ox
import networkx as nx
import os
import numpy as np
import csv
import pandas as pd
import ortools
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from sklearn.cluster import KMeans
import math
import concurrent.futures

dest_lat = 20.0119
dest_lon = 73.7535
BUS_CAPACITY = 50


def calculate_routes():
    start_time = time()
    

    # ==============================
    # GRAPH LOADING
    # ==============================
    def get_graph():
        place = "Nashik, Maharashtra, India"
        graph_file = "nashik_network.graphml"

        if os.path.exists(graph_file):
            return ox.load_graphml(graph_file)

        G = ox.graph_from_place(place, network_type="drive")
        G = ox.add_edge_speeds(G)
        G = ox.add_edge_travel_times(G)

        ox.save_graphml(G, graph_file)
        return G


    # ==============================
    # LOAD STUDENTS
    # ==============================
    def load_students():
        students = []
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'stdcood3.csv')

        with open(csv_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append((
                    row["name"],
                    float(row["latitude"]),
                    float(row["longitude"])
                ))
        return students


    # ==============================
    # CLUSTERING (UNCHANGED)
    # ==============================
    def cluster_with_ripple(student_data):
            import math

            center_lat = 20.0110
            center_lon = 73.7903
            num_buses = 5
            sector_angle = 2 * math.pi / num_buses

            zones = {i: [] for i in range(num_buses)}

            # STEP 1: assign zones
            for name, lat, lon in student_data:
                dy = lat - center_lat
                dx = lon - center_lon

                angle = math.atan2(dy, dx)
                if angle < 0:
                    angle += 2 * math.pi

                sector = int(angle / sector_angle)
                sector = min(sector, num_buses - 1)

                zones[sector].append((name, lat, lon))

            groups = {i: list(zones[i]) for i in range(num_buses)}

            # distance helper (to zone direction)
            def dist_to_zone(s, zone_id):
                # approximate zone center direction
                angle = (2 * math.pi / num_buses) * zone_id
                zx = center_lat + math.sin(angle)
                zy = center_lon + math.cos(angle)
                return (s[1] - zx)**2 + (s[2] - zy)**2

            # ==============================
            # 🔥 RIPPLE PUSH FUNCTION
            # ==============================
            def push_chain(bus, direction, visited):

                if bus in visited:
                    return False
                visited.add(bus)

                next_bus = (bus + direction) % num_buses

                # if next bus has space → done
                if len(groups[next_bus]) < BUS_CAPACITY:
                    return True

                # else push someone from next_bus further
                if not push_chain(next_bus, direction, visited):
                    return False

                # move nearest-to-next-zone student forward
                candidate = min(
                    groups[next_bus],
                    key=lambda s: dist_to_zone(s, (next_bus + direction) % num_buses)
                )

                groups[next_bus].remove(candidate)
                groups[(next_bus + direction) % num_buses].append(candidate)

                return True

            # ==============================
            # HANDLE OVERFLOW
            # ==============================
            for bus in range(num_buses):

                while len(groups[bus]) > BUS_CAPACITY:

                    # pick boundary student (farthest from own zone center)
                    def dist_from_zone(s, bus):
                        angle = (2 * math.pi / num_buses) * bus
                        zx = center_lat + math.sin(angle)
                        zy = center_lon + math.cos(angle)
                        return (s[1] - zx)**2 + (s[2] - zy)**2

                    student = max(groups[bus], key=lambda s: dist_from_zone(s, bus))
                    groups[bus].remove(student)
                    placed = False

                    for direction in [+1, -1]:

                        neighbor = (bus + direction) % num_buses

                        # direct place
                        if len(groups[neighbor]) < BUS_CAPACITY:
                            groups[neighbor].append(student)
                            placed = True
                            break

                        # ripple push
                        if push_chain(neighbor, direction, set()):
                            groups[neighbor].append(student)
                            placed = True
                            break

                    if not placed:
                        print(f"⚠️ Could not place {student[0]}")

            groups = {k: v for k, v in groups.items() if v}
            return groups
        

    # ==============================
    # OR-TOOLS ROUTE SOLVER
    # ==============================
    def solve_route(G, coords):

        nodes = [ox.distance.nearest_nodes(G, lon, lat) for lat, lon in coords]

        def dist(a, b):
            try:
                return nx.shortest_path_length(G, a, b, weight="travel_time")
            except:
                return 999999

        matrix = np.array([[dist(a, b) for b in nodes] for a in nodes])

        manager = pywrapcp.RoutingIndexManager(len(nodes), 1, 0)
        model = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            return int(matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)])

        transit = model.RegisterTransitCallback(distance_callback)
        model.SetArcCostEvaluatorOfAllVehicles(transit)

        params = pywrapcp.DefaultRoutingSearchParameters()
        params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

        solution = model.SolveWithParameters(params)

        route = []
        index = model.Start(0)

        while not model.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(model.NextVar(index))

        return [coords[i] for i in route]


    # ==============================
    # PATH GENERATION (REAL ROADS)
    # ==============================
    def build_path(G, route_coords):

        full_path = []

        for i in range(len(route_coords) - 1):
            try:
                start = route_coords[i]
                end = route_coords[i+1]

                start_node = ox.distance.nearest_nodes(G, start[1], start[0])
                end_node = ox.distance.nearest_nodes(G, end[1], end[0])

                path = nx.shortest_path(G, start_node, end_node, weight="travel_time")

                for node in path:
                    full_path.append((G.nodes[node]['y'], G.nodes[node]['x']))

            except:
                continue

        return full_path


    # ==============================
    # MAIN EXECUTION
    # ==============================
    print("Loading graph...")
    G = get_graph()

    print("Loading students...")
    students = load_students()

    print("Clustering...")
    groups = cluster_with_ripple(students)

    routes = {}
    colors = ["red", "blue", "green", "purple", "orange"]

    print("Calculating routes...")

    # ==============================
# PARALLEL BUS PROCESSING
# ==============================
    def process_bus(i, group):
        coords = [(dest_lat, dest_lon)] + [(s[1], s[2]) for s in group]

        optimized = solve_route(G, coords)
        full_path = build_path(G, optimized)

        return i, {
            "color": colors[i % len(colors)],
            "pickup_path": full_path,
            "final_path": [],
            "students": group
        }


    print("Calculating routes (parallel)...")

    routes = {}

    # 🔥 THREAD POOL
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:

        futures = []

        for i, group in groups.items():
            futures.append(executor.submit(process_bus, i, group))

        for future in concurrent.futures.as_completed(futures):
            i, data = future.result()
            routes[f"Bus {i+1}"] = data

    # ==============================
    # SAVE CSV
    # ==============================
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    path     = os.path.join(data_dir, 'bus_routes.csv')
    tmp_path = os.path.join(data_dir, 'bus_routes_tmp.csv')  # write here first

    with open(tmp_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Bus','Color','Student Name','Latitude','Longitude','PickupPath','FinalPath'])

        for b, info in routes.items():
            pickup_str = ';'.join([f"({x},{y})" for x,y in info["pickup_path"]])

            for s in info["students"]:
                writer.writerow([
                    b,
                    info["color"],
                    s[0],
                    s[1],
                    s[2],
                    pickup_str,
                    ""
                ])

    os.replace(tmp_path, path)  # atomic swap — readers never see a partial file
    end_time = time()
    print(f"✅ Routes saved in {end_time - start_time:.2f} seconds")
    print("✅ Routes saved")

    return groups, routes


# ==============================
# UNASSIGNED STUDENTS POPUP
# ==============================
def show_unassigned_students(unassigned_dict):
    from PIL import Image, ImageTk

    window = tk.Toplevel()
    window.title("Unassigned Students")
    window.geometry("600x600")

    img_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'std_stop.png')
    img = Image.open(img_path).resize((400, 400))
    photo = ImageTk.PhotoImage(img)

    label_img = tk.Label(window, image=photo)
    label_img.image = photo
    label_img.pack(pady=10)

    tk.Label(window, text="Unassigned Students:", font=("Arial", 14)).pack()

    for name, info in unassigned_dict.items():
        tk.Label(window, text=f"{name}: lat={info['lat']}, lon={info['lon']}").pack()


# ==============================
# STUDENT MAP PAGE
# ==============================
def show_student_route(main_frame, student_details):
   
    for widget in main_frame.winfo_children():
        widget.destroy()

    # ── unwrap API response wrapper ──────────────────────────
    if "data" in student_details:
        student_details = student_details["data"]

    # ── layout ──────────────────────────────────────────────
    map_frame = ttk.Frame(main_frame)
    map_frame.pack(fill="both", expand=True)

    map_widget = tkintermapview.TkinterMapView(map_frame)
    map_widget.set_position(dest_lat, dest_lon)
    map_widget.set_zoom(13)
    map_widget.pack(fill="both", expand=True)

    # ── resolve student name ─────────────────────────────────
    student_name = (student_details.get("name") or
                    student_details.get("username") or "").strip()

    if not student_name:
        ttk.Label(
            main_frame,
            text="No student name provided. Cannot show route.",
            font=("Arial", 16)
        ).pack(pady=20)
        print(f"[ERROR] student_details missing 'name'/'username': {student_details}")
        return


    # ── load routes (reuse the same load_routes() as show_map) ──
    routes = load_routes()

    if not routes:
        ttk.Label(
            main_frame,
            text="No bus routes file found.",
            font=("Arial", 16)
        ).pack(pady=20)
        print("[ERROR] load_routes() returned nothing.")
        return

    print(f"[DEBUG] All student names in routes: "
          f"{[s[0] for data in routes.values() for s in data['students']]}")

    # ── find which bus this student belongs to ───────────────
    student_bus    = None
    student_info   = None
    student_coords = (None, None)

    for bus, info in routes.items():
        for s in info["students"]:
            if s[0].lower() == student_name.lower():
                student_bus    = bus
                student_info   = info
                student_coords = (s[1], s[2])
                print(f"[DEBUG] Found '{student_name}' on {bus}")
                break
        if student_bus:
            break

    if not student_bus:
        ttk.Label(
            main_frame,
            text="No bus assigned.\nAsk admin to recalculate routes.",
            font=("Arial", 16)
        ).pack(pady=20)
        print(f"[DEBUG] '{student_name}' not found in any bus.")
        return

    # ── join paths exactly like show_map does ────────────────
    def join_paths(pickup, final):
        if pickup and final:
            if pickup[-1] == final[0]:
                return pickup + final[1:]
            else:
                return pickup + final
        elif pickup:
            return pickup
        elif final:
            return final
        else:
            return []

    full_path = join_paths(
        student_info["pickup_path"],
        student_info["final_path"]
    )

    if not full_path:
        ttk.Label(
            main_frame,
            text="Bus found but route path is empty.\nRoutes may need recalculating.",
            font=("Arial", 16)
        ).pack(pady=20)
        print(f"[DEBUG] Empty path for bus {student_bus}")
        return

    # ── draw route (only this student's bus) ─────────────────
    map_widget.set_path(full_path, color=student_info["color"], width=3)

    # ── college marker ───────────────────────────────────────
    map_widget.set_marker(dest_lat, dest_lon, text="College",
                          marker_color_circle="red")

    # ── start marker ─────────────────────────────────────────
    if student_info["pickup_path"]:
        start = student_info["pickup_path"][0]
        map_widget.set_marker(start[0], start[1], text="START",
                              marker_color_circle="green")

    # ── "You" marker — only this student, no others ──────────
    display_lat = float(student_details.get("latitude") or student_coords[0] or dest_lat)
    display_lon = float(student_details.get("longitude") or student_coords[1] or dest_lon)

    map_widget.set_marker(display_lat, display_lon, text="You")
    map_widget.set_position(display_lat, display_lon)

    # ── animated bus icon ────────────────────────────────────
    bus_marker = map_widget.set_marker(
        full_path[0][0],
        full_path[0][1],
        text="🚌"
    )

    def animate(index=0):
        if index >= len(full_path):
            return
        lat, lon = full_path[index]
        bus_marker.set_position(lat, lon)
        map_widget.after(100, lambda: animate(index + 1))

    map_widget.after(500, lambda: animate(0))

    # ── info label ───────────────────────────────────────────
    ttk.Label(
        main_frame,
        text=f"Your bus: {student_bus}",
        font=("Arial", 18)
    ).pack(pady=5)
# ==============================
# LOAD ROUTES FROM CSV
# ==============================
def load_routes():
    routes = {}
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'bus_routes.csv')

    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            bus = row['Bus']

            if bus not in routes:
                routes[bus] = {
                    'color':    row['Color'],
                    'students': [],
                    'path':     []
                }

            routes[bus]['students'].append((
                row['Student Name'],
                float(row['Latitude']),
                float(row['Longitude'])
            ))

            pickup_coords = []
            for coord in row['PickupPath'].split(';'):
                if coord:
                    lat, lon = coord.strip('()').split(',')
                    pickup_coords.append((float(lat), float(lon)))

            final_coords = []
            for coord in row['FinalPath'].split(';'):
                if coord:
                    lat, lon = coord.strip('()').split(',')
                    final_coords.append((float(lat), float(lon)))

            routes[bus]['pickup_path'] = pickup_coords
            routes[bus]['final_path']  = final_coords
            routes[bus]['path']        = pickup_coords + final_coords

    return routes


# ==============================
# LOAD UNASSIGNED STUDENTS
# ==============================
def load_unassigned():
    unassigned = {}
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'unassigned_students.csv')

    if not os.path.exists(path):
        return unassigned

    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            unassigned[row['name']] = {
                'lat': float(row['lat']),
                'lon': float(row['lon'])
            }

    return unassigned


# ==============================
# MAIN MAP VIEW
# ==============================
def show_map(main_frame):
    map_frame = ttk.Frame(main_frame)
    map_frame.pack(fill="both", expand=True)

    map_widget = tkintermapview.TkinterMapView(map_frame)
    map_widget.set_position(dest_lat, dest_lon)
    map_widget.set_zoom(13)
    map_widget.pack(fill="both", expand=True)

    corner_frame = ttk.Frame(map_frame)
    corner_frame.place(relx=1.0, rely=0.0, anchor="ne")

    ttk.Label(corner_frame, text="Select Bus Route", font=("Arial", 14)).pack(pady=10)

    routes    = load_routes()
    unassigned = load_unassigned()

    if unassigned:
        show_unassigned_students(unassigned)

    bus_options  = ["All Buses"] + list(routes.keys())
    bus_combobox = ttk.Combobox(corner_frame, values=bus_options, state="readonly")
    bus_combobox.set("All Buses")
    bus_combobox.pack(fill="x")

    def join_paths(pickup, final):
        if pickup and final:
            if pickup[-1] == final[0]:
                return pickup + final[1:]
            return pickup + final
        return pickup or final or []

    def draw_routes(event=None):
        selected = bus_combobox.get()

        map_widget.delete_all_path()
        map_widget.delete_all_marker()

        map_widget.set_marker(
            dest_lat, dest_lon,
            text="College",
            marker_color_circle="red"
        )

        if selected == "All Buses":
            for bus, info in routes.items():
                full_path = join_paths(info["pickup_path"], info["final_path"])
                if full_path:
                    map_widget.set_path(full_path, color=info["color"], width=3)

                if info["pickup_path"]:
                    sp = info["pickup_path"][0]
                    map_widget.set_marker(sp[0], sp[1], text="START", marker_color_circle="green")

                for s in info["students"]:
                    map_widget.set_marker(s[1], s[2], text=f"{s[0]} ({bus})")
        else:
            info      = routes[selected]
            full_path = join_paths(info["pickup_path"], info["final_path"])
            if full_path:
                map_widget.set_path(full_path, color=info["color"], width=2)

            if info["pickup_path"]:
                sp = info["pickup_path"][0]
                map_widget.set_marker(sp[0], sp[1], text="START", marker_color_circle="green")

            for s in info["students"]:
                map_widget.set_marker(s[1], s[2], text=s[0])

        for name, info in unassigned.items():
            map_widget.set_marker(
                info['lat'], info['lon'],
                text=f"{name} (Unassigned)",
                marker_color_circle="black",
                marker_color_outside="black"
            )

    bus_combobox.bind("<<ComboboxSelected>>", draw_routes)
    draw_routes()
    return map_widget


# ==============================
# BUS ANIMATION
# ==============================
def animate_bus(map_widget, bus_name):
    routes = load_routes()

    if bus_name not in routes:
        print("❌ Bus not found")
        return

    path = routes[bus_name]["path"]

    if not path:
        print("❌ No path found")
        return

    map_widget.delete_all_marker()
    map_widget.set_path(path, color=routes[bus_name]["color"], width=3)

    bus_marker = None
    step = 0

    def move_bus():
        nonlocal bus_marker, step

        if step >= len(path):
            print("✅ Animation finished")
            return

        lat, lon = path[step]

        if bus_marker:
            bus_marker.delete()

        bus_marker = map_widget.set_marker(
            lat, lon,
            text="🚌",
            marker_color_circle="yellow"
        )

        step += 1
        map_widget.after(50, move_bus)

    move_bus()


# Show only a specific student's route and marker
# Usage: show_student_route(main_frame, student_details)
