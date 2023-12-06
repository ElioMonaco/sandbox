CREATE TABLE `processing_errors` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message_id` bigint NOT NULL,
  `chat_id` bigint NOT NULL,
  `step` text,
  `step_number` int NOT NULL,
  `is_error` tinyint(1) NOT NULL,
  `error_message` text,
  `insert_time` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1993 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci