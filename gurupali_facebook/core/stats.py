import json
import pandas as pd

from gurupali_facebook.db import (
    get_window_stat, get_first_post_date,
    get_last_post_date, get_post_members, get_comment_members, get_sum_post,
    get_sum_comment, get_post_stat, get_comment_stat)
from gurupali_facebook.utils import add_month, profile_str, profile_stat
from gurupali_facebook.analyzer.main_viz_feed_hac_2017 import (
    generete_viz_feed_csvs, generete_closeness_centrality,
    generete_pagerank)


def analyze(settings):
    (monthly_raw_data, start_year,
        start_month, dateline) = _get_monthly_raw_data(settings)
    generete_viz_feed_csvs(monthly_raw_data, start_year, start_month)


def generate_profiles(settings):
    profiles = {}
    posts_stat = _get_stats(settings, fn=get_post_stat)
    comments_stat = _get_stats(settings, fn=get_comment_stat)

    (monthly_raw_data, start_year,
        start_month, dateline) = _get_monthly_raw_data(settings)
    closeness_stat = generete_closeness_centrality(monthly_raw_data, dateline)
    pagerank_stat = generete_pagerank(monthly_raw_data, dateline)

    for m in list(
            set(get_post_members(settings) + get_comment_members(settings))):
        profiles[m[0]] = [
            profile_str(m[1]),
            profile_str(get_sum_post(settings, _id=m[0]),
                        name="Total number of posts"),
            profile_str(get_sum_comment(settings, _id=m[0]),
                        name="Total number of comments"),
            profile_stat(posts_stat, m[0], "Number of posts"),
            profile_stat(comments_stat, m[0], "Number of comments"),
            profile_stat(closeness_stat, m[0], "Closenesses"),
            profile_stat(pagerank_stat, m[0], "Pageranks")
        ]

    with open('profiles.json', 'w') as outfile:
        json.dump(profiles, outfile)


def _get_monthly_raw_data(settings):
    interval = 2
    step = 1
    from_date = init_date = get_first_post_date(settings).replace(
        day=1, hour=0, minute=0, second=0)
    to_date = get_last_post_date(settings)

    stats = []
    dateline = []
    while from_date <= to_date:
        dateline.append(from_date)
        df = pd.DataFrame(
            get_window_stat(settings, settings.facebook_group_id,
                            from_date, add_month(from_date, n=interval)) or
            pd.np.empty((0, 2)))
        df.columns = ['member_id_post_owner', 'member_id_commenter']
        stats.append(df)
        from_date = add_month(from_date, n=step)
    return stats, init_date.year, init_date.month, dateline


def _get_stats(settings, fn):
    from_date = get_first_post_date(settings).replace(
        day=1, hour=0, minute=0, second=0)
    to_date = get_last_post_date(settings)

    stats = []
    while from_date <= to_date:
        stat_on_month = fn(settings, settings.facebook_group_id,
                           from_date, add_month(from_date))
        stats.append([from_date, {i[0]: i[1] for i in stat_on_month}])
        from_date = add_month(from_date)
    return stats
