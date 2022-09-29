
import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager
from detect import Detect
from tensorflow.keras.models import load_model
import uvicorn
from auth.jwt_bearer import JWTBearer
from config.config import initiate_database
from routes.admin import router as AdminRouter
from routes.student import router as StudentRouter
from routes.device import router as DeviceRouter
from routes.log import router as LogRouter
from models.log import *
from database.database import add_log
import json
import logging
import sys
import asyncio
import time
import datetime

app = FastAPI()
token_listener = JWTBearer()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
sio = SocketManager(app=app)

model_12label = load_model("/home/hoangtrongbinh/HoangTrongBinh/DoAnUngDung/server/model/checkpoint_best_12label.hdf5")
model_11label = load_model("/home/hoangtrongbinh/HoangTrongBinh/DoAnUngDung/server/model/checkpoint_best_11label.hdf5")
detect = Detect(model_12label, model_11label)

'''
    API 
'''
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Do An MTA server API!"}

app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
app.include_router(StudentRouter, tags=["Students"], prefix="/student", dependencies=[Depends(token_listener)])
app.include_router(DeviceRouter, tags=["Devices"], prefix="/device", dependencies=[Depends(token_listener)])
app.include_router(LogRouter, tags=["Logs"], prefix="/log", dependencies=[Depends(token_listener)])

'''
    Server Fast API and SocketIO
'''

@app.sio.on('join')
async def handle_join(sid, *args, **kwargs):
    counter = 0


@sio.on('test')
async def test(sid, *args, **kwargs):
    print(args)
    #await sio.emit('lobby', 'joe')

'''
    Start up with application
'''
async def do_stuff():
    async for response in detect.run_predict():
        log = Log(id=response["id"],mac_address = response["mac_address"], label_detect = response["label_detect"], time_detect = datetime.datetime.now(), status = response["status"])
        await log.insert()
        await sio.emit('notify_detect_iot_device', json.dumps(response))

@app.on_event('startup')
async def app_startup():
    asyncio.create_task(initiate_database())
    asyncio.create_task(do_stuff())

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        stream=sys.stdout)

    uvicorn.run("app:app", host="0.0.0.0", port=5678, reload=True, debug=True)