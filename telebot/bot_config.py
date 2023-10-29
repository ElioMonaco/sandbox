import telebot
import random
import datetime
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine, func
import numpy as np
import requests
import json

user_db = '**********'
passw_db = '*********************'
host_db =  'localhost'
port_db = 3306
schema_db = 'telegram'

general_purpose = "******************************"
target_user = [
    "name3"
    ,"name2"
    ,"name1"
        ]
chat = {
    "[PLACEHOLDER ID]": "[PLACEHOLDER NAME]"
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

def define_connector(user, passw, host, port, schema):
    connection_string = 'mysql://'+str(user)+':'+str(passw)+'@'+str(host)+':'+str(port)+'/'+str(schema)
    print("connecting to:", connection_string)
    return create_engine(connection_string, echo=False)

def get_current_unix():
    return int(datetime.datetime.now().timestamp())
