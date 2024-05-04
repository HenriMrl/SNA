import networkx as nx
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

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

# 3: Generate attributed network of artists based on shared tags
def generate_artist_network(user_tagged_artists_file):
    artist_data = load_data(user_tagged_artists_file)
    artist_graph = nx.Graph()
    
    # Group tags by artists
    artist_tags = artist_data.groupby('artistID')['tagID'].apply(list).to_dict()
    
    # Add nodes with attributes (tags)
    for artist, tags in artist_tags.items():
        artist_graph.add_node(artist, tags=tags)
    
    return artist_graph

# 4: Calculate node similarity measure suitable for attributed network
def calculate_node_similarity(artist_graph):
    # Calculate cosine similarity between attribute vectors
    attribute_vectors = nx.get_node_attributes(artist_graph, 'tags')
    artist_ids = list(attribute_vectors.keys())
    attribute_vectors = [attribute_vectors[artist_id] for artist_id in artist_ids]
    
    # Convert attribute vectors to binary format for Jaccard similarity
    binary_attribute_vectors = []
    for vec in attribute_vectors:
        binary_vec = np.zeros(len(attribute_vectors[0]))
        binary_vec[vec] = 1
        binary_attribute_vectors.append(binary_vec)
    
    # Calculate cosine similarity matrix
    similarity_matrix = cosine_similarity(binary_attribute_vectors)
    
    # Fill similarity matrix to create edges between similar artists
    for i in range(len(artist_ids)):
        for j in range(i+1, len(artist_ids)):
            similarity = similarity_matrix[i][j]
            if similarity > 0:
                artist_graph.add_edge(artist_ids[i], artist_ids[j], similarity=similarity)
    
    return artist_graph

# Main function to run the different parts
def main():
    user_friends_file = 'user_friends.dat'
    user_tagged_artists_file = 'user_taggedartists.dat'

    # 1
    friendship_network = generate_friendship_network(user_friends_file)

    # 2
    calculate_network_properties(friendship_network)

    # 3
    artist_network = generate_artist_network(user_tagged_artists_file)

    # 4
    calculate_node_similarity(artist_network)

if __name__ == "__main__":
    main()
