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


def upsert_group(settings, _id, name):
    return _upsert(settings, 'group_exists', 'add_group', _id, name)


def upsert_member(settings, _id, name, profile_pic):
    return _upsert(settings, 'member_exists', 'add_member',
                   _id, name, profile_pic)


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


def get_first_post_date(settings):
    return _get_one(settings, 'first_post_date')


def get_last_post_date(settings):
    return _get_one(settings, 'last_post_date')
