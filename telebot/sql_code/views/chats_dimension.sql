CREATE ALGORITHM = UNDEFINED DEFINER = `elio`@` % ` SQL SECURITY DEFINER VIEW `chats_dimension` AS

WITH cte1 AS (
    SELECT DISTINCT `chats`.`chat_id` AS `chat_id`
        ,(
            CASE 
                WHEN (`chats`.`title` IS NOT NULL)
                    THEN `chats`.`title`
                ELSE `chats`.`username`
                END
            ) AS `chat_name`
        ,`chats`.`type` AS `chat_type`
        ,`chats`.`valid_from` AS `valid_from`
    FROM `chats`
)
,cte2 AS (
    SELECT *
            ,ROW_NUMBER() OVER(PARTITION BY `chat_id` ORDER BY `valid_from` DESC) AS row_num  
    FROM cte1
)

SELECT `chat_id`
        ,`chat_name`
        ,`chat_type`
FROM cte2
WHERE row_num = 1