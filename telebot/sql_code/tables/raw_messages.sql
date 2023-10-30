CREATE TABLE `raw_messages` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `message` longtext,
  `insert_time` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=542 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci