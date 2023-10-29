CREATE TABLE `message_entities` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message_id` bigint NOT NULL,
  `chat_id` bigint NOT NULL,
  `offset` bigint DEFAULT NULL,
  `length` bigint DEFAULT NULL,
  `type` text,
  `insert_time` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci