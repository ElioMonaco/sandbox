CREATE ALGORITHM = UNDEFINED DEFINER = `elio`@` % ` SQL SECURITY DEFINER VIEW `users_dimension` AS

SELECT DISTINCT `users`.`user_id` AS `user_id`
	,`users`.`username` AS `username`
FROM `users`
