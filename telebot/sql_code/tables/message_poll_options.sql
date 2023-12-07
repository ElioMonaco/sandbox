CREATE TABLE `message_poll_options` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `poll_id` bigint DEFAULT NULL,
  `text` text,
  `voter_count` bigint DEFAULT NULL,
  `insert_time` datetime NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `poll_id` (`poll_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci