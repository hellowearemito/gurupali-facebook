from urllib.parse import urlencode
import requests

graph_url = 'https://graph.facebook.com'
version = 'v2.11'
post_fields = 'id,from{id,name,picture},created_time'  # noqa
comment_fields = 'id,from{id,name,picture},created_time'


def get_next_page_url(obj):
    return obj.get('paging', {}).get('next')


def get_next_page(url):
    return requests.get(url).json()


def get_group(settings):
    return _call_api(_id=settings.facebook_group_id, endpoint='',
                     access_token=settings.facebook_access_token)


def get_feed(settings):
    return _call_api(_id=settings.facebook_group_id, endpoint='feed',
                     access_token=settings.facebook_access_token)


def get_post(_id, settings):
    return _call_api(_id=_id, endpoint='',
                     fields=post_fields,
                     access_token=settings.facebook_access_token)


def get_comments(_id, settings):
    return _call_api(_id=_id, endpoint='comments',
                     fields=comment_fields,
                     access_token=settings.facebook_access_token)


def _call_api(_id, endpoint, *args, **kwargs):
    res = requests.get(
        _assemble_url(_id, endpoint, *args, **kwargs)).json()

    if 'error' in res:
        raise Exception(
            'Facebook API error: {error}'.format(
                error=res['error']['message']))
    return res


def _assemble_url(_id, endpoint, *args, **kwargs):
    return '{graph_url}/{version}/{_id}/{endpoint}?{query}'.format(
        graph_url=graph_url,
        version=version,
        _id=_id,
        endpoint=endpoint,
        query=urlencode(kwargs))
