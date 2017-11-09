import copy
import csv


def generate_viz_feed_csvs(graphs, groups_tracking, start_year, start_month):
    local_graph = copy.deepcopy(graphs)
    only_community_node_graphs = list(map(drop_not_community_member_nodes, local_graph, groups_tracking))
    group_attributed_graphs = list(map(add_group_attr_to_graph, only_community_node_graphs, groups_tracking))

    dump_edges(group_attributed_graphs, start_year, start_month)
    dump_nodes(group_attributed_graphs, start_year, start_month)
    return None


def drop_not_community_member_nodes(G, groups):
    graph_nodes = G.nodes()
    nodes_to_keep = get_nodes_to_keep(groups)
    nodes_to_drop = list(set(graph_nodes) ^ set(nodes_to_keep))
    G.remove_nodes_from(nodes_to_drop)
    return G


def get_nodes_to_keep(groups):
    list_of_lists = list(groups.values())
    flattened = [val for sublist in list_of_lists for val in sublist]
    return flattened


def next_year_and_month(year, month):
    month += 1
    if month == 13:
        month = 1
        year += 1

    return year, month


def add_group_attr_to_graph(G, groups):
    for group_id, community_members in groups.items():
        for community_member in community_members:
            G.node[community_member]["group"] = group_id

    return G


def dump_edges(graphs, year, month):
    with open('edges.csv', 'w', newline='') as csvfile:
        edge_writer = csv.writer(csvfile)

        edge_writer.writerow(["from","to","year","month","weight"])

        for G in graphs:
            for edge in G.edges(data=True):
                edge_writer.writerow([edge[0], edge[1], year, month, edge[2]['weight']])

            year, month = next_year_and_month(year, month)

    return True


def dump_nodes(graphs, year, month):
    with open('nodes.csv', 'w', newline='') as csvfile:
        node_writer = csv.writer(csvfile)

        node_writer.writerow(["id", "year", "month", "group", "weight"])

        for G in graphs:
            for node in G.nodes(data=True):
                if 'weight' not in node[1].keys():
                    node[1]["weight"] = 0

                node_writer.writerow([node[0], year, month, node[1]['group'], node[1]['weight']])

            year, month = next_year_and_month(year, month)

    return True
