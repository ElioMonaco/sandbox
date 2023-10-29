CREATE TABLE `users` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `original_chat_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `is_bot` tinyint(1) DEFAULT NULL,
  `first_name` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `username` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `last_name` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `language_code` varchar(100) DEFAULT NULL,
  `can_join_groups` varchar(100) DEFAULT NULL,
  `can_read_all_group_messages` varchar(100) DEFAULT NULL,
  `supports_inline_queries` varchar(100) DEFAULT NULL,
  `is_premium` varchar(100) DEFAULT NULL,
  `added_to_attachment_menu` varchar(100) DEFAULT NULL,
  `valid_from` datetime NOT NULL,
  `valid_to` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci