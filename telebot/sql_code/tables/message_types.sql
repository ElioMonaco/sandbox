CREATE TABLE `message_types` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message_type` varchar(100) DEFAULT NULL,
  `last_updated` datetime NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `message_type_UNIQUE` (`message_type`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci