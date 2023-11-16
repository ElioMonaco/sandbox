from telebot_utils import *

sql_engine = define_connector(user_db, passw_db, host_db, port_db, schema_db)
bot = telebot.TeleBot(general_purpose)
commands = list(messages["command_messages"].keys())
dataframe_types = pd.read_sql('SELECT * FROM telegram.message_types', sql_engine)
dataframe_timestamp = pd.read_sql('SELECT MAX(message_timestamp) AS value FROM telegram.messages', sql_engine)
messages_from_time = dataframe_timestamp["value"][0] if dataframe_timestamp.count()[0] == 1 else get_current_unix()
message_types = list(dataframe_types["message_type"])
log_file = os.path.join(logs_data_location, time_string("%Y%m%d")+"_GPbot_logs")

@bot.message_handler(commands = commands)

def send_welcome(message):
    
    if message.date > messages_from_time:

        command_received = message.text.split()[0].replace("/", "")

        if command_received != "scrape" and command_received not in ["getfile","downloadfile"]:

            for reply in range(len(messages["command_messages"][command_received])):

                bot.reply_to(message, messages["command_messages"][command_received][reply])

        elif command_received == "scrape":

            messages["command_messages"][command_received] = False if messages["command_messages"][command_received] else True
            reply = "chat scraping on. Da adesso in poi tutti i messaggi saranno registrati, salvati su un database e forniti alle autorità competenti" if messages["command_messages"][command_received] else "chat scraping off"
            bot.reply_to(message, reply)  

        elif command_received == "downloadfile" and len(message.text.split()) > 2:

            if message.text.split()[1] not in message_types:

                bot.reply_to(message, "'"+str(message.text.split()[1])+"' is not a valid file type")
            
            else: 

                download_files(get_latest_file(engine = sql_engine, message = message, message_type = message.text.split()[1])
                               ,message = message
                               ,bot_instance = bot
                               ,bot_key = general_purpose)
                
        elif command_received == "getfile" and len(message.text.split()) > 2:

            if message.text.split()[1] not in message_types:

                bot.reply_to(message, "'"+str(message.text.split()[1])+"' is not a valid file type")
            
            else: 

                get_files(get_latest_file(engine = sql_engine, message = message, message_type = message.text.split()[1])
                            ,message = message
                            ,bot_instance = bot
                            ,bot_key = general_purpose)
                bot.reply_to(message, "here are last "+str(message.text.split()[2])+" '"+str(message.text.split()[1])+"' message(s) ever sent in this chat")
                


        if messages["command_messages"]["scrape"]:

            f = open(log_file,'a')
            f.write("["+str(pd.Timestamp.now())+"]: begin transaction for message "+str(message.json['message_id'])+" from user "+str(message.from_user.id)+" from chat "+str(message.chat.id)+". Logs from scraper function.\n")
            f.write("["+str(pd.Timestamp.now())+"]: appending raw message to database...\n")
            raw_message = raw_df(message)
            raw_message.to_sql(name = message_table_mapping["raw"], con = sql_engine, if_exists = 'append', index=False)
            f.write("["+str(pd.Timestamp.now())+"]: done\n")

            f.write("["+str(pd.Timestamp.now())+"]: appending user to staging...\n")
            message_user = user_df(message)
            message_user.to_sql(name = message_table_mapping["user"], con = sql_engine, if_exists = 'append', index=False)
            f.write("["+str(pd.Timestamp.now())+"]: done\n")
            f.write("["+str(pd.Timestamp.now())+"]: merging staging user with final user registry...\n")
            sql_engine.execute("CALL `telegram`.`update_users`();")
            f.write("["+str(pd.Timestamp.now())+"]: done\n")

            f.write("["+str(pd.Timestamp.now())+"]: appending message type to staging...\n")
            message_type = type_df(message)
            message_type.to_sql(name = message_table_mapping["type"], con = sql_engine, if_exists = 'append', index=False)
            f.write("["+str(pd.Timestamp.now())+"]: done\n")
            f.write("["+str(pd.Timestamp.now())+"]: merging staging message types with final message types registry...\n")
            sql_engine.execute("CALL `telegram`.`update_message_types`();")
            f.write("["+str(pd.Timestamp.now())+"]: done\n")

            f.write("["+str(pd.Timestamp.now())+"]: appending chat to staging...\n")
            message_chat = chat_df(message)
            message_chat.to_sql(name = message_table_mapping["chat"], con = sql_engine, if_exists = 'append', index=False)
            f.write("["+str(pd.Timestamp.now())+"]: done\n")
            f.write("["+str(pd.Timestamp.now())+"]: merging staging chats with final chats registry...\n")
            sql_engine.execute("CALL telegram.update_chats();")
            f.write("["+str(pd.Timestamp.now())+"]: done\n")

            f.write("["+str(pd.Timestamp.now())+"]: writing message to database...\n")
            message_item = message_df(message)
            message_item.to_sql(name = message_table_mapping["message"], con = sql_engine, if_exists = 'append', index=False)
            
            if "entities" in message.json:

                message_entity = entity_df(message)
                message_entity.to_sql(name = message_table_mapping["entity"], con = sql_engine, if_exists = 'append', index=False)

            f.write("["+str(pd.Timestamp.now())+"]: done\n")
            f.write("=====================================================================================================\n")
            f.close()
        
