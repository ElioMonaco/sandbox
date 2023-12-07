CREATE TABLE `message_entities` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message_id` bigint NOT NULL,
  `chat_id` bigint NOT NULL,
  `offset` bigint DEFAULT NULL,
  `length` bigint DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `insert_time` datetime NOT NULL,
  `custom_emoji_id` bigint unsigned DEFAULT NULL,
  PRIMARY KEY (`chat_id`,`message_id`),
  KEY `id_index` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=143 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci