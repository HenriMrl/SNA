import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import pickle

data = pd.read_csv("user_taggedartists.dat", delimiter="\t")

G = nx.Graph()

# Step 1: Group by artistID and aggregate shared tags
grouped_data = data.groupby('artistID')['tagID'].apply(set).reset_index()

# Step 2: Add nodes and attributes to the graph
with open("tag_results.txt", "w") as file:  # Open file for documenting results
    file.write("Nodes and their tags:\n")
    for index, row in grouped_data.iterrows():
        print(f"Adding node {row['artistID']} with tags {row['tagID']}")
        G.add_node(row['artistID'], tags=row['tagID'])
        # Document the node and its tags in the file
        file.write(f"Node {row['artistID']} has tags {row['tagID']}\n")

print("Nodes added successfully.")

# Step 3: Add edges based using Jaccard similarity
print("Step 5: Precomputing union of tag sets for each node...")
tag_sets = {node: set(tags) for node, tags in nx.get_node_attributes(G, 'tags').items()}

# Step 4: Add edges based on Jaccard similarity
print("Step 6: Calculating and adding Jaccard similarities...")
for u in G.nodes():
    tags_u = tag_sets[u]
    print(f"Processing node {u}...")
    for v in G.neighbors(u):
        tags_v = tag_sets[v]
        print(f"Calculating Jaccard similarity between nodes {u} and {v}...")
        jaccard_similarity = len(tags_u.intersection(tags_v)) / len(tags_u.union(tags_v))
        if jaccard_similarity > 0:
            G.add_edge(u, v, weight=jaccard_similarity)

# Save the graph for task 10
with open("artist_network.pickle", "wb") as f:
    pickle.dump(G, f)

# Step 5: drawing graph

pos = nx.circular_layout(G)

node_sizes = [200 * len(G.edges(node)) for node in G.nodes()]

edge_width = [edata['weight'] * 2 for u, v, edata in G.edges(data=True)]

nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='skyblue')

nx.draw_networkx_edges(G, pos, width=edge_width, edge_color='k', alpha=0.5)

nx.draw_networkx_labels(G, pos, font_size=8)

plt.axis('off')
plt.show()
print("Process completed successfully.")


