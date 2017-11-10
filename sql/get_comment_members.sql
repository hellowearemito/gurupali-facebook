WITH members AS (
    SELECT
        distinct fb_comment.member_id
    FROM
        fb_post
    JOIN
        fb_comment
        ON fb_comment.post_id = fb_post.id
    WHERE
        group_id=%s
)

SELECT
    *
FROM
    fb_member
WHERE
    id IN (SELECT * FROM members)
