from collections import deque
import heapq

#insert state space here
state_space = [
    ["Santiago", "Ourense", 104],
    ["Ourense", "Leon", 190],
    ["Ourense", "Salamanca", 338],
    ["Salamanca", "Madrid", 214],
    ["Salamanca", "Caceres", 202],
    ["Caceres", "Madrid", 296],
    ["Caceres", "Seville", 264],
    ["Seville", "Cordoba", 140],
    ["Seville", "Granada", 250],
    ["Cordoba", "Malaga", 168],
    ["Cordoba", "Toledo", 342],
    ["Toledo", "Madrid", 74],
    ["Granada", "Madrid", 419],
    ["Granada", "Murcia", 277],
    ["Murcia", "Madrid", 404],
    ["Murcia", "Valencia", 226],
    ["Valencia", "Madrid", 359],
    ["Valencia", "Barcelona", 348],
    ["Barcelona", "Girona", 101],
    ["Valencia", "Zaragoza", 308],
    ["Zaragoza", "Madrid", 319],
    ["Zaragoza", "Barcelona", 310],
    ["Zaragoza", "Bilbao", 302],
    ["Bilbao", "Donostia", 101],
    ["Donostia", "Zaragoza", 262],
    ["Leon", "Bilbao", 228],
    ["Leon", "Madrid", 288],
    ["Madrid", "Bilbao", 402],
]

#build the association of each node in a dictionary
def build_graph(state_space):
    graph = {}
    for state in state_space:
        (node1, node2, distance) = state
        if node1 not in graph:
            graph[node1] = {}
        if node2 not in graph:
            graph[node2] = {}
        graph[node1][node2] = distance
        graph[node2][node1] = distance
    return graph

#bfs method of calculating distance
def bfs(graph, start_node, goal_node):
    visited = set()
    queue = deque([(start_node, [])])

    while queue:
        #pop and check node to see if it is the goal
        current_node, path = queue.popleft()
        if current_node == goal_node:
            return path + [current_node]
        
        #if node has not been visited, obtain the node's neighbors
        if current_node not in visited:
            visited.add(current_node)
            neighbors = graph[current_node]
            for neighbor in neighbors:
                queue.append((neighbor, path + [current_node]))
    
    return None

#a-star method of calculating distance
def astar(graph, start_node, goal_node, heuristic_values):
    visited = set()
    queue = [(0, start_node, [])]
    heapq.heapify(queue)
    
    while queue:
        #obtain node and path using heappop
        _, current_node, path = heapq.heappop(queue)
        if current_node == goal_node:
            return path + [current_node]
        
        if current_node not in visited:
            visited.add(current_node)
            neighbors = graph[current_node]
            for neighbor in neighbors:
                #calculate the total cost of a path and use it as metric for calculating priority in heapq
                new_path = path + [current_node]
                g_cost = sum(graph[new_path[i]][new_path[i+1]] for i in range(len(new_path)-1))
                h_cost = heuristic_values.get(neighbor)
                if h_cost is not None:
                    priority = g_cost + h_cost
                    heapq.heappush(queue, (priority, neighbor, new_path))

    return None

#shows user what to do
def print_menu():
    print("\nPlease press [1] to set the start node")
    print("Please press [2] to select the goal node")
    print("Please press [3] to start the search using BFS")
    print("Please press [4] to search with heuristic values")
    print("Please press [5] to print all available nodes")
    print("Please press [6] to quit")

#allows user to input their own heuristic values
def input_heuristic_values(graph):
    heuristic_values = {}
    for state in graph.keys():
        while True:
            try:
                heuristic = float(input("Enter the heuristic value for state {}: ".format(state)))
                heuristic_values[state] = heuristic
                break
            except ValueError:
                print("Invalid input! Please enter a numeric value")
    return heuristic_values

start_node = None
goal_node = None

#case switch for user to select what they wish to do
while True:
    graph = build_graph(state_space)
    print_menu()
    choice = input("Please enter your choice: ")
    print()
    if choice == "1":
        start_node = input("Please enter the start node: ")
        if start_node not in graph:
            print("Invalid start node")
            start_node = None
    elif choice == "2":
        goal_node = input("Please enter the goal node: ")
        if goal_node not in graph:
            print("Invalid goal node")
            goal_node = None
    elif choice == "3":
        if not start_node or not goal_node:
            print("Please set start node and goal node first")
            continue
        path = bfs(graph, start_node, goal_node)
        if path:
            total_distance = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
            print("Path from", start_node, "to", goal_node, ":")
            print(" -> ".join(path))
            print("Total distance traveled:", total_distance)
        else:
            print("No path found from", start_node, "to", goal_node)
    elif choice == "4":
        if not start_node or not goal_node:
            print("Please set start node and goal node first")
            continue
        heuristic_values = input_heuristic_values(graph)
        path = astar(graph, start_node, goal_node, heuristic_values)
        if path:
            total_distance = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
            print("Path from", start_node, "to", goal_node, ":")
            print(" -> ".join(path))
            print("Total distance traveled:", total_distance)
        else:
            print("No path found from", start_node, "to", goal_node)
    elif choice == "5":
        print("Available nodes:")
        for node in graph:
            print(node)
    elif choice == "6":
        break
    else:
        print("Invalid choice")


