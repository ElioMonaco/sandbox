CREATE TABLE `message_photos` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message_id` bigint NOT NULL,
  `chat_id` bigint NOT NULL,
  `file_id` varchar(100) DEFAULT NULL,
  `file_unique_id` varchar(50) NOT NULL,
  `file_size` bigint DEFAULT NULL,
  `width` bigint DEFAULT NULL,
  `height` bigint DEFAULT NULL,
  `insert_time` datetime DEFAULT NULL,
  PRIMARY KEY (`chat_id`,`message_id`,`file_unique_id`),
  KEY `id_index` (`ID`),
  KEY `chat_id` (`chat_id`,`message_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2961 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci