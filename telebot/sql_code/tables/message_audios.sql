CREATE TABLE `message_audios` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message_id` bigint NOT NULL,
  `chat_id` bigint NOT NULL,
  `duration` bigint DEFAULT NULL,
  `mime_type` varchar(100) DEFAULT NULL,
  `file_id` varchar(100) DEFAULT NULL,
  `file_unique_id` varchar(50) DEFAULT NULL,
  `file_size` bigint DEFAULT NULL,
  `insert_time` datetime NOT NULL,
  PRIMARY KEY (`chat_id`,`message_id`),
  KEY `id_index` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=262 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci