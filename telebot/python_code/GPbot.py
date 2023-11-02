from bot_config import *

sql_engine = define_connector(user_db, passw_db, host_db, port_db, schema_db)
bot = telebot.TeleBot(general_purpose)
commands = list(messages["command_messages"].keys())
dataframe_types = pd.read_sql('SELECT * FROM telegram.message_types', sql_engine)
dataframe_timestamp = pd.read_sql('SELECT MAX(message_timestamp) AS value FROM telegram.messages', sql_engine)
messages_from_time = dataframe_timestamp["value"][0] if dataframe_timestamp.count()[0] == 1 else get_current_unix()
message_types = list(dataframe_types["message_type"])

@bot.message_handler(commands = commands) #(func = lambda message: True)
def send_welcome(message):
    if message.date > messages_from_time:
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
            
            f.write("["+str(pd.Timestamp.now())+"]: begin transaction for message "+str(message.json['message_id'])+" from user "+str(message.from_user.id)+" from chat "+str(message.chat.id)+". Logs from command function.\n")
            
            f.write("["+str(pd.Timestamp.now())+"]: appending raw message to database...\n")
            raw_message = pd.DataFrame([[str(message)
                                            ,pd.Timestamp.utcnow()  
                                        ]]
                                                ,columns = [
                                                    "message"
                                                        ,"insert_time"
                                                    ])
            raw_message.to_sql(name = 'raw_messages', con = sql_engine, if_exists = 'append', index=False)
            f.write("["+str(pd.Timestamp.now())+"]: done\n")

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
            
            if "text" in message.json:
                text_item = message.json["text"] 
            elif "pinned_message" in message.json and "text" in message.json["pinned_message"]:
                text_item = message.json["pinned_message"]["text"]
            else: 
                text_item = None
            message_item.insert(5, "text", text_item, True)
            forward_from_item = message.json["forward_from"]["id"] if "forward_from" in message.json else None
            message_item.insert(7, "forward_from_user", forward_from_item, True)
            forward_timestamp_item = message.json["forward_date"] if "forward_date" in message.json else None
            message_item.insert(8, "forward_timestamp", forward_timestamp_item, True)
            reply_item = message.json["reply_to_message"]["message_id"] if "reply_to_message" in message.json else None
            message_item.insert(9, "reply_to_message", reply_item, True)
            message_item.to_sql(name = 'messages', con = sql_engine, if_exists = 'append', index=False)
            
            if "entities" in message.json:
                message_entity = pd.DataFrame.from_dict(message.json["entities"], orient = "columns")
                message_entity.insert(0, "message_id", [message.json["message_id"] for i in range(len(message.json["entities"]))], True)
                message_entity.insert(1, "chat_id", [message.json["chat"]["id"] for i in range(len(message.json["entities"]))], True)
                message_entity.insert(5, "insert_time", [pd.Timestamp.utcnow() for i in range(len(message.json["entities"]))], True)
                message_entity.to_sql(name = 'message_entities', con = sql_engine, if_exists = 'append', index=False)

            f.write("["+str(pd.Timestamp.now())+"]: done\n")
            f.write("=====================================================================================================\n")
            f.close()
        
