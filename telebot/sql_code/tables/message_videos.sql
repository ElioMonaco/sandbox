CREATE TABLE `message_videos` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message_id` bigint NOT NULL,
  `chat_id` bigint NOT NULL,
  `file_id` text NOT NULL,
  `file_unique_id` text,
  `width` bigint DEFAULT NULL,
  `height` bigint DEFAULT NULL,
  `duration` bigint DEFAULT NULL,
  `file_name` text,
  `mime_type` text,
  `file_size` bigint DEFAULT NULL,
  `insert_time` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci