from bot_config import *

sql_engine = define_connector(user_db, passw_db, host_db, port_db, schema_db)
current_time = get_current_unix()
bot = telebot.TeleBot(general_purpose)
commands = list(messages["command_messages"].keys())
dataframe_types = pd.read_sql('SELECT * FROM telegram.message_types', sql_engine)
message_types = list(dataframe_types["message_type"])

@bot.message_handler(commands = commands)
def send_welcome(message):
    command_received = message.text.replace("/", "")
    if command_received != "scrape":
        for reply in range(len(messages["command_messages"][command_received])):
            bot.reply_to(message, messages["command_messages"][command_received][reply])
    elif command_received == "scrape":
        messages["command_messages"][command_received] = False if messages["command_messages"][command_received] else True
        reply = "chat scraping on. Da adesso in poi tutti i messaggi saranno registrati, salvati su un database e forniti alle autorità competenti" if messages["command_messages"][command_received] else "chat scraping off"
        bot.reply_to(message, reply)  

    if messages["command_messages"]["scrape"]:
        f = open(str(datetime.datetime.now().year)+"_"+str(datetime.datetime.now().month)+"_"+str(datetime.datetime.now().day)+"_GPbot_logs",'a')
        
        f.write("["+str(pd.Timestamp.now())+"]: begin trnsaction for message "+str(message.json['message_id'])+" from user "+str(message.from_user.id)+" from chat "+str(message.chat.id)+". Logs from command function.\n")
        f.write("["+str(pd.Timestamp.now())+"]: appending user to staging...\n")
        message_user = pd.DataFrame([[message.chat.id
                                                       ,message.from_user.id
                                                       ,message.from_user.is_bot
                                                       ,message.from_user.first_name
                                                       ,message.from_user.username
                                                       ,message.from_user.last_name
                                                       ,message.from_user.language_code
                                                       ,message.from_user.can_join_groups
                                                       ,message.from_user.can_read_all_group_messages
                                                       ,message.from_user.supports_inline_queries
                                                       ,message.from_user.is_premium
                                                       ,message.from_user.added_to_attachment_menu]]
                                              ,columns = [
                                                  "original_chat_id"
                                                  ,"user_id"
                                                  ,"is_bot"
                                                  ,"first_name"
                                                  ,"username"
                                                  ,"last_name"
                                                  ,"language_code"
                                                  ,"can_join_groups"
                                                  ,"can_read_all_group_messages"
                                                  ,"supports_inline_queries"
                                                  ,"is_premium"
                                                  ,"added_to_attachment_menu"
                                              ])
        message_user.to_sql(name = 'users_staging', con = sql_engine, if_exists = 'append', index=False)
        f.write("["+str(pd.Timestamp.now())+"]: done\n")
        f.write("["+str(pd.Timestamp.now())+"]: merging staging user with final user registry...\n")
        sql_engine.execute("CALL `telegram`.`update_users`();")
        f.write("["+str(pd.Timestamp.now())+"]: done\n")
        f.write("["+str(pd.Timestamp.now())+"]: appending message type to staging...\n")
        message_type = pd.DataFrame({"message_type": [message.content_type]})
        message_type.to_sql(name = 'message_types_staging', con = sql_engine, if_exists = 'append', index=False)
        f.write("["+str(pd.Timestamp.now())+"]: done\n")
        f.write("["+str(pd.Timestamp.now())+"]: merging staging message types with final message types registry...\n")
        sql_engine.execute("CALL `telegram`.`update_message_types`();")
        f.write("["+str(pd.Timestamp.now())+"]: done\n")
        f.write("["+str(pd.Timestamp.now())+"]: appending chat to staging...\n")
        message_chat = pd.DataFrame([[message.chat.id
                                        ,message.chat.type
                                        ,message.chat.title
                                        ,message.chat.username
                                        ,message.chat.first_name
                                        ,message.chat.last_name
                                        ,message.chat.is_forum
                                        ,message.chat.photo
                                        ,message.chat.bio
                                        ,message.chat.join_to_send_messages
                                        ,message.chat.join_by_request
                                        ,message.chat.has_private_forwards
                                        ,message.chat.has_restricted_voice_and_video_messages
                                        ,message.chat.description
                                        ,message.chat.invite_link
                                        ,message.chat.pinned_message
                                        ,message.chat.permissions
                                        ,message.chat.slow_mode_delay
                                        ,message.chat.message_auto_delete_time
                                        ,message.chat.has_protected_content
                                        ,message.chat.sticker_set_name
                                        ,message.chat.can_set_sticker_set
                                        ,message.chat.linked_chat_id
                                        ,message.chat.location
                                        ,message.chat.active_usernames
                                        ,message.chat.emoji_status_custom_emoji_id
                                        ,message.chat.has_hidden_members
                                        ,message.chat.has_aggressive_anti_spam_enabled
                                        ,message.chat.emoji_status_expiration_date]]
                                              ,columns = [
                                                  "chat_id"
                                                    ,"type"
                                                    ,"title"
                                                    ,"username"
                                                    ,"first_name"
                                                    ,"last_name"
                                                    ,"is_forum"
                                                    ,"photo"
                                                    ,"bio"
                                                    ,"join_to_send_messages"
                                                    ,"join_by_request"
                                                    ,"has_private_forwards"
                                                    ,"has_restricted_voice_and_video_messages"
                                                    ,"description"
                                                    ,"invite_link"
                                                    ,"pinned_message"
                                                    ,"permissions"
                                                    ,"slow_mode_delay"
                                                    ,"message_auto_delete_time"
                                                    ,"has_protected_content"
                                                    ,"sticker_set_name"
                                                    ,"can_set_sticker_set"
                                                    ,"linked_chat_id"
                                                    ,"location"
                                                    ,"active_usernames"
                                                    ,"emoji_status_custom_emoji_id"
                                                    ,"has_hidden_members"
                                                    ,"has_aggressive_anti_spam_enabled"
                                                    ,"emoji_status_expiration_date"])
        message_chat.to_sql(name = 'chats_staging', con = sql_engine, if_exists = 'append', index=False)
        f.write("["+str(pd.Timestamp.now())+"]: done\n")
        f.write("["+str(pd.Timestamp.now())+"]: merging staging chats with final chats registry...\n")
        sql_engine.execute("CALL telegram.update_chats();")
        f.write("["+str(pd.Timestamp.now())+"]: done\n")

        f.write("["+str(pd.Timestamp.now())+"]: writing message to database...\n")
        message_item = pd.DataFrame([[message.json['message_id']
                                        ,message.content_type
                                        ,message.json["from"]["id"]
                                        ,message.json["chat"]["id"]
                                        ,message.json["date"]
                                        ,pd.Timestamp.utcnow()  
                                      ]]
                                              ,columns = [
                                                  "message_id"
                                                    ,"message_type"
                                                    ,"from_user"
                                                    ,"from_chat"
                                                    ,"message_timestamp"
                                                    ,"insert_time"
                                                   ])
        
        text_item = message.json["text"] if "text" in message.json else None
        message_item.insert(5, "text", text_item, True)
        forward_from_item = message.json["forward_from"]["id"] if "forward_from" in message.json else None
        message_item.insert(7, "forward_from_user", forward_from_item, True)
        forward_timestamp_item = message.json["forward_date"] if "forward_date" in message.json else None
        message_item.insert(8, "forward_timestamp", forward_timestamp_item, True)
        message_item.to_sql(name = 'messages', con = sql_engine, if_exists = 'append', index=False)
        
        if "entities" in message.json:
            message_entity = pd.DataFrame.from_dict(message.json["entities"], orient = "columns")
            message_entity.insert(0, "message_id", [message.json["message_id"] for i in range(len(message.json["entities"]))], True)
            message_entity.insert(1, "chat_id", [message.json["chat"]["id"] for i in range(len(message.json["entities"]))], True)
            message_entity.insert(5, "insert_time", [pd.Timestamp.utcnow() for i in range(len(message.json["entities"]))], True)
            message_entity.to_sql(name = 'message_entities', con = sql_engine, if_exists = 'append', index=False)

        if "photo" in message.json:
            message_photo = pd.DataFrame.from_dict(message.json["photo"], orient = "columns")
            message_photo.insert(0, "message_id", [message.json["message_id"] for i in range(len(message.json["photo"]))], True)
            message_photo.insert(1, "chat_id", [message.json["chat"]["id"] for i in range(len(message.json["photo"]))], True)
            caption = message.json["caption"] if "caption" in message.json else None
            message_photo.insert(2, "caption", [caption for i in range(len(message.json["photo"]))], True)
            message_photo.insert(7, "insert_time", [pd.Timestamp.utcnow() for i in range(len(message.json["photo"]))], True)
            message_photo.to_sql(name = 'message_photos', con = sql_engine, if_exists = 'append', index=False)
            
        if "voice" in message.json:
            
            message_audio = pd.DataFrame([[message.json['message_id']
                                        ,message.json["chat"]["id"]
                                        ,message.json["voice"]["duration"]
                                        ,message.json["voice"]["mime_type"]
                                        ,message.json["voice"]["file_id"]
                                        ,message.json["voice"]["file_unique_id"]
                                        ,message.json["voice"]["file_size"]
                                        ,pd.Timestamp.utcnow()  
                                      ]]
                                              ,columns = [
                                                  "message_id"
                                                    ,"chat_id"
                                                    ,"duration"
                                                    ,"mime_type"
                                                    ,"file_id"
                                                    ,"file_unique_id"
                                                    ,"file_size"
                                                    ,"insert_time"
                                                   ])
            message_audio.to_sql(name = 'message_audios', con = sql_engine, if_exists = 'append', index=False)
        f.write("["+str(pd.Timestamp.now())+"]: done\n")
        f.write("=====================================================================================================\n")
        f.close()
        
@bot.message_handler(content_types = message_types)
def scrape_message(message):
    if messages["command_messages"]["scrape"]:
        f = open(str(datetime.datetime.now().year)+"_"+str(datetime.datetime.now().month)+"_"+str(datetime.datetime.now().day)+"_GPbot_logs",'a')
        
        f.write("["+str(pd.Timestamp.now())+"]: begin trnsaction for message "+str(message.json['message_id'])+" from user "+str(message.from_user.id)+" from chat "+str(message.chat.id)+". Logs from scraper function.\n")
        f.write("["+str(pd.Timestamp.now())+"]: appending user to staging...\n")
        message_user = pd.DataFrame([[message.chat.id
                                                       ,message.from_user.id
                                                       ,message.from_user.is_bot
                                                       ,message.from_user.first_name
                                                       ,message.from_user.username
                                                       ,message.from_user.last_name
                                                       ,message.from_user.language_code
                                                       ,message.from_user.can_join_groups
                                                       ,message.from_user.can_read_all_group_messages
                                                       ,message.from_user.supports_inline_queries
                                                       ,message.from_user.is_premium
                                                       ,message.from_user.added_to_attachment_menu]]
                                              ,columns = [
                                                  "original_chat_id"
                                                  ,"user_id"
                                                  ,"is_bot"
                                                  ,"first_name"
                                                  ,"username"
                                                  ,"last_name"
                                                  ,"language_code"
                                                  ,"can_join_groups"
                                                  ,"can_read_all_group_messages"
                                                  ,"supports_inline_queries"
                                                  ,"is_premium"
                                                  ,"added_to_attachment_menu"
                                              ])
        message_user.to_sql(name = 'users_staging', con = sql_engine, if_exists = 'append', index=False)
        f.write("["+str(pd.Timestamp.now())+"]: done\n")
        f.write("["+str(pd.Timestamp.now())+"]: merging staging user with final user registry...\n")
        sql_engine.execute("CALL `telegram`.`update_users`();")
        f.write("["+str(pd.Timestamp.now())+"]: done\n")
        f.write("["+str(pd.Timestamp.now())+"]: appending message type to staging...\n")
        message_type = pd.DataFrame({"message_type": [message.content_type]})
        message_type.to_sql(name = 'message_types_staging', con = sql_engine, if_exists = 'append', index=False)
        f.write("["+str(pd.Timestamp.now())+"]: done\n")
        f.write("["+str(pd.Timestamp.now())+"]: merging staging message types with final message types registry...\n")
        sql_engine.execute("CALL `telegram`.`update_message_types`();")
        f.write("["+str(pd.Timestamp.now())+"]: done\n")
        f.write("["+str(pd.Timestamp.now())+"]: appending chat to staging...\n")
        message_chat = pd.DataFrame([[message.chat.id
                                        ,message.chat.type
                                        ,message.chat.title
                                        ,message.chat.username
                                        ,message.chat.first_name
                                        ,message.chat.last_name
                                        ,message.chat.is_forum
                                        ,message.chat.photo
                                        ,message.chat.bio
                                        ,message.chat.join_to_send_messages
                                        ,message.chat.join_by_request
                                        ,message.chat.has_private_forwards
                                        ,message.chat.has_restricted_voice_and_video_messages
                                        ,message.chat.description
                                        ,message.chat.invite_link
                                        ,message.chat.pinned_message
                                        ,message.chat.permissions
                                        ,message.chat.slow_mode_delay
                                        ,message.chat.message_auto_delete_time
                                        ,message.chat.has_protected_content
                                        ,message.chat.sticker_set_name
                                        ,message.chat.can_set_sticker_set
                                        ,message.chat.linked_chat_id
                                        ,message.chat.location
                                        ,message.chat.active_usernames
                                        ,message.chat.emoji_status_custom_emoji_id
                                        ,message.chat.has_hidden_members
                                        ,message.chat.has_aggressive_anti_spam_enabled
                                        ,message.chat.emoji_status_expiration_date]]
                                              ,columns = [
                                                  "chat_id"
                                                    ,"type"
                                                    ,"title"
                                                    ,"username"
                                                    ,"first_name"
                                                    ,"last_name"
                                                    ,"is_forum"
                                                    ,"photo"
                                                    ,"bio"
                                                    ,"join_to_send_messages"
                                                    ,"join_by_request"
                                                    ,"has_private_forwards"
                                                    ,"has_restricted_voice_and_video_messages"
                                                    ,"description"
                                                    ,"invite_link"
                                                    ,"pinned_message"
                                                    ,"permissions"
                                                    ,"slow_mode_delay"
                                                    ,"message_auto_delete_time"
                                                    ,"has_protected_content"
                                                    ,"sticker_set_name"
                                                    ,"can_set_sticker_set"
                                                    ,"linked_chat_id"
                                                    ,"location"
                                                    ,"active_usernames"
                                                    ,"emoji_status_custom_emoji_id"
                                                    ,"has_hidden_members"
                                                    ,"has_aggressive_anti_spam_enabled"
                                                    ,"emoji_status_expiration_date"])
        message_chat.to_sql(name = 'chats_staging', con = sql_engine, if_exists = 'append', index=False)
        f.write("["+str(pd.Timestamp.now())+"]: done\n")
        f.write("["+str(pd.Timestamp.now())+"]: merging staging chats with final chats registry...\n")
        sql_engine.execute("CALL telegram.update_chats();")
        f.write("["+str(pd.Timestamp.now())+"]: done\n")

        f.write("["+str(pd.Timestamp.now())+"]: writing message to database...\n")
        message_item = pd.DataFrame([[message.json['message_id']
                                        ,message.content_type
                                        ,message.json["from"]["id"]
                                        ,message.json["chat"]["id"]
                                        ,message.json["date"]
                                        ,pd.Timestamp.utcnow()  
                                      ]]
                                              ,columns = [
                                                  "message_id"
                                                    ,"message_type"
                                                    ,"from_user"
                                                    ,"from_chat"
                                                    ,"message_timestamp"
                                                    ,"insert_time"
                                                   ])
        
        text_item = message.json["text"] if "text" in message.json else None
        message_item.insert(5, "text", text_item, True)
        forward_from_item = message.json["forward_from"]["id"] if "forward_from" in message.json else None
        message_item.insert(7, "forward_from_user", forward_from_item, True)
        forward_timestamp_item = message.json["forward_date"] if "forward_date" in message.json else None
        message_item.insert(8, "forward_timestamp", forward_timestamp_item, True)
        message_item.to_sql(name = 'messages', con = sql_engine, if_exists = 'append', index=False)
        
        if "entities" in message.json:
            message_entity = pd.DataFrame.from_dict(message.json["entities"], orient = "columns")
            message_entity.insert(0, "message_id", [message.json["message_id"] for i in range(len(message.json["entities"]))], True)
            message_entity.insert(1, "chat_id", [message.json["chat"]["id"] for i in range(len(message.json["entities"]))], True)
            message_entity.insert(5, "insert_time", [pd.Timestamp.utcnow() for i in range(len(message.json["entities"]))], True)
            message_entity.to_sql(name = 'message_entities', con = sql_engine, if_exists = 'append', index=False)

        if "photo" in message.json:
            message_photo = pd.DataFrame.from_dict(message.json["photo"], orient = "columns")
            message_photo.insert(0, "message_id", [message.json["message_id"] for i in range(len(message.json["photo"]))], True)
            message_photo.insert(1, "chat_id", [message.json["chat"]["id"] for i in range(len(message.json["photo"]))], True)
            caption = message.json["caption"] if "caption" in message.json else None
            message_photo.insert(2, "caption", [caption for i in range(len(message.json["photo"]))], True)
            message_photo.insert(7, "insert_time", [pd.Timestamp.utcnow() for i in range(len(message.json["photo"]))], True)
            message_photo.to_sql(name = 'message_photos', con = sql_engine, if_exists = 'append', index=False)
            
        if "voice" in message.json:
            
            message_audio = pd.DataFrame([[message.json['message_id']
                                        ,message.json["chat"]["id"]
                                        ,message.json["voice"]["duration"]
                                        ,message.json["voice"]["mime_type"]
                                        ,message.json["voice"]["file_id"]
                                        ,message.json["voice"]["file_unique_id"]
                                        ,message.json["voice"]["file_size"]
                                        ,pd.Timestamp.utcnow()  
                                      ]]
                                              ,columns = [
                                                  "message_id"
                                                    ,"chat_id"
                                                    ,"duration"
                                                    ,"mime_type"
                                                    ,"file_id"
                                                    ,"file_unique_id"
                                                    ,"file_size"
                                                    ,"insert_time"
                                                   ])
            message_audio.to_sql(name = 'message_audios', con = sql_engine, if_exists = 'append', index=False)
        
        if "video" in message.json:
            message_video = pd.DataFrame([[message.json['message_id']
                                        ,message.json["chat"]["id"]
                                        ,message.video.file_id
                                        ,message.video.file_unique_id
                                        ,message.video.width
                                        ,message.video.height
                                        ,message.video.duration
                                        ,message.video.file_name
                                        ,message.video.mime_type
                                        ,message.video.file_size
                                        ,pd.Timestamp.utcnow()  
                                      ]]
                                              ,columns = [
                                                  "message_id"
                                                    ,"chat_id"
                                                    ,"file_id"
                                                    ,"file_unique_id"
                                                    ,"width"
                                                    ,"height"
                                                    ,"duration"
                                                    ,"file_name"
                                                    ,"mime_type"
                                                    ,"file_size"
                                                    ,"insert_time"
                                                   ])
            message_video.to_sql(name = 'message_videos', con = sql_engine, if_exists = 'append', index=False)
        f.write("["+str(pd.Timestamp.now())+"]: done\n")
        f.write("=====================================================================================================\n")
        f.close()

for i in range(1000):
    print("attempt number "+str(i))
    try:
        bot.infinity_polling()
    except:
        bot.infinity_polling()