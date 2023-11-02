CREATE TABLE `message_polls` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message_id` bigint NOT NULL,
  `chat_id` bigint NOT NULL,
  `poll_id` text NOT NULL,
  `question` text,
  `total_voter_count` bigint DEFAULT NULL,
  `is_closed` bit(1) DEFAULT NULL,
  `is_anonymous` bit(1) DEFAULT NULL,
  `type` text,
  `allows_multiple_answers` bit(1) DEFAULT NULL,
  `insert_time` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci