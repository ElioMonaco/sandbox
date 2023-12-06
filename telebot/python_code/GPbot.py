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
            attempt_insert(message, step = message_table_mapping["raw"], step_nbr = 0, sql_engine = sql_engine, log_file = f)

            f.write("["+str(pd.Timestamp.now())+"]: appending user to staging...\n")
            attempt_insert(message, step = message_table_mapping["user"], step_nbr = 1, sql_engine = sql_engine, log_file = f)

            f.write("["+str(pd.Timestamp.now())+"]: merging staging user with final user registry...\n")
            attempt_exec(message, step = "CALL `telegram`.`update_users`();", step_nbr = 2, sql_engine = sql_engine, log_file = f)

            f.write("["+str(pd.Timestamp.now())+"]: appending message type to staging...\n")
            attempt_insert(message, step = message_table_mapping["type"], step_nbr = 3, sql_engine = sql_engine, log_file = f)

            f.write("["+str(pd.Timestamp.now())+"]: merging staging message types with final message types registry...\n")
            attempt_exec(message, step = "CALL `telegram`.`update_message_types`();", step_nbr = 4, sql_engine = sql_engine, log_file = f)

            f.write("["+str(pd.Timestamp.now())+"]: appending chat to staging...\n")
            attempt_insert(message, step = message_table_mapping["chat"], step_nbr = 5, sql_engine = sql_engine, log_file = f)

            f.write("["+str(pd.Timestamp.now())+"]: merging staging chats with final chats registry...\n")
            attempt_exec(message, step = "CALL `telegram`.`update_chats`();", step_nbr = 6, sql_engine = sql_engine, log_file = f)

            f.write("["+str(pd.Timestamp.now())+"]: writing message to database...\n")
            attempt_insert(message, step = message_table_mapping["message"], step_nbr = 7, sql_engine = sql_engine, log_file = f)
            
            step_nbr = 7
            pinned = True if "pinned_message" in message.json else False
            if "entities" in message.json:

                step_nbr += 1
                f.write("["+str(pd.Timestamp.now())+"]: writing entities to database...\n")
                attempt_insert(message, step = message_table_mapping["entity"], step_nbr = step_nbr, sql_engine = sql_engine, log_file = f, pinned = pinned)

            if "photo" in message.json or "new_chat_photo" in message.json or (pinned and ("photo" in message.json["pinned_message"] or "new_chat_photo" in message.json["pinned_message"])):
                
                step_nbr += 1
                f.write("["+str(pd.Timestamp.now())+"]: writing photos to database...\n")
                attempt_insert(message, step = message_table_mapping["photo"], step_nbr = step_nbr, sql_engine = sql_engine, log_file = f, pinned = pinned)
 
            if "poll" in message.json or (pinned and "poll" in message.json["pinned_message"]):
                
                step_nbr += 1
                f.write("["+str(pd.Timestamp.now())+"]: writing poll to database...\n")
                attempt_insert(message, step = message_table_mapping["poll"], step_nbr = step_nbr, sql_engine = sql_engine, log_file = f, pinned = pinned)
                
            if "voice" in message.json or (pinned and "voice" in message.json["pinned_message"]):
                
                step_nbr += 1
                f.write("["+str(pd.Timestamp.now())+"]: writing voice to database...\n")
                attempt_insert(message, step = message_table_mapping["voice"], step_nbr = step_nbr, sql_engine = sql_engine, log_file = f, pinned = pinned)
            
            if "video" in message.json or (pinned and "video" in message.json["pinned_message"]):

                step_nbr += 1
                f.write("["+str(pd.Timestamp.now())+"]: writing video to database...\n")
                attempt_insert(message, step = message_table_mapping["video"], step_nbr = step_nbr, sql_engine = sql_engine, log_file = f, pinned = pinned)
            
            if "sticker" in message.json or (pinned and "sticker" in message.json["pinned_message"]):

                step_nbr += 1
                f.write("["+str(pd.Timestamp.now())+"]: writing sticker to database...\n")
                attempt_insert(message, step = message_table_mapping["sticker"], step_nbr = step_nbr, sql_engine = sql_engine, log_file = f, pinned = pinned)

            if "location" in message.json or (pinned and "location" in message.json["pinned_message"]):

                step_nbr += 1
                f.write("["+str(pd.Timestamp.now())+"]: writing location to database...\n")
                attempt_insert(message, step = message_table_mapping["location"], step_nbr = step_nbr, sql_engine = sql_engine, log_file = f, pinned = pinned)

            if "contact" in message.json or (pinned and "contact" in message.json["pinned_message"]):

                step_nbr += 1
                f.write("["+str(pd.Timestamp.now())+"]: writing location to database...\n")
                attempt_insert(message, step = message_table_mapping["contact"], step_nbr = step_nbr, sql_engine = sql_engine, log_file = f, pinned = pinned)
                    
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
            attempt_insert(message, step = message_table_mapping["raw"], step_nbr = 0, sql_engine = sql_engine, log_file = f)

            f.write("["+str(pd.Timestamp.now())+"]: appending user to staging...\n")
            attempt_insert(message, step = message_table_mapping["user"], step_nbr = 1, sql_engine = sql_engine, log_file = f)

            f.write("["+str(pd.Timestamp.now())+"]: merging staging user with final user registry...\n")
            attempt_exec(message, step = "CALL `telegram`.`update_users`();", step_nbr = 2, sql_engine = sql_engine, log_file = f)

            f.write("["+str(pd.Timestamp.now())+"]: appending message type to staging...\n")
            attempt_insert(message, step = message_table_mapping["type"], step_nbr = 3, sql_engine = sql_engine, log_file = f)

            f.write("["+str(pd.Timestamp.now())+"]: merging staging message types with final message types registry...\n")
            attempt_exec(message, step = "CALL `telegram`.`update_message_types`();", step_nbr = 4, sql_engine = sql_engine, log_file = f)

            f.write("["+str(pd.Timestamp.now())+"]: appending chat to staging...\n")
            attempt_insert(message, step = message_table_mapping["chat"], step_nbr = 5, sql_engine = sql_engine, log_file = f)

            f.write("["+str(pd.Timestamp.now())+"]: merging staging chats with final chats registry...\n")
            attempt_exec(message, step = "CALL `telegram`.`update_chats`();", step_nbr = 6, sql_engine = sql_engine, log_file = f)

            f.write("["+str(pd.Timestamp.now())+"]: writing message to database...\n")
            attempt_insert(message, step = message_table_mapping["message"], step_nbr = 7, sql_engine = sql_engine, log_file = f)
            
            step_nbr = 7
            pinned = True if "pinned_message" in message.json else False
            if "entities" in message.json:

                step_nbr += 1
                f.write("["+str(pd.Timestamp.now())+"]: writing entities to database...\n")
                attempt_insert(message, step = message_table_mapping["entity"], step_nbr = step_nbr, sql_engine = sql_engine, log_file = f, pinned = pinned)

            if "photo" in message.json or "new_chat_photo" in message.json or (pinned and ("photo" in message.json["pinned_message"] or "new_chat_photo" in message.json["pinned_message"])):
                
                step_nbr += 1
                f.write("["+str(pd.Timestamp.now())+"]: writing photos to database...\n")
                attempt_insert(message, step = message_table_mapping["photo"], step_nbr = step_nbr, sql_engine = sql_engine, log_file = f, pinned = pinned)
 
            if "poll" in message.json or (pinned and "poll" in message.json["pinned_message"]):
                
                step_nbr += 1
                f.write("["+str(pd.Timestamp.now())+"]: writing poll to database...\n")
                attempt_insert(message, step = message_table_mapping["poll"], step_nbr = step_nbr, sql_engine = sql_engine, log_file = f, pinned = pinned)
                
            if "voice" in message.json or (pinned and "voice" in message.json["pinned_message"]):
                
                step_nbr += 1
                f.write("["+str(pd.Timestamp.now())+"]: writing voice to database...\n")
                attempt_insert(message, step = message_table_mapping["voice"], step_nbr = step_nbr, sql_engine = sql_engine, log_file = f, pinned = pinned)
            
            if "video" in message.json or (pinned and "video" in message.json["pinned_message"]):

                step_nbr += 1
                f.write("["+str(pd.Timestamp.now())+"]: writing video to database...\n")
                attempt_insert(message, step = message_table_mapping["video"], step_nbr = step_nbr, sql_engine = sql_engine, log_file = f, pinned = pinned)
            
            if "sticker" in message.json or (pinned and "sticker" in message.json["pinned_message"]):

                step_nbr += 1
                f.write("["+str(pd.Timestamp.now())+"]: writing sticker to database...\n")
                attempt_insert(message, step = message_table_mapping["sticker"], step_nbr = step_nbr, sql_engine = sql_engine, log_file = f, pinned = pinned)

            if "location" in message.json or (pinned and "location" in message.json["pinned_message"]):

                step_nbr += 1
                f.write("["+str(pd.Timestamp.now())+"]: writing location to database...\n")
                attempt_insert(message, step = message_table_mapping["location"], step_nbr = step_nbr, sql_engine = sql_engine, log_file = f, pinned = pinned)

            if "contact" in message.json or (pinned and "contact" in message.json["pinned_message"]):

                step_nbr += 1
                f.write("["+str(pd.Timestamp.now())+"]: writing location to database...\n")
                attempt_insert(message, step = message_table_mapping["contact"], step_nbr = step_nbr, sql_engine = sql_engine, log_file = f, pinned = pinned)
                    
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