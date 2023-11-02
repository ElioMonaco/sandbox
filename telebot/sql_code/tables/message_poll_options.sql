CREATE TABLE `message_poll_options` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `poll_id` text NOT NULL,
  `text` text,
  `voter_count` bigint DEFAULT NULL,
  `insert_time` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci