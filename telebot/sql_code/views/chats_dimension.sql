CREATE ALGORITHM = UNDEFINED DEFINER = `elio`@` % ` SQL SECURITY DEFINER VIEW `chats_dimension` AS

SELECT DISTINCT `chats`.`chat_id` AS `chat_id`
	,(
		CASE 
			WHEN (`chats`.`title` IS NOT NULL)
				THEN `chats`.`title`
			ELSE `chats`.`username`
			END
		) AS `chat_name`
	,`chats`.`type` AS `chat_type`
FROM `chats`
