import psycopg2
import pandas as pd
import networkx as nx

from gurupali_facebook.analyzer.generate_graph import generate_grapf
from gurupali_facebook.analyzer.detect_communities import detect_communities
from gurupali_facebook.analyzer.track_groups import track_groups
from gurupali_facebook.analyzer.genetere_viz_fedd_csvs import generate_viz_feed_csvs

# # create graph
# post_comment_members = pd.read_csv("dummy_query_result.csv", names=['member_id_post_owner', 'member_id_commenter'])
# post_comment_members2 = pd.read_csv("dummy_query_result_month2.csv", names=['member_id_post_owner', 'member_id_commenter'])
# post_comment_members3 = pd.read_csv("dummy_query_result_month3.csv", names=['member_id_post_owner', 'member_id_commenter'])
#
# monthly_raw_data = [post_comment_members, post_comment_members2, post_comment_members3]
#
# #### idaig tarto reszt kell ujrairni
#
# monthly_graphs = list(map(generate_grapf, monthly_raw_data))
#
# detected_communities = list(map(detect_communities, monthly_graphs))
#
# groups_tracking = track_groups(detected_communities)
#
# generate_viz_feed_csvs(monthly_graphs, groups_tracking, 2017, 1)


def generete_viz_feed_csvs(monthly_raw_data, start_year, start_month):
    monthly_graphs = list(map(generate_grapf, monthly_raw_data))

    detected_communities = list(map(detect_communities, monthly_graphs))

    groups_tracking = track_groups(detected_communities)

    generate_viz_feed_csvs(monthly_graphs, groups_tracking, start_year, start_month)

    return True