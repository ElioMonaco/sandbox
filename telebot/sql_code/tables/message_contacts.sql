CREATE TABLE `message_contacts` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message_id` bigint NOT NULL,
  `chat_id` bigint NOT NULL,
  `contact_phone_number` text,
  `contact_user_id` bigint DEFAULT NULL,
  `contact_first_name` varchar(100) DEFAULT NULL,
  `contact_last_name` varchar(100) DEFAULT NULL,
  `contact_vcard` varchar(300) DEFAULT NULL,
  `insert_time` datetime NOT NULL,
  PRIMARY KEY (`chat_id`,`message_id`),
  KEY `id_index` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci