CREATE DEFINER=`root`@`localhost` PROCEDURE `update_chats`()
BEGIN
	SET @changed_chat = (SELECT COUNT(*)
							FROM telegram.chats AS c
                            INNER JOIN telegram.chats_staging AS s
                            ON c.chat_id = s.chat_id
                            WHERE c.type <> s.type
									OR c.title <> s.title
									OR c.username <> s.username
									OR c.first_name <> s.first_name
									OR c.last_name <> s.last_name
									OR c.is_forum <> s.is_forum
									OR c.photo <> s.photo
									OR c.bio <> s.bio
									OR c.join_to_send_messages <> s.join_to_send_messages
									OR c.join_by_request <> s.join_by_request
									OR c.has_private_forwards <> s.has_private_forwards
									OR c.has_restricted_voice_and_video_messages <> s.has_restricted_voice_and_video_messages
									OR c.description <> s.description
									OR c.invite_link <> s.invite_link
									OR c.pinned_message <> s.pinned_message
									OR c.permissions <> s.permissions
									OR c.slow_mode_delay <> s.slow_mode_delay
									OR c.message_auto_delete_time <> s.message_auto_delete_time
									OR c.has_protected_content <> s.has_protected_content
									OR c.sticker_set_name <> s.sticker_set_name
									OR c.can_set_sticker_set <> s.can_set_sticker_set
									OR c.linked_chat_id <> s.linked_chat_id
									OR c.location <> s.location
									OR c.active_usernames <> s.active_usernames
									OR c.emoji_status_custom_emoji_id <> s.emoji_status_custom_emoji_id
									OR c.has_hidden_members <> s.has_hidden_members
									OR c.has_aggressive_anti_spam_enabled <> s.has_aggressive_anti_spam_enabled
									OR c.emoji_status_expiration_date <> s.emoji_status_expiration_date);

    SET @same_chat = (SELECT COUNT(*)
							FROM telegram.chats AS c
                            INNER JOIN telegram.chats_staging AS s
                            ON c.chat_id = s.chat_id);

    SET @time_bridge = (SELECT UTC_TIMESTAMP());
    IF @changed_chat = 1 THEN

		UPDATE telegram.chats AS c
        INNER JOIN telegram.chats_staging AS s
        ON c.chat_id = s.chat_id
        SET c.valid_to = @time_bridge
        WHERE c.valid_to IS NULL;

    END IF;

    IF @changed_chat = 1 OR @same_chat = 0 THEN

		INSERT INTO telegram.chats (chat_id
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
									,valid_to)
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
				,@time_bridge AS valid_from
				,NULL AS valid_to
		FROM telegram.chats_staging;

	END IF;

    TRUNCATE TABLE `telegram`.`chats_staging`;
END