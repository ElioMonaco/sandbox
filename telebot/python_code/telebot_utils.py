import telebot
import random
import datetime
import os.path
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine, func
import numpy as np
import requests
import json
from re import search
import pandas as pd
from bot_config import *
import zipfile 

def define_connector(user, passw, host, port, schema):
    connection_string = 'mysql://'+str(user)+':'+str(passw)+'@'+str(host)+':'+str(port)+'/'+str(schema)
    print("connecting to:", connection_string)
    return create_engine(connection_string, echo=False)

def get_current_unix():
    return int(datetime.datetime.now().timestamp())

def time_string(fmt):
    return datetime.datetime.now().strftime(fmt)

def get_latest_file(engine, message, message_type):
    return pd.read_sql("""SELECT DISTINCT m.message_id
                                            ,m.message_timestamp
                                            ,a.file_id
                            FROM telegram.messages AS m 
                            INNER JOIN telegram."""+message_table_mapping[message_type]+""" AS a 
                                ON a.chat_id = m.from_chat 
                                AND a.message_id = m.message_id
                            WHERE m.message_type = '"""+message_type+"""' 
                                AND m.from_chat = '"""+str(message.chat.id)+"""'
                            ORDER BY m.message_timestamp DESC
                            LIMIT """+str(message.text.split()[2]), engine).drop(columns = ["message_id", "message_timestamp"]).drop_duplicates()

def raw_df(message):
    return pd.DataFrame([[str(message)
                                ,pd.Timestamp.utcnow()
                            ]]
                        ,columns = [
                            "message"
                            ,"insert_time"
                        ])

def user_df(message):
    return pd.DataFrame([[message.chat.id
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

def type_df(message):
    return pd.DataFrame({"message_type": [message.content_type]})

def chat_df(message):
    return pd.DataFrame([[message.chat.id
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

def message_df(message, pinned):
    first_df = pd.DataFrame([[message.json['message_id']
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
    elif pinned and "text" in message.json["pinned_message"]:
        text_item = message.json["pinned_message"]["text"]
    elif "new_chat_title" in message.json:
        text_item = message.json["new_chat_title"] 
    elif "caption" in message.json:
        text_item = message.json["caption"] 
    elif "caption" in message.json["pinned_message"]:
        text_item = message.json["pinned_message"]["caption"] 
    else: 
        text_item = None
    first_df.insert(5, "text", text_item, True)
    forward_from_item = message.json["forward_from"]["id"] if "forward_from" in message.json else None
    first_df.insert(7, "forward_from_user", forward_from_item, True)
    forward_timestamp_item = message.json["forward_date"] if "forward_date" in message.json else None
    first_df.insert(8, "forward_timestamp", forward_timestamp_item, True)
    reply_item = message.json["reply_to_message"]["message_id"] if "reply_to_message" in message.json else None
    first_df.insert(9, "reply_to_message", reply_item, True)
    return first_df

def entity_df(message):
    first_df = pd.DataFrame.from_dict(message.json["entities"], orient = "columns")
    first_df.insert(0, "message_id", [message.json["message_id"] for i in range(len(message.json["entities"]))], True)
    first_df.insert(1, "chat_id", [message.json["chat"]["id"] for i in range(len(message.json["entities"]))], True)
    first_df.insert(5, "insert_time", [pd.Timestamp.utcnow() for i in range(len(message.json["entities"]))], True)
    return first_df
    
def photo_df(message, pinned):
    if pinned:
        photo_item = message.json["pinned_message"]["photo"] if "photo" in message.json["pinned_message"] else message.json["pinned_message"]["new_chat_photo"]
    else:
        photo_item = message.json["photo"] if "photo" in message.json else message.json["new_chat_photo"]
    first_df = pd.DataFrame.from_dict(photo_item, orient = "columns")
    first_df.insert(0, "message_id", [message.json["message_id"] for i in range(len(photo_item))], True)
    first_df.insert(1, "chat_id", [message.json["chat"]["id"] for i in range(len(photo_item))], True)
    first_df.insert(6, "insert_time", [pd.Timestamp.utcnow() for i in range(len(photo_item))], True)
    return first_df

def poll_df(message, pinned):
    poll_item = message.json["pinned_message"]["poll"] if pinned else message.json["poll"]
    first_df = pd.DataFrame.from_dict(poll_item["options"], orient = "columns")
    first_df.insert(0, "poll_id", [poll_item["id"] for i in range(len(poll_item["options"]))], True)
    first_df.insert(3, "insert_time", [pd.Timestamp.utcnow() for i in range(len(poll_item["options"]))], True)
    second_df = pd.DataFrame([[message.json['message_id']
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
    return first_df, second_df

def voice_df(message, pinned):
    voice_item = message.json["pinned_message"]["voice"] if pinned else message.json["voice"]
    return pd.DataFrame([[message.json['message_id']
                            ,message.json["chat"]["id"]
                            ,voice_item["duration"]
                            ,voice_item["mime_type"]
                            ,voice_item["file_id"]
                            ,voice_item["file_unique_id"]
                            ,voice_item["file_size"]
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

def video_df(message, pinned):
    video_item = message.json["pinned_message"]["video"] if pinned else message.json["video"]
    return pd.DataFrame([[message.json['message_id']
                            ,message.json["chat"]["id"]
                            ,video_item["file_id"]
                            ,video_item["file_unique_id"]
                            ,video_item["width"]
                            ,video_item["height"]
                            ,video_item["duration"]
                            ,video_item["file_name"]
                            ,video_item["mime_type"]
                            ,video_item["file_size"]
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

def sticker_df(message, pinned):
    sticker_item = message.json["pinned_message"]["sticker"] if pinned else message.json["sticker"]
    return pd.DataFrame([[message.json['message_id']
                            ,message.json["chat"]["id"]
                            ,sticker_item["file_id"]
                            ,sticker_item["file_unique_id"]
                            ,sticker_item["type"]
                            ,sticker_item["width"]
                            ,sticker_item["height"]
                            ,sticker_item["is_animated"]
                            ,sticker_item["is_video"]
                            ,sticker_item["emoji"]
                            ,sticker_item["set_name"]
                            ,sticker_item["mask_position"]
                            ,sticker_item["file_size"]
                            ,sticker_item["premium_animation"]
                            ,sticker_item["custom_emoji_id"]
                            ,sticker_item["needs_repainting"]
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

def location_df(message, pinned):
    if pinned:
        location_item = message.json["pinned_message"]["location"]
        horizontal_accuracy = location_item["horizontal_accuracy"] if "horizontal_accuracy" in location_item else None
        live_period = location_item["live_period"] if "live_period" in location_item else None
        heading = location_item["heading"] if "heading" in location_item else None
        proximity_alert_radius = location_item["proximity_alert_radius"] if "proximity_alert_radius" in location_item else None

        return pd.DataFrame([[message.json['message_id']
                              ,message.json["chat"]["id"]
                              ,location_item["latitude"]
                              ,location_item["longitude"]
                              ,horizontal_accuracy
                              ,live_period
                              ,heading
                              ,proximity_alert_radius
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
    
    else:
        return pd.DataFrame([[message.json['message_id']
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

def contact_df(message, pinned):
    if pinned:
        contact_item = message.json["pinned_message"]["contact"]
        phone_number = contact_item["phone_number"] if "phone_number" in contact_item else None
        user_id = contact_item["user_id"] if "user_id" in contact_item else None
        first_name = contact_item["first_name"] if "first_name" in contact_item else None
        last_name = contact_item["last_name"] if "last_name" in contact_item else None
        vcard = contact_item["vcard"] if "vcard" in contact_item else None

        return pd.DataFrame([[message.json['message_id']
                              ,message.json["chat"]["id"]
                              ,phone_number
                              ,user_id
                              ,first_name
                              ,last_name
                              ,vcard
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
    
    else:
        return pd.DataFrame([[message.json['message_id']
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

def error_df(message, step, step_nbr, **kwargs):
    extraoption = kwargs.get("error_message", None)
    is_error = True if extraoption != None else False
    return pd.DataFrame([[message.json['message_id']
                              ,message.json["chat"]["id"]
                              ,step
                              ,step_nbr
                              ,is_error
                              ,extraoption
                              ,pd.Timestamp.utcnow()  
                        ]]
                        ,columns = [
                              "message_id"
                              ,"chat_id"
                              ,"step"
                              ,"step_number"
                              ,"is_error"
                              ,"error_message"      
                              ,"insert_time"
                             ])

def run_bot(bot_instance, times):
    for i in range(times):
        print("attempt number "+str(i))
        try:
            bot_instance.infinity_polling()
        except:
            print("attempt number "+str(i)+" failed")

def download_files(what_files, message, bot_instance, bot_key):

    for index, row in what_files.iterrows():

        try:

            query = "https://api.telegram.org/bot"+str(bot_key)+"/getFile"
                        
            response = requests.get(query
                                    ,data = {'file_id': row["file_id"]})
            downloaded = requests.get("https://api.telegram.org/file/bot"+str(bot_key)+"/"+str(json.loads(response.content)["result"]["file_path"]))

            if response.status_code == 200 and downloaded.status_code == 200:
                
                destination = message.text.split()[3] if len(message.text.split()) > 3 else "C:\\Users\\monac\\Downloads\\"
                path = os.path.join(destination, row["file_id"]+file_types[message.text.split()[1]])
                file_info = bot_instance.get_file(row["file_id"])
                downloaded_file = bot_instance.download_file(file_info.file_path)
                with open(path,'wb') as new_file:
                    new_file.write(downloaded_file)
                bot_instance.reply_to(message, "downloaded "+str(index)+"th file")

            else:

                bot_instance.send_message(message.chat.id, "Error: Unable to download the file.")

        except Exception as e:

            bot_instance.send_message(message.chat.id, f"Error: {str(e)}")

def get_files(what_files, message, bot_instance, bot_key):

    for index, row in what_files.iterrows():

        print(row["file_id"])
        try:

            if str(message.text.split()[1]) == "photo":

                bot_instance.send_photo(message.chat.id, row["file_id"])
            
            elif str(message.text.split()[1]) == "voice":

                bot_instance.send_voice(message.chat.id, row["file_id"])

            elif str(message.text.split()[1]) == "video":

                bot_instance.send_video(message.chat.id, row["file_id"])
            
            else:

                bot_instance.reply_to(message, "'"+str(message.text.split()[1])+"' not yet supported")

        except Exception as e:

            bot_instance.send_message(message.chat.id, f"Error: {str(e)}")

def backup_database(db_host, db_user, db_passwd, db_name, bkp_path, time_name_format, source, log_file):
    
    f = open(log_file,'a')
    original_path = os.getcwd()
    backup_file = os.path.join(bkp_path, db_name, time_string(time_name_format))
    db_path = os.path.join(source, db_name)
    exe_path = os.path.join("C:\\", "Program Files", "MySQL", "MySQL Server 8.0", "bin")
    
    if os.path.exists(db_path):
        
        f.write("=====================================================================================================\n")
        f.write("["+str(pd.Timestamp.now())+f"]: changing directory to {exe_path}\n")

        try:
            os.chdir(exe_path)
            f.write("["+str(pd.Timestamp.now())+f"]: done.\n")
        except Exception as err:
                f.write("["+str(pd.Timestamp.now())+"]: could not perform the action due to the following error: "+str(err)+"\n")

        dump_cmd = f".\mysqldump -h {db_host} -u {db_user} -p{db_passwd} {db_name} > {backup_file}.sql"
        f.write("["+str(pd.Timestamp.now())+f"]: writing back up into {backup_file}.sql with command {dump_cmd}...\n")

        try:
            os.system(dump_cmd)
            f.write("["+str(pd.Timestamp.now())+f"]: done.\n")
        except Exception as err:
                f.write("["+str(pd.Timestamp.now())+"]: could not perform the action due to the following error: "+str(err)+"\n")

        f.write("["+str(pd.Timestamp.now())+f"]: changing directory to {original_path}\n")

        try:
            os.chdir(original_path)
            f.write("["+str(pd.Timestamp.now())+f"]: done.\n")
        except Exception as err:
                f.write("["+str(pd.Timestamp.now())+"]: could not perform the action due to the following error: "+str(err)+"\n")

        f.write("["+str(pd.Timestamp.now())+f"]: compressing {backup_file}.sql to {backup_file}.zip...\n")

        try:
            zip = zipfile.ZipFile(f"{backup_file}.zip", "w", zipfile.ZIP_DEFLATED)
            zip.write(f"{backup_file}.sql")
            zip.close()
            f.write("["+str(pd.Timestamp.now())+f"]: done.\n")
        except Exception as err:
                f.write("["+str(pd.Timestamp.now())+"]: could not perform the action due to the following error: "+str(err)+"\n")

        f.write("["+str(pd.Timestamp.now())+f"]: removing {backup_file}.sql...\n")

        try:
            os.remove(f"{backup_file}.sql")
            f.write("["+str(pd.Timestamp.now())+f"]: done.\n")
        except Exception as err:
                f.write("["+str(pd.Timestamp.now())+"]: could not perform the action due to the following error: "+str(err)+"\n")

        f.write("=====================================================================================================\n")
        f.close()
        
    else:
        f.write("["+str(pd.Timestamp.now())+f"could not find the requested database '{db_name}'")
        f.write("=====================================================================================================\n")
        f.close()

def attempt_insert(message, step, step_nbr, sql_engine, log_file, **kwargs):
    pinned = kwargs.get("pinned", False)

    try:

        if step == "raw_messages":
                dataframe_insert = raw_df(message)
        elif step == "users_staging":
            dataframe_insert = user_df(message)
        elif step == "message_types_staging":
            dataframe_insert = type_df(message)
        elif step == "chats_staging":
            dataframe_insert = chat_df(message)
        elif step == "messages":
            dataframe_insert = message_df(message, pinned)
        elif step == "message_entities":
            dataframe_insert = entity_df(message)
        elif step == "message_photos":
            dataframe_insert = photo_df(message, pinned)
        elif step == "message_polls":
            dataframe_insert2, dataframe_insert = poll_df(message, pinned)
        elif step == "message_audios":
            dataframe_insert = voice_df(message, pinned)
        elif step == "message_videos":
            dataframe_insert = video_df(message, pinned)
        elif step == "message_stickers":
            dataframe_insert = sticker_df(message, pinned)
        elif step == "message_locations":
            dataframe_insert = location_df(message, pinned)
        elif step == "message_contacts":
            dataframe_insert = contact_df(message, pinned)
        
        dataframe_insert.to_sql(name = step, con = sql_engine, if_exists = 'append', index=False)
        log_file.write("["+str(pd.Timestamp.now())+"]: done\n")
        error_df(message, step, step_nbr).to_sql(name = message_table_mapping["error"], con = sql_engine, if_exists = 'append', index=False)
        if step == "message_polls":
            dataframe_insert2.to_sql(name = message_table_mapping["poll_option"], con = sql_engine, if_exists = 'append', index=False)
    
    except Exception as err:
        log_file.write("["+str(pd.Timestamp.now())+"]: could not perform the action due to the following error: "+str(err)+"\n")
        error_df(message, step, step_nbr, error_message = err).to_sql(name = message_table_mapping["error"], con = sql_engine, if_exists = 'append', index=False)

def attempt_exec(message, step, step_nbr, sql_engine, log_file):

    try:

        sql_engine.execute(step)
        log_file.write("["+str(pd.Timestamp.now())+"]: done\n")
        error_df(message, step, step_nbr).to_sql(name = message_table_mapping["error"], con = sql_engine, if_exists = 'append', index=False)

    except Exception as err:
        log_file.write("["+str(pd.Timestamp.now())+"]: could not perform the action due to the following error: "+str(err)+"\n")
        error_df(message, step, step_nbr, error_message = err).to_sql(name = message_table_mapping["error"], con = sql_engine, if_exists = 'append', index=False)