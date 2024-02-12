#https://www.youtube.com/watch?v=P_SIZDsI3Ro

import json
import websocket
import uuid
from time import sleep
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine, func


def on_message(ws, message):
    global mydf
    message = json.loads(message)
    mydf = to_dataframe(message)
    #print(mydf)
    mydf.to_sql(name = "currency_events", con = sql_engine, if_exists = 'append', index = False)
    sleep(300)

def to_dataframe(source):
    dict = {}
    dict["Stream"] = str(source["stream"])
    dict["EventType"] = str(source["data"]["e"])
    dict["EventTimestamp"] = int(source["data"]["E"])
    dict["Symbol"] = str(source["data"]["s"])
    dict["KlineStartTime"] = int(source["data"]["k"]["t"])
    dict["KlineCloseTime"] = int(source["data"]["k"]["T"])
    dict["Interval"] = str(source["data"]["k"]["i"])
    dict["FirstTradeId"] = int(source["data"]["k"]["f"])
    dict["LastTradeId"] = int(source["data"]["k"]["L"])
    dict["OpenPrice"] = float(source["data"]["k"]["o"])
    dict["ClosePrice"] = float(source["data"]["k"]["c"])
    dict["HighPrice"] = float(source["data"]["k"]["h"])
    dict["LowPrice"] = float(source["data"]["k"]["l"])
    dict["BaseAssetVolume"] = str(source["data"]["k"]["v"])
    dict["NumberOfTrades"] = int(source["data"]["k"]["n"])
    dict["IsKlineClosed"] = bool(source["data"]["k"]["x"])
    dict["QuoteAssetVolume"] = str(source["data"]["k"]["q"])
    dict["TakerBuyBaseAssetVolume"] = str(source["data"]["k"]["V"])
    dict["TakerBuyQuoteAssetVolume"] = str(source["data"]["k"]["Q"])
    df = pd.DataFrame([dict])
    df["InsertTimestamp"] = pd.Timestamp.utcnow()
    df["TransactionId"] = str(uuid.uuid4())
    return df

def define_connector(server_type, user, passw, host, port, schema):
    connection_string = str(server_type) + '://'+str(user)+':'+str(passw)+'@'+str(host)+':'+str(port)+'/'+str(schema)
    print("connecting to:", connection_string)
    return create_engine(connection_string, echo=False)

symbol = "BTCUSDT"
asset = symbol.lower() + "@kline_5m"
socket = "wss://stream.binance.com:9443/stream?streams=" + asset
ws = websocket.WebSocketApp(socket, on_message = on_message)
user_db_mysql = 'root'
passw_db_mysql = '*****************'
host_db_mysql =  'localhost'
port_db_mysql = 0
schema_db_mysql = 'crypto'
sql_engine = define_connector("mysql", user_db_mysql, passw_db_mysql, host_db_mysql, port_db_mysql, schema_db_mysql)