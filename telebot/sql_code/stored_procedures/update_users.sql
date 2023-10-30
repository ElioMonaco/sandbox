CREATE DEFINER=`root`@`localhost` PROCEDURE `update_users`()
BEGIN
	SET @changed_user = (SELECT COUNT(*)
							FROM telegram.users AS u
                            INNER JOIN telegram.users_staging AS s
                            ON u.original_chat_id = s.original_chat_id
								AND u.user_id = s.user_id
                            WHERE u.is_bot <> s.is_bot
								OR u.first_name <> s.first_name
                                OR u.username <> s.username
                                OR u.last_name <> s.last_name
                                OR u.can_join_groups <> s.can_join_groups
                                OR u.can_read_all_group_messages <> s.can_read_all_group_messages
                                OR u.supports_inline_queries <> s.supports_inline_queries
                                OR u.is_premium <> s.is_premium
                                OR u.added_to_attachment_menu <> s.added_to_attachment_menu);

    SET @same_user = (SELECT COUNT(*)
							FROM telegram.users AS u
                            INNER JOIN telegram.users_staging AS s
                            ON u.original_chat_id = s.original_chat_id
								AND u.user_id = s.user_id);

    SET @time_bridge = (SELECT UTC_TIMESTAMP());
    IF @changed_user = 1 THEN

		UPDATE telegram.users AS u
        INNER JOIN telegram.users_staging AS s
        ON u.original_chat_id = s.original_chat_id AND u.user_id = s.user_id
        SET u.valid_to = @time_bridge
        WHERE u.valid_to IS NULL;

    END IF;

    IF @changed_user = 1 OR @same_user = 0 THEN

		INSERT INTO telegram.users (original_chat_id
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
									,valid_to)
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
				,@time_bridge AS valid_from
				,NULL AS valid_to
		FROM telegram.users_staging;

	END IF;

    TRUNCATE TABLE `telegram`.`users_staging`;

END