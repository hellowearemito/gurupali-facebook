SELECT
    member_id,
    count(*)
FROM
    fb_post
WHERE
    group_id = %s
    AND date >= %s::timestamp
    AND date < %s::timestamp
GROUP BY
    1
