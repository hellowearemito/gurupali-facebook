import networkx as nx
import community

def detect_communities(G, k=3):
    communities = list(nx.k_clique_communities(G, k))
    list_communities = [list(x) for x in communities]
    return list_communities


def louvain_community(G):

    partition = community.best_partition(G)
    result_dict = dict()

    for k, v in partition.items():
        if v in result_dict.keys():
            result_dict[v].append(k)
        else:
            result_dict[v] = [k]

    return list(result_dict.values())

