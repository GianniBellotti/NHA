#----------------------------------------------------------------------------------------------------------------
#Derived weights from report table

#-------
#Vulnerabilitiy inverse weights
no_vulns = 0
minor = -1
medium = -2
major = -3

#--------
#Security Control Weights
firewall_router = 3
router_firewall = 7
router_switch = 0
switch_router = 9
router_client = 6
client_router = 3
router_wireless = 0
wireless_router = 3
switch_firewall = 7
firewall_switch = 0
switch_client = 4
client_switch = 2
wireless_client = 4
client_wireless = 0
firewall_client = 4
client_firewall = 5
client_client = 1
#----------------------------------------------------------------------------------------------------------------


# This class represent a graph
class Graph:
    # Initialize the class
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()
    # Create an undirected graph by adding symmetric edges
    def make_undirected(self):
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.graph_dict.setdefault(b, {})[a] = dist
    # Add a link from A and B of given distance, and also add the inverse link if the graph is undirected
    def connect(self, A, B, distance=1):
        self.graph_dict.setdefault(A, {})[B] = distance
        if not self.directed:
            self.graph_dict.setdefault(B, {})[A] = distance
    # Get neighbors or a neighbor
    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)
    # Return a list of nodes in the graph
    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)
#----------------------------------------------------------------------------------------------------------------

# This class represent a node
class Node:
    # Initialize the class
    def __init__(self, name:str, parent:str):
        self.name = name
        self.parent = parent
        self.g = 0 # Distance to start node
        self.h = 0 # Distance to goal node
        self.f = 0 # Total cost
    # Compare nodes
    def __eq__(self, other):
        return self.name == other.name
    # Sort nodes
    def __lt__(self, other):
         return self.f < other.f
    # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.name, self.f))


#----------------------------------------------------------------------------------------------------------------

# A* search
def astar_search(graph, heuristics, start, end):
    
    # Create lists for open nodes and closed nodes
    open = []
    closed = []
    # Create a start node and an goal node
    start_node = Node(start, None)
    goal_node = Node(end, None)
    # Add the start node
    open.append(start_node)
    
    # Loop until the open list is empty
    while len(open) > 0:
        # Sort the open list to get the node with the lowest cost first
        open.sort()
        # Get the node with the lowest cost
        current_node = open.pop(0)
        # Add the current node to the closed list
        closed.append(current_node)
        
        # Check if we have reached the goal, return the path
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.name + ': ' + str(current_node.g))
                current_node = current_node.parent
            path.append(start_node.name + ': ' + str(start_node.g))
            # Return reversed path
            return path[::-1]
        # Get neighbours
        neighbors = graph.get(current_node.name)
        # Loop neighbors
        for key, value in neighbors.items():
            # Create a neighbor node
            neighbor = Node(key, current_node)
            # Check if the neighbor is in the closed list
            if(neighbor in closed):
                continue
            # Calculate full path cost
            neighbor.g = current_node.g + graph.get(current_node.name, neighbor.name)
            neighbor.h = heuristics.get(neighbor.name)
            neighbor.f = neighbor.g + neighbor.h
            # Check if neighbor is in open list and if it has a lower f value
            if(add_to_open(open, neighbor) == True):
                # Everything is green, add neighbor to open list
                open.append(neighbor)
    # Return None, no path is found
    return None
#----------------------------------------------------------------------------------------------------------------

# Check if a neighbor should be added to open list
def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f > node.f):
            return False
    return True
#----------------------------------------------------------------------------------------------------------------


# The main entry point for this module
def main():
    # Create a graph
    graph = Graph()
    # Create graph connections (Actual distance)
    
    #Subdomain A
    #Client -> Switch
    graph.connect('ClientA', 'SwitchA', client_switch)
    graph.connect('ClientB', 'SwitchA', client_switch)
    graph.connect('ClientC', 'SwitchA', client_switch)
    graph.connect('ClientD', 'SwitchA', client_switch)
    graph.connect('ClientE', 'SwitchA', client_switch)

    #Switch -> client
    graph.connect('SwitchA', 'ClientA', switch_client)
    graph.connect('SwitchA', 'ClientB', switch_client)
    graph.connect('SwitchA', 'ClientC', switch_client)
    graph.connect('SwitchA', 'ClientD', switch_client)
    graph.connect('SwitchA', 'ClientE', switch_client)

    #Branch
    graph.connect('SwitchA', 'SwitchB', switch_client)

    #Subdomain B
    #Client -> Switch
    graph.connect('ClientF', 'SwitchB', client_switch)
    graph.connect('ClientG', 'SwitchB', client_switch)
    graph.connect('ClientH', 'SwitchB', client_switch)
    graph.connect('ClientI', 'SwitchB', client_switch)
    graph.connect('ClientJ', 'SwitchB', client_switch)
    graph.connect('ClientK', 'SwitchB', client_switch)

    #Switch -> client
    graph.connect('SwitchB', 'ClientF', switch_client)
    graph.connect('SwitchB', 'ClientG', switch_client)
    graph.connect('SwitchB', 'ClientH', switch_client)
    graph.connect('SwitchB', 'ClientI', switch_client)
    graph.connect('SwitchB', 'ClientJ', switch_client)
    graph.connect('SwitchB', 'ClientK', switch_client)

    #Port opennings between non branched
    graph.connect('ClientA', 'ClientB', client_client)
    graph.connect('ClientJ', 'ClientB', client_client)
    graph.connect('ClientH', 'ClientB', client_client)
    graph.connect('ClientB', 'ClientK', client_client)

    # Create heuristics (inverse vulnerabilities)
    heuristics = {}
    heuristics['ClientA'] = no_vulns
    heuristics['ClientB'] = no_vulns
    heuristics['ClientC'] = no_vulns
    heuristics['ClientD'] = no_vulns
    heuristics['ClientE'] = no_vulns
    heuristics['ClientF'] = no_vulns
    heuristics['ClientG'] = no_vulns
    heuristics['ClientH'] = minor
    heuristics['ClientI'] = no_vulns
    heuristics['ClientJ'] = no_vulns
    heuristics['ClientK'] = no_vulns
    heuristics['SwitchA'] = minor
    heuristics['SwitchB'] = medium

    # Run the search algorithm
    path = astar_search(graph, heuristics, 'ClientA', 'ClientI')
    print(path)
    print()
# Tell python to run main method
if __name__ == "__main__": main()