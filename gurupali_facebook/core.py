import pandas as pd

from gurupali_facebook.facebook import (
    get_group, get_feed, get_post, get_comments,
    get_next_page_url, get_next_page)
from gurupali_facebook.db import (
    create_tables as db_create_tables, upsert_group, upsert_member,
    upsert_post, upsert_comment, get_window_stat, get_first_post_date,
    get_last_post_date)
from gurupali_facebook.utils import add_month
from gurupali_facebook.analyzer.main_viz_feed_hac_2017 import generete_viz_feed_csvs


def create_tables(settings):
    db_create_tables(settings)


def crawl_group(settings):
    group = get_group(settings)
    upsert_group(settings, _id=group['id'], name=group['name'])

    feed = get_feed(settings)
    next_page_url = get_next_page_url(feed)

    while(next_page_url):
        for d in feed['data']:
            post = get_post(d['id'], settings)

            upsert_member(settings, _id=post['from']['id'],
                          name=post['from']['name'],
                          profile_pic=post['from']['picture']['data']['url'])

            upsert_post(settings, _id=post['id'],
                        group_id=settings.facebook_group_id,
                        member_id=post['from']['id'],
                        date=post['created_time'])

            _crawl_comments(post['id'], settings)

        next_page_url = get_next_page_url(feed)
        if next_page_url:
            feed = get_next_page(next_page_url)


def analyze(settings):
    monthly_raw_data, start_year, start_month = _get_monthly_raw_data(settings)
    generete_viz_feed_csvs(monthly_raw_data, start_year, start_month)


def _crawl_comments(post_id, settings):
    comments = get_comments(post_id, settings)
    for comment in comments['data']:
        upsert_member(
            settings, _id=comment['from']['id'],
            name=comment['from']['name'],
            profile_pic=comment['from']['picture']['data']['url'])

        upsert_comment(
            settings, _id=comment['id'], post_id=post_id,
            member_id=comment['from']['id'],
            date=comment['created_time'])


def _get_monthly_raw_data(settings):
    interval = 2
    step = 1
    from_date = init_date = get_first_post_date(settings).replace(
        day=1, hour=0, minute=0, second=0)
    to_date = get_last_post_date(settings)

    stats = []
    while from_date <= to_date:
        df = pd.DataFrame(
            get_window_stat(settings, settings.facebook_group_id,
                            from_date, add_month(from_date, n=interval)))
        df.columns = ['member_id_post_owner', 'member_id_commenter']
        stats.append(df)
        from_date = add_month(from_date, n=step)
    return stats, init_date.year, init_date.month
