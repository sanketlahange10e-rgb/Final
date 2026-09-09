BUS_CAPACITY = 41

def greedy_route_with_capacity(G, students, destination_lat, destination_lon, bus_capacity=BUS_CAPACITY):
	"""
	Splits students into groups of bus_capacity and applies greedy_route to each group.
	Returns dict of bus routes.
	"""
	routes = {}
	num_buses = int(np.ceil(len(students) / bus_capacity))
	for i in range(num_buses):
		group = students[i*bus_capacity:(i+1)*bus_capacity]
		if not group:
			continue
		path = greedy_route(G, group, destination_lat, destination_lon)
		routes[f"Bus {i+1}"] = {
			"path": path,
			"students": group
		}
	return routes
import osmnx as ox
import networkx as nx
import numpy as np

def greedy_route(G, students, destination_lat, destination_lon):
	"""
	Given a graph G, a list of students (name, lat, lon), and a destination,
	returns the route picking the first student, then always the next closest student,
	then goes to the destination.
	"""
	# Convert student coordinates to graph nodes
	nodes = [ox.distance.nearest_nodes(G, lon, lat) for _, lat, lon in students]
	destination_node = ox.distance.nearest_nodes(G, destination_lon, destination_lat)

	# Start at the first student
	current_node = nodes[0]
	remaining_nodes = nodes[1:]
	route = [current_node]

	while remaining_nodes:
		# Find the closest node to current_node
		distances = [nx.shortest_path_length(G, current_node, n, weight='length') for n in remaining_nodes]
		min_idx = np.argmin(distances)
		next_node = remaining_nodes[min_idx]
		# Add path segment
		segment = nx.shortest_path(G, current_node, next_node, weight='length')
		route.extend(segment[1:])
		current_node = next_node
		remaining_nodes.pop(min_idx)

	# Final segment to destination
	segment = nx.shortest_path(G, current_node, destination_node, weight='length')
	route.extend(segment[1:])

	# Convert route to coordinates
	path_coords = []
	for u in route:
		path_coords.append((G.nodes[u]["y"], G.nodes[u]["x"]))
	return path_coords
