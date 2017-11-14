from gurupali_facebook.facebook import (
    get_group, get_feed, get_post, get_comments, get_next_page_url, get_page)
from gurupali_facebook.db import (
    upsert_group, upsert_member, upsert_post, upsert_comment)


def crawl_group(settings):
    group = get_group(settings)
    upsert_group(settings, _id=group['id'], name=group['name'])

    feed = get_feed(settings)
    has_next_page_url = True

    while(has_next_page_url):
        print('next page')
        _crawl_posts(feed, settings)

        next_page_url = get_next_page_url(feed)
        if next_page_url:
            feed = get_page(next_page_url)
        else:
            has_next_page_url = False


def _crawl_posts(feed, settings):
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


def _crawl_comments(post_id, settings):
    comments = get_comments(post_id, settings)
    has_next_page_url = True

    while(has_next_page_url):
        for comment in comments['data']:
            upsert_member(
                settings, _id=comment['from']['id'],
                name=comment['from']['name'],
                profile_pic=comment['from']['picture']['data']['url'])

            upsert_comment(
                settings, _id=comment['id'], post_id=post_id,
                member_id=comment['from']['id'],
                date=comment['created_time'])
        next_page_url = get_next_page_url(comments)
        if next_page_url:
            comments = get_page(next_page_url)
        else:
            has_next_page_url = False
