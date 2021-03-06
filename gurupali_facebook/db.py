import os
import psycopg2


def _get_connection(db_config):
    return psycopg2.connect(**db_config)


def _get_query(base_dir, query_name):
    path = os.path.join(
        base_dir,
        'sql/{}.sql'.format(query_name))
    with open(path, 'r') as f:
        return f.read()


def create_tables(settings):
    conn = _get_connection(settings.db_settings)
    cur = conn.cursor()

    cur.execute(_get_query(settings.base_dir, 'create_tables'))
    conn.commit()
    cur.close()


def _upsert(settings, exists_query, add_query, *args):
    conn = _get_connection(settings.db_settings)
    cur = conn.cursor()

    cur.execute(_get_query(settings.base_dir, exists_query), (args[0],))
    result = cur.fetchone()
    if not result:
        cur.execute(_get_query(settings.base_dir, add_query), (args))
        conn.commit()
        cur.close()
    return args[0]


def _get_one(settings, query):
    conn = _get_connection(settings.db_settings)
    cur = conn.cursor()

    cur.execute(_get_query(settings.base_dir, query))
    res = cur.fetchone()[0]
    conn.close()
    return res


def _get_one_w_param(settings, query, *args):
    conn = _get_connection(settings.db_settings)
    cur = conn.cursor()

    cur.execute(_get_query(settings.base_dir, query), (args))
    res = cur.fetchone()[0]
    conn.close()
    return res


def upsert_group(settings, _id, name):
    return _upsert(settings, 'group_exists', 'add_group', _id, name)


def upsert_member(settings, _id, name):
    return _upsert(settings, 'member_exists', 'add_member', _id, name)


def upsert_post(settings, _id, group_id, member_id, date):
    return _upsert(settings, 'post_exists', 'add_post',
                   _id, group_id, member_id, date)


def upsert_comment(settings, _id, post_id, member_id, date):
    return _upsert(settings, 'comment_exists', 'add_comment',
                   _id, post_id, member_id, date)


def get_window_stat(settings, group_id, from_date, to_date):
    conn = _get_connection(settings.db_settings)
    cur = conn.cursor()

    cur.execute(_get_query(settings.base_dir, 'stat_on_window'),
                (group_id, from_date, to_date))
    res = cur.fetchall()

    conn.close()
    return res


def get_post_stat(settings, group_id, from_date, to_date):
    return _get_all(settings, 'stat_posts', group_id, from_date, to_date)


def get_comment_stat(settings, group_id, from_date, to_date):
    return _get_all(settings, 'stat_comments', group_id, from_date, to_date)


def _get_all(settings, query, *args):
    conn = _get_connection(settings.db_settings)
    cur = conn.cursor()

    cur.execute(_get_query(settings.base_dir, query),
                (args))
    res = cur.fetchall()

    conn.close()
    return res


def get_first_post_date(settings):
    return _get_one_w_param(settings, 'first_post_date',
                            settings.facebook_group_id)


def get_last_post_date(settings):
    return _get_one_w_param(settings, 'last_post_date',
                            settings.facebook_group_id)


def get_post_members(settings):
    conn = _get_connection(settings.db_settings)
    cur = conn.cursor()

    cur.execute(_get_query(settings.base_dir, 'get_post_members'),
                (settings.facebook_group_id,))
    res = cur.fetchall()

    conn.close()
    return res


def get_comment_members(settings):
    conn = _get_connection(settings.db_settings)
    cur = conn.cursor()

    cur.execute(_get_query(settings.base_dir, 'get_comment_members'),
                (settings.facebook_group_id,))
    res = cur.fetchall()

    conn.close()
    return res


def get_sum_post(settings, _id):
    return _get_one_w_param(settings, 'get_sum_post', _id)


def get_sum_comment(settings, _id):
    return _get_one_w_param(settings, 'get_sum_comment', _id)


def next_page_exists(settings, group_id):
    return bool(_get_one_w_param(settings, 'next_page_exists', group_id))


def save_next_page_url(settings, group_id, url):
    conn = _get_connection(settings.db_settings)
    cur = conn.cursor()

    if next_page_exists(settings, group_id):
        cur.execute(_get_query(settings.base_dir, 'update_pager'),
                    (url, group_id))
    else:
        cur.execute(_get_query(settings.base_dir, 'add_pager'),
                    (group_id, url))
    conn.commit()
    cur.close()
    conn.close()


def get_next_page(settings, group_id):
    return _get_one_w_param(settings, 'get_next_page', group_id)
