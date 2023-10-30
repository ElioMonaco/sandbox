CREATE ALGORITHM = UNDEFINED DEFINER = `elio`@` % ` SQL SECURITY DEFINER VIEW `message_facts` AS

SELECT DISTINCT `m`.`message_type` AS `message_type`
	,`m`.`text` AS `text`
	,`m`.`message_id` AS `message_id`
	,`u`.`user_id` AS `user_id`
	,`u`.`original_chat_id` AS `original_chat_id`
	,concat_ws('|', `u`.`original_chat_id`, `u`.`user_id`, `m`.`message_id`) AS `unique_message_id`
	,`u`.`username` AS `username`
	,from_unixtime(`m`.`message_timestamp`) AS `message_time`
	,`m`.`text` AS `message_text`
	,`a`.`file_id` AS `message_audio`
	,`p`.`file_id` AS `message_photo`
	,`v`.`file_id` AS `message_video`
FROM (
	(
		(
			(
				`messages` `m` LEFT JOIN `users` `u` ON (
						(
							(`u`.`original_chat_id` = `m`.`from_chat`)
							AND (`u`.`user_id` = `m`.`from_user`)
							)
						)
				) LEFT JOIN `message_audios` `a` ON (
					(
						(`a`.`message_id` = `m`.`message_id`)
						AND (`a`.`chat_id` = `m`.`from_chat`)
						)
					)
			) LEFT JOIN `message_photos` `p` ON (
				(
					(`p`.`message_id` = `m`.`message_id`)
					AND (`p`.`chat_id` = `m`.`from_chat`)
					)
				)
		) LEFT JOIN `message_videos` `v` ON (
			(
				(`v`.`message_id` = `m`.`message_id`)
				AND (`v`.`chat_id` = `m`.`from_chat`)
				)
			)
	)
