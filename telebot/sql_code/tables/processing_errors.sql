CREATE TABLE `processing_errors` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message_id` bigint NOT NULL,
  `chat_id` bigint NOT NULL,
  `step` varchar(50) DEFAULT NULL,
  `step_number` int NOT NULL,
  `is_error` tinyint(1) NOT NULL,
  `error_message` text,
  `insert_time` datetime NOT NULL,
  KEY `id_index` (`ID`),
  KEY `chat_id` (`chat_id`,`message_id`),
  KEY `is_error` (`is_error`)
) ENGINE=InnoDB AUTO_INCREMENT=2322 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci