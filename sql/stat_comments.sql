SELECT
    fb_comment.member_id,
    count(*)
FROM
    fb_comment
JOIN
    fb_post
    ON fb_comment.post_id = fb_post.id
WHERE
    group_id = %s
    AND fb_comment.date >= %s::timestamp
    AND fb_comment.date < %s::timestamp
GROUP BY
    1
