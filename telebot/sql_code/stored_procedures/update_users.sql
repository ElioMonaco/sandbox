CREATE DEFINER=`root`@`localhost` PROCEDURE `update_users`()
BEGIN

	CREATE TEMPORARY TABLE cte0
    SELECT s.*
    FROM telegram.users_staging AS s
    LEFT JOIN
    (
        SELECT *
        FROM telegram.users
        WHERE valid_to IS NULL
    ) AS u
    ON s.user_id = u.user_id 
        AND s.original_chat_id = u.original_chat_id
    WHERE COALESCE(s.is_bot, 0) <> COALESCE(u.is_bot, 0)
        OR COALESCE(s.first_name, '') <> COALESCE(u.first_name, '')
        OR COALESCE(s.username, '') <> COALESCE(u.username, '')
        OR COALESCE(s.last_name, '') <> COALESCE(u.last_name, '')
        OR COALESCE(s.language_code, '') <> COALESCE(u.language_code, '')
        OR COALESCE(s.can_join_groups, '') <> COALESCE(u.can_join_groups, '')
        OR COALESCE(s.can_read_all_group_messages, '') <> COALESCE(u.can_read_all_group_messages, '')
        OR COALESCE(s.supports_inline_queries, '') <> COALESCE(u.supports_inline_queries, '')
        OR COALESCE(s.is_premium, 0) <> COALESCE(u.is_premium, 0)
        OR COALESCE(s.added_to_attachment_menu, '') <> COALESCE(u.added_to_attachment_menu, '');

    UPDATE telegram.users AS u
    INNER JOIN cte0 AS c
    ON c.user_id = u.user_id
    SET valid_to = UTC_TIMESTAMP()
    WHERE u.valid_to IS NULL;

    INSERT INTO telegram.users
    (
        original_chat_id
        ,user_id
        ,is_bot
        ,first_name
        ,username
        ,last_name
        ,language_code
        ,can_join_groups
        ,can_read_all_group_messages
        ,supports_inline_queries
        ,is_premium
        ,added_to_attachment_menu
        ,valid_from
        ,valid_to
    )
    SELECT original_chat_id
            ,user_id
            ,is_bot
            ,first_name
            ,username
            ,last_name
            ,language_code
            ,can_join_groups
            ,can_read_all_group_messages
            ,supports_inline_queries
            ,is_premium
            ,added_to_attachment_menu
            ,UTC_TIMESTAMP() AS valid_from
            ,NULL AS valid_to
    FROM cte0;

    TRUNCATE TABLE telegram.users_staging;

    DROP TABLE cte0;

END