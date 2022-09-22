
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager
from detect import Detect
from tensorflow.keras.models import load_model
import uvicorn
import json
import logging
import sys
import asyncio

app = FastAPI()
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
        await sio.emit('notify_detect_iot_device', json.dumps(response))

@app.on_event('startup')
async def app_startup():
    asyncio.create_task(do_stuff())
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        stream=sys.stdout)

    uvicorn.run("app:app", host="0.0.0.0", port=5678, reload=True, debug=True)