CREATE TABLE `message_polls` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message_id` bigint NOT NULL,
  `chat_id` bigint NOT NULL,
  `poll_id` bigint DEFAULT NULL,
  `question` text,
  `total_voter_count` bigint DEFAULT NULL,
  `is_closed` bit(1) DEFAULT NULL,
  `is_anonymous` bit(1) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `allows_multiple_answers` bit(1) DEFAULT NULL,
  `insert_time` datetime NOT NULL,
  PRIMARY KEY (`chat_id`,`message_id`),
  KEY `id_index` (`ID`),
  KEY `poll_id` (`poll_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci