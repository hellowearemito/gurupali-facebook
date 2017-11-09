import networkx as nx


def generate_grapf(post_comment_members):
    G = nx.Graph()

    for row_index in range(post_comment_members.shape[0]):
        n1 = post_comment_members.member_id_post_owner[row_index]
        n2 = post_comment_members.member_id_commenter[row_index]

        # edge
        if G.has_edge(n1, n2):
            G[n1][n2]['weight'] += 1
        else:
            G.add_edge(n1, n2, weight=1)

        # node
        if 'weight' in G.node[n1]:
            G.node[n1]['weight'] += 1
        else:
            G.node[n1]['weight'] = 1

    return G
