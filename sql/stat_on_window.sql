SELECT
    p.member_id as post_author,
    c.member_id as comment_author
FROM
    fb_post AS p
JOIN
    fb_comment AS c
    ON p.id = c.post_id
WHERE
    group_id = %s
    AND p.date >= %s::timestamp
    AND p.date < %s::timestamp
