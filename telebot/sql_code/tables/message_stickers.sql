CREATE TABLE `message_stickers` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message_id` bigint NOT NULL,
  `chat_id` bigint NOT NULL,
  `file_id` varchar(100) DEFAULT NULL,
  `file_unique_id` varchar(100) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `width` bigint DEFAULT NULL,
  `height` bigint DEFAULT NULL,
  `is_animated` tinyint(1) DEFAULT NULL,
  `is_video` tinyint(1) DEFAULT NULL,
  `emoji` varchar(5) DEFAULT NULL,
  `set_name` varchar(100) DEFAULT NULL,
  `mask_position` varchar(100) DEFAULT NULL,
  `file_size` bigint DEFAULT NULL,
  `premium_animation` varchar(100) DEFAULT NULL,
  `custom_emoji_id` varchar(100) DEFAULT NULL,
  `needs_repainting` varchar(100) DEFAULT NULL,
  `insert_time` datetime NOT NULL,
  PRIMARY KEY (`chat_id`,`message_id`),
  KEY `id_index` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci