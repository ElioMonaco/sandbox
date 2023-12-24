CREATE DEFINER=`root`@`localhost` PROCEDURE `update_chats`()
BEGIN

	CREATE TEMPORARY TABLE cte0
    SELECT s.*
    FROM telegram.chats_staging AS s
    LEFT JOIN 
    (
        SELECT *
        FROM telegram.chats 
        WHERE valid_to IS NULL
    ) AS c
    ON s.chat_id = c.chat_id
    WHERE COALESCE(s.type, '') <> COALESCE(c.type, '')
        OR COALESCE(s.title, '') <> COALESCE(c.title, '') 
        OR COALESCE(s.username, '') <> COALESCE(c.username, '')
        OR COALESCE(s.first_name, '') <> COALESCE(c.first_name, '')
        OR COALESCE(s.last_name, '') <> COALESCE(c.last_name, '')
        OR COALESCE(s.is_forum, '') <> COALESCE(c.is_forum, '')
        OR COALESCE(s.photo, '') <> COALESCE(c.photo, '')
        OR COALESCE(s.bio, '') <> COALESCE(c.bio, '')
        OR COALESCE(s.join_to_send_messages, '') <> COALESCE(c.join_to_send_messages, '')
        OR COALESCE(s.join_by_request, '') <> COALESCE(c.join_by_request, '')
        OR COALESCE(s.has_private_forwards, '') <> COALESCE(c.has_private_forwards, '')
        OR COALESCE(s.has_restricted_voice_and_video_messages, '') <> COALESCE(c.has_restricted_voice_and_video_messages, '')
        OR COALESCE(s.description, '') <> COALESCE(c.description, '')
        OR COALESCE(s.invite_link, '') <> COALESCE(c.invite_link, '')
        OR COALESCE(s.pinned_message, '') <> COALESCE(c.pinned_message, '') 
        OR COALESCE(s.permissions, '') <> COALESCE(c.permissions, '') 
        OR COALESCE(s.slow_mode_delay, '') <> COALESCE(c.slow_mode_delay, '')
        OR COALESCE(s.message_auto_delete_time, '') <> COALESCE(c.message_auto_delete_time, '') 
        OR COALESCE(s.has_protected_content, '') <> COALESCE(c.has_protected_content, '')
        OR COALESCE(s.sticker_set_name, '') <> COALESCE(c.sticker_set_name, '')
        OR COALESCE(s.can_set_sticker_set, '') <> COALESCE(c.can_set_sticker_set, '')
        OR COALESCE(s.linked_chat_id, '') <> COALESCE(c.linked_chat_id, '')
        OR COALESCE(s.location, '') <> COALESCE(c.location, '') 
        OR COALESCE(s.active_usernames, '') <> COALESCE(c.active_usernames, '')
        OR COALESCE(s.emoji_status_custom_emoji_id, '') <> COALESCE(c.emoji_status_custom_emoji_id, '')
        OR COALESCE(s.has_hidden_members, '') <> COALESCE(c.has_hidden_members, '')
        OR COALESCE(s.has_aggressive_anti_spam_enabled, '') <> COALESCE(c.has_aggressive_anti_spam_enabled, '')
        OR COALESCE(s.emoji_status_expiration_date, '') <> COALESCE(c.emoji_status_expiration_date, '');
    
    UPDATE telegram.chats AS u
    INNER JOIN cte0 AS c
    ON c.chat_id = u.chat_id
    SET valid_to = UTC_TIMESTAMP()
    WHERE u.valid_to IS NULL;

    INSERT INTO telegram.chats 
    (
        chat_id
        ,type
        ,title
        ,username
        ,first_name
        ,last_name
        ,is_forum
        ,photo
        ,bio
        ,join_to_send_messages
        ,join_by_request
        ,has_private_forwards
        ,has_restricted_voice_and_video_messages
        ,description
        ,invite_link
        ,pinned_message
        ,permissions
        ,slow_mode_delay
        ,message_auto_delete_time
        ,has_protected_content
        ,sticker_set_name
        ,can_set_sticker_set
        ,linked_chat_id
        ,location
        ,active_usernames
        ,emoji_status_custom_emoji_id
        ,has_hidden_members
        ,has_aggressive_anti_spam_enabled
        ,emoji_status_expiration_date
        ,valid_from
        ,valid_to
    ) 
    SELECT chat_id
            ,type
            ,title
            ,username
            ,first_name
            ,last_name
            ,is_forum
            ,photo
            ,bio
            ,join_to_send_messages
            ,join_by_request
            ,has_private_forwards
            ,has_restricted_voice_and_video_messages
            ,description
            ,invite_link
            ,pinned_message
            ,permissions
            ,slow_mode_delay
            ,message_auto_delete_time
            ,has_protected_content
            ,sticker_set_name
            ,can_set_sticker_set
            ,linked_chat_id
            ,location
            ,active_usernames
            ,emoji_status_custom_emoji_id
            ,has_hidden_members
            ,has_aggressive_anti_spam_enabled
            ,emoji_status_expiration_date
            ,UTC_TIMESTAMP() AS valid_from
            ,NULL AS valid_to
    FROM cte0;
        
    TRUNCATE TABLE telegram.chats_staging;

    DROP TABLE cte0;

END