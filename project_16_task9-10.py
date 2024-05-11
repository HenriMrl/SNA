import pandas as pd
import networkx as nx

#task 9 implemented

# Load data
data = pd.read_csv("user_taggedartists.dat", delimiter="\t")

# Create a graph
G = nx.Graph()

grouped_data = data.groupby('artistID')['tagID'].apply(set).reset_index()

for index, row in grouped_data.iterrows():
    G.add_node(row['artistID'], tags=row['tagID'])

#use jaccard similarity
for u in G.nodes():
    tags_u = G.nodes[u]['tags']
    for v in G.nodes():
        if u != v:
            tags_v = G.nodes[v]['tags']
            jaccard_similarity = len(tags_u.intersection(tags_v)) / len(tags_u.union(tags_v))
            if jaccard_similarity > 0.5:  # Adjust the threshold as needed
                G.add_edge(u, v, weight=jaccard_similarity)

# Ensure connectivity with jaccard similarity
if not nx.is_connected(G):
    print("Graph is not connected. Connecting the graph...")
    for u in G.nodes():
        for v in G.nodes():
            if u != v and not G.has_edge(u, v):
                tags_u = G.nodes[u]['tags']
                tags_v = G.nodes[v]['tags']
                jaccard_similarity = len(tags_u.intersection(tags_v)) / len(tags_u.union(tags_v))
                if jaccard_similarity > 0.5:
                    G.add_edge(u, v, weight=jaccard_similarity)
                    if nx.is_connected(G):
                        print("Graph is now connected.")
                        break
        if nx.is_connected(G):
            break

print("Graph is now connected.")

#task 10 implemented

degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
eigenvector_centrality = nx.eigenvector_centrality(G)

# Combine centrality measures into a single score for each node
combined_centrality = {}
for node in G.nodes():
    combined_centrality[node] = degree_centrality[node] + betweenness_centrality[node] + eigenvector_centrality[node]

# Find top-10 popular nodes based on the combined centrality score
top_10_combined = sorted(combined_centrality, key=combined_centrality.get, reverse=True)[:10]

# Print top-10 nodes based on the combined centrality score
print("Top 10 nodes based on Combined Centrality:")
print(top_10_combined)
