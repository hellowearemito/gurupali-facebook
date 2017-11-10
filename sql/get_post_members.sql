WITH members AS (
    SELECT
        distinct(member_id)
    FROM
        fb_post
    WHERE
        group_id=%s
)

SELECT
    *
FROM
    fb_member
WHERE
    id IN (SELECT * FROM members)
