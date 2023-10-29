CREATE TABLE `message_photos` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message_id` bigint NOT NULL,
  `caption` text,
  `chat_id` bigint NOT NULL,
  `file_id` text,
  `file_unique_id` text,
  `file_size` bigint DEFAULT NULL,
  `width` bigint DEFAULT NULL,
  `height` bigint DEFAULT NULL,
  `insert_time` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci