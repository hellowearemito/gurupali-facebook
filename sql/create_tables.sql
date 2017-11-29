CREATE TABLE IF NOT EXISTS fb_group (
    id varchar(255) primary key,
    name varchar(255)
);

CREATE TABLE IF NOT EXISTS fb_member (
    id varchar(255) primary key,
    name varchar(255)
);

CREATE TABLE IF NOT EXISTS fb_post (
    id varchar(255) primary key,
    group_id varchar(255) REFERENCES fb_group (id),
    member_id varchar(255) REFERENCES fb_member (id),
    date timestamp without time zone
);

CREATE TABLE IF NOT EXISTS fb_comment (
    id varchar(255) primary key,
    post_id varchar(255) REFERENCES fb_post (id),
    member_id varchar(255) REFERENCES fb_member (id),
    date timestamp without time zone
);

CREATE TABLE IF NOT EXISTS fb_post_recations (
    id serial primary key,
    post_id varchar(255) REFERENCES fb_post (id),
    member_id varchar(255) REFERENCES fb_member (id),
    type varchar(255)
);

CREATE TABLE IF NOT EXISTS fb_comment_recations (
    id serial primary key,
    comment_id varchar(255) REFERENCES fb_post (id),
    member_id varchar(255) REFERENCES fb_member (id),
    type varchar(255)
);

CREATE TABLE IF NOT EXISTS fb_pager (
    id serial primary key,
    group_id varchar(255) REFERENCES fb_group (id),
    link text
);