@bot.message_handler(content_types = message_types)
def scrape_message(message):
    if message.date > messages_from_time:
        if messages["command_messages"]["scrape"]:
            f = open(str(datetime.datetime.now().year)+"_"+str(datetime.datetime.now().month)+"_"+str(datetime.datetime.now().day)+"_GPbot_logs",'a')
            
            f.write("["+str(pd.Timestamp.now())+"]: begin transaction for message "+str(message.json['message_id'])+" from user "+str(message.from_user.id)+" from chat "+str(message.chat.id)+". Logs from scraper function.\n")
            
            f.write("["+str(pd.Timestamp.now())+"]: appending raw message to database...\n")
            raw_message = pd.DataFrame([[str(message)
                                            ,pd.Timestamp.utcnow()  
                                        ]]
                                                ,columns = [
                                                    "message"
                                                        ,"insert_time"
                                                    ])
            raw_message.to_sql(name = 'raw_messages', con = sql_engine, if_exists = 'append', index=False)
            f.write("["+str(pd.Timestamp.now())+"]: done\n")
            
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
            
            if "text" in message.json:
                text_item = message.json["text"] 
            elif "pinned_message" in message.json and "text" in message.json["pinned_message"]:
                text_item = message.json["pinned_message"]["text"]
            elif "new_chat_title" in message.json:
                text_item = message.json["new_chat_title"] 
            elif "caption" in message.json:
                text_item = message.json["caption"] 
            else: 
                text_item = None
            message_item.insert(5, "text", text_item, True)
            forward_from_item = message.json["forward_from"]["id"] if "forward_from" in message.json else None
            message_item.insert(7, "forward_from_user", forward_from_item, True)
            forward_timestamp_item = message.json["forward_date"] if "forward_date" in message.json else None
            message_item.insert(8, "forward_timestamp", forward_timestamp_item, True)
            reply_item = message.json["reply_to_message"]["message_id"] if "reply_to_message" in message.json else None
            message_item.insert(9, "reply_to_message", reply_item, True)
            message_item.to_sql(name = 'messages', con = sql_engine, if_exists = 'append', index=False)
            
            if "entities" in message.json:
                message_entity = pd.DataFrame.from_dict(message.json["entities"], orient = "columns")
                message_entity.insert(0, "message_id", [message.json["message_id"] for i in range(len(message.json["entities"]))], True)
                message_entity.insert(1, "chat_id", [message.json["chat"]["id"] for i in range(len(message.json["entities"]))], True)
                message_entity.insert(5, "insert_time", [pd.Timestamp.utcnow() for i in range(len(message.json["entities"]))], True)
                message_entity.to_sql(name = 'message_entities', con = sql_engine, if_exists = 'append', index=False)

            if "photo" in message.json or "new_chat_photo" in message.json:
                photo_item = message.json["photo"] if "photo" in message.json else message.json["new_chat_photo"]
                message_photo = pd.DataFrame.from_dict(photo_item, orient = "columns")
                message_photo.insert(0, "message_id", [message.json["message_id"] for i in range(len(photo_item))], True)
                message_photo.insert(1, "chat_id", [message.json["chat"]["id"] for i in range(len(photo_item))], True)
                caption = message.json["caption"] if "caption" in message.json else None
                message_photo.insert(2, "caption", [caption for i in range(len(photo_item))], True)
                message_photo.insert(7, "insert_time", [pd.Timestamp.utcnow() for i in range(len(photo_item))], True)
                message_photo.to_sql(name = 'message_photos', con = sql_engine, if_exists = 'append', index=False)

            if "pinned_message" in message.json:
                if "poll" in message.json["pinned_message"]:
                    poll_item = message.json["pinned_message"]["poll"]
                    message_poll_options = pd.DataFrame.from_dict(poll_item["options"], orient = "columns")
                    message_poll_options.insert(0, "poll_id", [poll_item["id"] for i in range(len(poll_item["options"]))], True)
                    message_poll_options.insert(3, "insert_time", [pd.Timestamp.utcnow() for i in range(len(poll_item["options"]))], True)
                    message_poll_options.to_sql(name = 'message_poll_options', con = sql_engine, if_exists = 'append', index=False)

                    message_poll = pd.DataFrame([[message.json['message_id']
                                            ,message.json["chat"]["id"]
                                            ,poll_item["id"]
                                            ,poll_item["question"]
                                            ,poll_item["total_voter_count"]
                                            ,poll_item["is_closed"]
                                            ,poll_item["is_anonymous"]
                                            ,poll_item["type"]
                                            ,poll_item["allows_multiple_answers"] 
                                            ,pd.Timestamp.utcnow()  
                                        ]]
                                                ,columns = [
                                                    "message_id"
                                                        ,"chat_id"
                                                        ,"poll_id"
                                                        ,"question"
                                                        ,"total_voter_count"
                                                        ,"is_closed"
                                                        ,"is_anonymous"
                                                        ,"type"
                                                        ,"allows_multiple_answers"
                                                        ,"insert_time"
                                                    ])
                    message_poll.to_sql(name = 'message_polls', con = sql_engine, if_exists = 'append', index=False)
                
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
            
            if "sticker" in message.json:
                message_sticker = pd.DataFrame([[message.json['message_id']
                                                ,message.json["chat"]["id"]
                                                ,message.sticker.file_id
                                                ,message.sticker.file_unique_id
                                                ,message.sticker.type
                                                ,message.sticker.width
                                                ,message.sticker.height
                                                ,message.sticker.is_animated
                                                ,message.sticker.is_video
                                                ,message.sticker.emoji
                                                ,message.sticker.set_name
                                                ,message.sticker.mask_position
                                                ,message.sticker.file_size
                                                ,message.sticker.premium_animation
                                                ,message.sticker.custom_emoji_id
                                                ,message.sticker.needs_repainting
                                                ,pd.Timestamp.utcnow()  
                                          ]]
                                                  ,columns = [
                                                      "message_id"
                                                        ,"chat_id"
                                                        ,"file_id"           
                                                        ,"file_unique_id"    
                                                        ,"type"              
                                                        ,"width"             
                                                        ,"height"            
                                                        ,"is_animated"       
                                                        ,"is_video"          
                                                        ,"emoji"             
                                                        ,"set_name"          
                                                        ,"mask_position"     
                                                        ,"file_size"         
                                                        ,"premium_animation" 
                                                        ,"custom_emoji_id"   
                                                        ,"needs_repainting"  
                                                        ,"insert_time"
                                                       ])
                message_sticker.to_sql(name = 'message_stickers', con = sql_engine, if_exists = 'append', index=False)

            if "location" in message.json:
                message_location = pd.DataFrame([[message.json['message_id']
                                                ,message.json["chat"]["id"]
                                                ,message.location.latitude
                                                ,message.location.longitude
                                                ,message.location.horizontal_accuracy
                                                ,message.location.live_period
                                                ,message.location.heading
                                                ,message.location.proximity_alert_radius
                                                ,pd.Timestamp.utcnow()  
                                          ]]
                                                  ,columns = [
                                                      "message_id"
                                                        ,"chat_id"
                                                        ,"latitude"           
                                                        ,"longitude"    
                                                        ,"horizontal_accuracy"              
                                                        ,"live_period"             
                                                        ,"heading"            
                                                        ,"proximity_alert_radius"       
                                                        ,"insert_time"
                                                       ])
                message_location.to_sql(name = 'message_locations', con = sql_engine, if_exists = 'append', index=False)

            if "contact" in message.json:
                message_contact = pd.DataFrame([[message.json['message_id']
                                                ,message.json["chat"]["id"]
                                                ,message.contact.phone_number
                                                ,message.contact.user_id
                                                ,message.contact.first_name
                                                ,message.contact.last_name
                                                ,message.contact.vcard
                                                ,pd.Timestamp.utcnow()  
                                          ]]
                                                  ,columns = [
                                                        "message_id"
                                                        ,"chat_id"
                                                        ,"contact_phone_number"
                                                        ,"contact_user_id"  
                                                        ,"contact_first_name"           
                                                        ,"contact_last_name"
                                                        ,"contact_vcard"       
                                                        ,"insert_time"
                                                       ])
                message_contact.to_sql(name = 'message_contacts', con = sql_engine, if_exists = 'append', index=False)
            f.write("["+str(pd.Timestamp.now())+"]: done\n")
            f.write("=====================================================================================================\n")
            f.close()

for i in range(1000):
    print("attempt number "+str(i))
    try:
        bot.infinity_polling()
    except:
        bot.infinity_polling()