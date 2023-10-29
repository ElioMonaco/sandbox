CREATE TABLE `chats` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `chat_id` bigint NOT NULL,
  `type` text,
  `title` text,
  `username` text,
  `first_name` text,
  `last_name` text,
  `is_forum` text,
  `photo` text,
  `bio` text,
  `join_to_send_messages` text,
  `join_by_request` text,
  `has_private_forwards` text,
  `has_restricted_voice_and_video_messages` text,
  `description` text,
  `invite_link` text,
  `pinned_message` text,
  `permissions` text,
  `slow_mode_delay` text,
  `message_auto_delete_time` text,
  `has_protected_content` text,
  `sticker_set_name` text,
  `can_set_sticker_set` text,
  `linked_chat_id` text,
  `location` text,
  `active_usernames` text,
  `emoji_status_custom_emoji_id` text,
  `has_hidden_members` text,
  `has_aggressive_anti_spam_enabled` text,
  `emoji_status_expiration_date` text,
  `valid_from` datetime NOT NULL,
  `valid_to` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci