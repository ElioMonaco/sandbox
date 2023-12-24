user_db_mysql = 'root'
passw_db_mysql = "************************"
host_db_mysql =  'localhost'
port_db_mysql = 0
schema_db_mysql = 'telegram'
jack_frocio = "************************"
jaden_picio = "************************"
general_purpose = "************************"
bkp_mysql = "************************"
mysql_data_location = "************************"
logs_data_location = "************************"
target_user = [
    "jackinyellow"
    ,"gweiffin"
    ,"The_Bias"
        ]
chat = {
    000000000000000000 : "************************"
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
    ,"error": "processing_errors"
}

file_types = {
    "voice": ".mp3"
    ,"photo": ".jpg"
    ,"video": ".mp4"
}