@bot.message_handler(content_types = message_types)
def scrape_message(message):

    if message.date > messages_from_time:

        if messages["command_messages"]["scrape"]:

            f = open(log_file,'a')
            f.write("["+str(pd.Timestamp.now())+"]: begin transaction for message "+str(message.json['message_id'])+" from user "+str(message.from_user.id)+" from chat "+str(message.chat.id)+". Logs from scraper function.\n")
            f.write("["+str(pd.Timestamp.now())+"]: appending raw message to database...\n")
            raw_message = raw_df(message)
            raw_message.to_sql(name = message_table_mapping["raw"], con = sql_engine, if_exists = 'append', index=False)
            f.write("["+str(pd.Timestamp.now())+"]: done\n")

            f.write("["+str(pd.Timestamp.now())+"]: appending user to staging...\n")
            message_user = user_df(message)
            message_user.to_sql(name = message_table_mapping["user"], con = sql_engine, if_exists = 'append', index=False)
            f.write("["+str(pd.Timestamp.now())+"]: done\n")
            f.write("["+str(pd.Timestamp.now())+"]: merging staging user with final user registry...\n")
            sql_engine.execute("CALL `telegram`.`update_users`();")
            f.write("["+str(pd.Timestamp.now())+"]: done\n")

            f.write("["+str(pd.Timestamp.now())+"]: appending message type to staging...\n")
            message_type = type_df(message)
            message_type.to_sql(name = message_table_mapping["type"], con = sql_engine, if_exists = 'append', index=False)
            f.write("["+str(pd.Timestamp.now())+"]: done\n")
            f.write("["+str(pd.Timestamp.now())+"]: merging staging message types with final message types registry...\n")
            sql_engine.execute("CALL `telegram`.`update_message_types`();")
            f.write("["+str(pd.Timestamp.now())+"]: done\n")

            f.write("["+str(pd.Timestamp.now())+"]: appending chat to staging...\n")
            message_chat = chat_df(message)
            message_chat.to_sql(name = message_table_mapping["chat"], con = sql_engine, if_exists = 'append', index=False)
            f.write("["+str(pd.Timestamp.now())+"]: done\n")
            f.write("["+str(pd.Timestamp.now())+"]: merging staging chats with final chats registry...\n")
            sql_engine.execute("CALL telegram.update_chats();")
            f.write("["+str(pd.Timestamp.now())+"]: done\n")

            f.write("["+str(pd.Timestamp.now())+"]: writing message to database...\n")
            message_item = message_df(message)
            message_item.to_sql(name = message_table_mapping["message"], con = sql_engine, if_exists = 'append', index=False)
            
            if "entities" in message.json:

                message_entity = entity_df(message)
                message_entity.to_sql(name = message_table_mapping["entity"], con = sql_engine, if_exists = 'append', index=False)

            if "photo" in message.json or "new_chat_photo" in message.json:

                message_photo = photo_df(message)
                message_photo.to_sql(name = message_table_mapping["photo"], con = sql_engine, if_exists = 'append', index=False)

            if "pinned_message" in message.json:
                
                if "poll" in message.json["pinned_message"]:

                    message_poll_options, message_poll = poll_df(message)
                    message_poll_options.to_sql(name = message_table_mapping["poll_option"], con = sql_engine, if_exists = 'append', index=False)
                    message_poll.to_sql(name = message_table_mapping["poll"], con = sql_engine, if_exists = 'append', index=False)
                
            if "voice" in message.json:
                
                message_audio = voice_df(message)
                message_audio.to_sql(name = message_table_mapping["voice"], con = sql_engine, if_exists = 'append', index=False)
            
            if "video" in message.json:
                message_video = video_df(message)
                message_video.to_sql(name = message_table_mapping["video"], con = sql_engine, if_exists = 'append', index=False)
            
            if "sticker" in message.json:
                message_sticker = sticker_df(message)
                message_sticker.to_sql(name = message_table_mapping["sticker"], con = sql_engine, if_exists = 'append', index=False)

            if "location" in message.json:
                message_location = location_df(message)
                message_location.to_sql(name = message_table_mapping["location"], con = sql_engine, if_exists = 'append', index=False)

            if "contact" in message.json:
                message_contact = contact_df(message)
                message_contact.to_sql(name = message_table_mapping["contact"], con = sql_engine, if_exists = 'append', index=False)
            f.write("["+str(pd.Timestamp.now())+"]: done\n")
            f.write("=====================================================================================================\n")
            f.close()

backup_database(db_host = host_db
                ,db_user = user_db
                ,db_passwd = passw_db
                ,db_name = schema_db
                ,bkp_path = bkp_mysql
                ,time_name_format = "%Y%m%d-%H%M%S"
                ,source = mysql_data_location,
                log_file = log_file)

run_bot(bot_instance = bot, times = 100)