import networkx as nx

def detect_communities(G, k=3):
    communities = list(nx.k_clique_communities(G, k))
    list_communities = [list(x) for x in communities]
    return list_communities