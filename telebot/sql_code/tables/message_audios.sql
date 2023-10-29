CREATE TABLE `message_audios` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message_id` bigint DEFAULT NULL,
  `chat_id` bigint DEFAULT NULL,
  `duration` bigint DEFAULT NULL,
  `mime_type` text,
  `file_id` text,
  `file_unique_id` text,
  `file_size` bigint DEFAULT NULL,
  `insert_time` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci