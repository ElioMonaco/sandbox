CREATE TABLE `message_locations` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message_id` bigint NOT NULL,
  `chat_id` bigint NOT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `horizontal_accuracy` double DEFAULT NULL,
  `live_period` bigint DEFAULT NULL,
  `heading` varchar(100) DEFAULT NULL,
  `proximity_alert_radius` varchar(100) DEFAULT NULL,
  `insert_time` datetime NOT NULL,
  PRIMARY KEY (`chat_id`,`message_id`),
  KEY `id_index` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci