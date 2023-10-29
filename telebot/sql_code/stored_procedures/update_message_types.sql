CREATE DEFINER=`root`@`localhost` PROCEDURE `update_message_types`()
BEGIN
	SET @same_type = (SELECT COUNT(*) 
							FROM telegram.message_types AS m
                            INNER JOIN telegram.message_types_staging AS s
                            ON m.message_type = s.message_type);
	
    IF @same_type = 0 THEN
    
		INSERT INTO telegram.message_types (message_type
											,last_updated)
		SELECT message_type
				,UTC_TIMESTAMP() AS last_updated
		FROM telegram.message_types_staging; 
        
	END IF;
    
    TRUNCATE TABLE telegram.message_types_staging; 
END