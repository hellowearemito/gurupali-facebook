from gurupali_facebook.facebook import (
    get_group, get_feed, get_post, get_comments, get_next_page_url, get_page)
from gurupali_facebook.db import (
    upsert_group, upsert_member, upsert_post, upsert_comment, next_page_exists,
    save_next_page_url, get_next_page)


def crawl_group(settings):
    group = get_group(settings)
    upsert_group(settings, _id=group['id'], name=group['name'])

    has_next_page_url = True
    feed = _get_feed(settings)

    while(has_next_page_url):
        print('next page')
        _crawl_posts(feed, settings)

        feed = _get_feed(settings, feed)
        if not feed:
            has_next_page_url = False


def _crawl_posts(feed, settings):
    for d in feed['data']:
        post = get_post(d['id'], settings)

        upsert_member(settings, _id=post['from']['id'],
                      name=post['from']['name'])

        upsert_post(settings, _id=post['id'],
                    group_id=settings.facebook_group_id,
                    member_id=post['from']['id'],
                    date=post['created_time'])

        _crawl_comments(settings, post['id'])


def _crawl_comments(settings, post_id):
    comments = get_comments(post_id, settings)
    has_next_page_url = True

    while(has_next_page_url):
        for comment in comments['data']:
            upsert_member(
                settings, _id=comment['from']['id'],
                name=comment['from']['name'])

            upsert_comment(
                settings, _id=comment['id'], post_id=post_id,
                member_id=comment['from']['id'],
                date=comment['created_time'])
        next_page_url = get_next_page_url(comments)
        if next_page_url:
            comments = get_page(next_page_url)
        else:
            has_next_page_url = False


def _get_feed(settings, current_feed=None):
    if current_feed:
        next_page_url = get_next_page_url(current_feed,
                                          remove_access_token=True)
        if next_page_url:
            save_next_page_url(settings,
                               settings.facebook_group_id, next_page_url)
        else:
            return None

    if not next_page_exists(settings, settings.facebook_group_id):
        feed = get_feed(settings)
        next_page_url = get_next_page_url(feed, remove_access_token=True)
        if next_page_url:
            save_next_page_url(settings,
                               settings.facebook_group_id, next_page_url)
        return feed

    next_page_url = get_next_page(settings, settings.facebook_group_id)
    return get_feed(settings, url=next_page_url)
