CREATE TABLE `messages` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message_id` bigint NOT NULL,
  `message_type` text,
  `from_user` bigint NOT NULL,
  `from_chat` bigint NOT NULL,
  `message_timestamp` bigint DEFAULT NULL,
  `text` text,
  `insert_time` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci