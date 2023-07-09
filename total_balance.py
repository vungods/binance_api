import uvicorn
from fastapi import FastAPI
import json
from time import sleep
import datetime

app = FastAPI()
from functions import *


# @app.get("/")
# async def root():
#     current_balance = get_current_USDT_blance()
#     order_json = {"total": f"{current_balance}", "time": f"{datetime.datetime.now()}"}
#     order_json = json.dumps(order_json)
#     with open("transaction_history.log", "a") as file:
#         file.write(f"{order_json}\n")
#     data = []
#     with open("transaction_history.log") as file:
#         for line in file:
#             order = json.loads(line)
#             get_time(line)
#             data.append(order)
#     return {"data": data}


@app.get("/get-current-usdt-balance/")
async def root():
    current_balance = get_current_USDT_blance()
    order_json = {"total": f"{current_balance}", "time": f"{datetime.datetime.now()}"}
    return {"data": order_json}



@app.get("/get-data")
async def get_data():
    with open('data.json') as file:
        lines = file.readlines()
        if lines:
            last_line = lines[-1].strip()
            latest_data = json.loads(last_line)
        else:
            latest_data = {}
    
    return {"data": latest_data}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
