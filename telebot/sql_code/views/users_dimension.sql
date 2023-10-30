CREATE ALGORITHM = UNDEFINED DEFINER = `elio`@` % ` SQL SECURITY DEFINER VIEW `users_dimension` AS

WITH cte AS (
    SELECT DISTINCT `users`.`user_id` AS `user_id`
        ,`users`.`username` AS `username`
        ,ROW_NUMBER() OVER(PARTITION BY `user_id` ORDER BY `valid_from` DESC) AS row_num  
    FROM `users`
)

SELECT `user_id`
        ,`username`
FROM cte
WHERE row_num = 1