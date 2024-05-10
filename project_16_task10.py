import networkx as nx
import pickle
# task 10 implemented

# load the graph from task 9
with open("artist_network.pickle", "rb") as f:
    G = pickle.load(f)

# read the data
data = [] 
with open('user_taggedartists.dat', 'r') as file:
    next(file)
    for line in file:
        parts = line.strip().split('\t')
        if len(parts) >= 2: # only expects 2 values. 
            user_id, artist_id = map(int, parts[:2])
            data.append((user_id, artist_id))
            G.add_edge(user_id, artist_id)  # Add edge to the graph

# calculate the centrality measures
centrality_measures = nx.algorithms.centrality.degree_centrality(G)
centrality_measures.update(nx.algorithms.centrality.betweenness_centrality(G))
centrality_measures.update(nx.algorithms.centrality.eigenvector_centrality(G))

# sort the nodes based on the centrality measures
sorted_centrality = sorted(centrality_measures.items(), key=lambda x: x[1], reverse=True)

# Print top-10 based on the centrality measures
print("Top 10 nodes based on Combined Centrality Measures:")
for node, centrality in sorted_centrality[:10]:
    print(node, centrality)

