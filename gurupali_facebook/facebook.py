from urllib.parse import urlencode, urlparse, parse_qsl, urlunparse
from time import sleep
import requests

graph_url = 'https://graph.facebook.com'
version = 'v2.10'
fields = 'id,from{id,name,picture},created_time'


def get_next_page_url(obj, remove_access_token=False):
    params = {'fields': fields}
    url = obj.get('paging', {}).get('next')
    if url:
        url_parts = list(urlparse(url))
        query = dict(parse_qsl(url_parts[4]))
        query.update(params)
        if remove_access_token:
            query.pop('access_token', None)
        url_parts[4] = urlencode(query)
        return urlunparse(url_parts)
    return url


def get_page(url):
    return requests.get(url).json()


def get_group(settings):
    return _call_api(_id=settings.facebook_group_id, endpoint='',
                     access_token=settings.facebook_access_token)


def get_feed(settings, url=None):
    return _call_api(_id=settings.facebook_group_id, endpoint='feed', url=url,
                     access_token=settings.facebook_access_token)


def get_post(_id, settings):
    return _call_api(_id=_id, endpoint='',
                     fields=fields,
                     access_token=settings.facebook_access_token)


def get_comments(_id, settings):
    return _call_api(_id=_id, endpoint='comments',
                     fields=fields,
                     access_token=settings.facebook_access_token)


def _call_api(_id, endpoint, *args, **kwargs):
    if 'url' in kwargs and kwargs['url'] is not None:
        url = '{url}&{params}'.format(url=kwargs.pop('url'),
                                      params=urlencode(kwargs))
    else:
        url = _assemble_url(_id, endpoint, *args, **kwargs)
    resp = requests.get(url)

    if resp.status_code == 503:
        print('Error at Facebook API. Retrying...')
        sleep(5)
        resp = requests.get(url)

    res = resp.json()

    if 'error' in res:
        if res['error']['code'] == 17:
            print("User request limit reached.")
        elif res['error']['code'] == 190:
            print("""Access token has expired"""
                  """Please refresh your token and start again.""")
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
