CREATE TABLE `message_contacts` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message_id` bigint NOT NULL,
  `chat_id` bigint NOT NULL,
  `contact_phone_number` text,
  `contact_user_id` bigint DEFAULT NULL,
  `contact_first_name` text,
  `contact_last_name` text,
  `contact_vcard` text,
  `insert_time` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci