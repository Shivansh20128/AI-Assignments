import networkx as nx
import csv
import heapq

map_roads = nx.Graph()

with open('Road_Distance.csv', 'r') as file:
    data = csv.reader(file)
    first_line = next(data)
    cities = first_line[1:]

    for city_distances in data:
        city_1 = city_distances[0]
        for i, distance in enumerate(city_distances[1:]):
            city_2 = cities[i]
            if distance == '-':
                continue
            else:
                map_roads.add_edge(city_1, city_2, distance=float(distance))

def unform_cost_search_algo(road_map, source, destination):
    shortest_distance_paths = {city: float(10000) for city in road_map.nodes}
    shortest_distance_paths[source] = 0

    priority_queue = [(0, source)]  

    while priority_queue:
        distance, current_city = heapq.heappop(priority_queue)

        if distance > shortest_distance_paths[current_city]:
            continue

        for neighbor in road_map[current_city]:
            better_path = shortest_distance_paths[current_city] + road_map[current_city][neighbor]['distance']
            if better_path < shortest_distance_paths[neighbor]:
                shortest_distance_paths[neighbor] = better_path
                heapq.heappush(priority_queue, (better_path, neighbor))

    path = []
    current_city = destination
    while current_city != source:
        path.insert(0, current_city)
        eligible_neighbors = (connected_city for connected_city in road_map[current_city] if shortest_distance_paths[connected_city] == shortest_distance_paths[current_city] - road_map[current_city][connected_city]['distance'])
        current_city = min(eligible_neighbors, key=lambda neighbor_city: shortest_distance_paths[neighbor_city])
    path.insert(0, source)
    return path


start_city = 'Delhi'
destination_city = 'Imphal'
shortest_distance_path = unform_cost_search_algo(map_roads, start_city, destination_city)

if shortest_distance_path:
    shortest_distance = sum(map_roads[shortest_distance_path[i]][shortest_distance_path[i+1]]['distance'] for i in range(len(shortest_distance_path) - 1))
    print(f"Shortest path from {start_city} to {destination_city}: {shortest_distance_path}.")
    print(f"Shortest distance between {start_city} to {destination_city}: {shortest_distance}.")
else:
    print(f"There does not exist any path from {start_city} to {destination_city}.")

print()
start_city ='Hubli'
destination_city = 'Agartala'
shortest_distance_path = unform_cost_search_algo(map_roads, start_city, destination_city)

if shortest_distance_path:
    shortest_distance = sum(map_roads[shortest_distance_path[i]][shortest_distance_path[i+1]]['distance'] for i in range(len(shortest_distance_path) - 1))
    print(f"Shortest path from {start_city} to {destination_city}: {shortest_distance_path}.")
    print(f"Shortest distance between {start_city} to {destination_city}: {shortest_distance}.")
else:
    print(f"There does not exist any path from {start_city} to {destination_city}.")
