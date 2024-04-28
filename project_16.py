import networkx as nx
import pandas as pd

# Load data from files
def load_data(file_path):
    data = pd.read_csv(file_path, delimiter='\t')
    return data

# 1: Generate friendship network among users
def generate_friendship_network(user_friends_file):
    friendship_data = load_data(user_friends_file)
    friendship_graph = nx.Graph()
    for index, row in friendship_data.iterrows():
        user1 = row['userID']
        friend = row['friendID']
        friendship_graph.add_edge(user1, friend)
    return friendship_graph

# 2: Calculate various statistical properties of the network
def calculate_network_properties(network):
    properties = {}
    
    # Calculate the number of edges and nodes
    properties['Number of edges'] = network.number_of_edges()
    properties['Number of nodes'] = network.number_of_nodes()
    
    # Calculate magnitude of largest component
    largest_component = max(nx.connected_components(network), key=len)
    properties['Magnitude of largest component'] = len(largest_component)
    
    # Calculate count and sizes of components
    components = list(nx.connected_components(network))
    properties['Count of components'] = len(components)
    properties['Sizes of components'] = [len(component) for component in components]
    
    # Calculate diameter
    diameters = [nx.diameter(network.subgraph(component)) for component in components]
    properties['Diameter'] = max(diameters)
    
    # Calculate average path length
    avg_path_lengths = [nx.average_shortest_path_length(network.subgraph(component)) for component in components]
    properties['Average path length'] = sum(avg_path_lengths) / len(avg_path_lengths)
    
    # Calculate average clustering coefficient
    clustering_coeffs = [nx.average_clustering(network.subgraph(component)) for component in components]
    properties['Average clustering coefficient'] = sum(clustering_coeffs) / len(clustering_coeffs)
    
    # Print network properties
    print("Network Properties:")
    for prop, value in properties.items():
        print(f"{prop}: {value}")
    
    return properties

# Main function to run the different parts
def main():
    user_friends_file = 'user_friends.dat'

    # 1
    friendship_network = generate_friendship_network(user_friends_file)

    # 2
    calculate_network_properties(friendship_network)

if __name__ == "__main__":
    main()
