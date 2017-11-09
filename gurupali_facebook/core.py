from gurupali_facebook.facebook import (
    get_group, get_feed, get_post, get_comments)
from gurupali_facebook.db import (
    create_tables as db_create_tables, upsert_group, upsert_member,
    upsert_post, upsert_comment)


def create_tables(settings):
    db_create_tables(settings)


def crawl_group(settings):
    group = get_group(settings)
    upsert_group(settings, _id=group['id'], name=group['name'])

    feed = get_feed(settings)

    for d in feed['data']:
        post = get_post(d['id'], settings)

        upsert_member(settings, _id=post['from']['id'],
                      name=post['from']['name'],
                      profile_pic=post['from']['picture']['data']['url'])

        upsert_post(settings, _id=post['id'],
                    group_id=settings.facebook_group_id,
                    member_id=post['from']['id'], date=post['created_time'])

        comments = get_comments(post['id'], settings)
        for comment in comments['data']:
            upsert_member(
                settings, _id=comment['from']['id'],
                name=comment['from']['name'],
                profile_pic=comment['from']['picture']['data']['url'])

            upsert_comment(
                settings, _id=comment['id'], post_id=post['id'],
                member_id=comment['from']['id'], date=comment['created_time'])
