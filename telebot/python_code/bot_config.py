user_db = "************************"
passw_db = "************************"
host_db =  'localhost'
port_db = 3306
schema_db = 'telegram'
jack = "************************"
jaden = "************************"
general_purpose = "************************"
bkp_mysql = "E:\\MySQL"
mysql_data_location = "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Data"
logs_data_location = "E:\\MySQL\\GPbot_logs"
target_user = [
    "jackinyellow"
    ,"gweiffin"
    ,"The_Bias"
        ]
chat = {
    "************************": "************************"
}
messages = {
    "command_messages": {
        "start": [
            "bot enabled"
        ]
        ,"set": [
            "reply_sc1", "reply_sc2"
        ]
        ,"scrape": True
        ,"getfile": [
            
        ]
        ,"downloadfile": [

        ]
    }
    ,"reply_messages": {
        "user1": [
            "reply_user11"
            ,"reply_user12"
        ]
        ,"user2": [
            "reply_user21"
            ,"reply_user22"
        ]
    }
}

message_table_mapping = {
    "raw": "raw_messages"
    ,"user": "users_staging"
    ,"type": "message_types_staging"
    ,"chat": "chats_staging"
    ,"message": "messages"
    ,"entity": "message_entities"
    ,"photo": "message_photos"
    ,"poll_option": "message_poll_options"
    ,"poll": "message_polls"
    ,"voice": "message_audios"
    ,"video": "message_videos"
    ,"sticker": "message_stickers"
    ,"location": "message_locations"
    ,"contact": "message_contacts"
}

file_types = {
    "voice": ".mp3"
    ,"photo": ".jpg"
    ,"video": ".mp4"
}
