import networkx as nx

from gurupali_facebook.analyzer.generate_graph import generate_grapf
from gurupali_facebook.analyzer.track_groups import track_groups
from gurupali_facebook.analyzer.genetere_viz_fedd_csvs import generate_viz_feed_csvs
from gurupali_facebook.analyzer.detect_communities import louvain_community

def generete_viz_feed_csvs(monthly_raw_data, start_year, start_month):
    monthly_graphs = list(map(generate_grapf, monthly_raw_data))

    detected_communities = list(map(louvain_community, monthly_graphs))

    groups_tracking = track_groups(detected_communities)

    generate_viz_feed_csvs(monthly_graphs, groups_tracking,
                           start_year, start_month)


def generete_closeness_centrality(monthly_raw_data, dateline):
    monthly_graphs = list(map(generate_grapf, monthly_raw_data))

    stat = []
    for i, mg in enumerate(monthly_graphs):
        closenesses = nx.closeness_centrality(mg)

        stat.append([dateline[i], closenesses])

    return stat


def generete_pagerank(monthly_raw_data, dateline):
    monthly_graphs = list(map(generate_grapf, monthly_raw_data))

    stat = []
    for i, mg in enumerate(monthly_graphs):
        closenesses = nx.pagerank(mg)

        stat.append([dateline[i], closenesses])

    return stat
