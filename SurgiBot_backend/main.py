from typing import Union
from fastapi import FastAPI, UploadFile, File, WebSocket
import os
import json
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from meca_rbt import *

# Meca500 IP
ip = "192.168.0.100:10000" # command port

app = FastAPI()
app.Robot = mecaRbt(ip="192.168.0.100:10000")

origins = [
    "http://localhost:8000",  # React's default port
    "http://localhost:8080",  # Vue's default port
    "http://localhost:1420",
    # Add other origins if necessary
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/api")
async def root():
    return {"message": "[SurgiBot Backend]: Connected"}

@app.get("/robot/deactivate")
async def deactivate():
    try:
        app.Robot.rbtDeactivate()
    except Exception as e:
        return {"message": f"[SurgiBot Backend]: {e}"}
    
    return {"message": "[SurgiBot Backend]: deactivated"}


# Pydantic model for registration data
class JointAngle(BaseModel):
    joint: str

@app.post('/api/moveJoint')
async def moveJoint(message:JointAngle):
    message = message.joint
    try:
        message = json.loads(message)
        print("[SurgiBot Backend] message received: ", message)
        if len(message) == 6:
            app.Robot.moveRbtJoints(10, message)
            return {"message": "[SurgiBot Backend]: robot move done"}
        else:
            return {"message": "[SurgiBot Backend]: Joints input not correct"}
    except Exception as e:
        return {"message": f"[SurgiBot Backend]: {e}"}

# Pydantic model for registration data
class cartPose(BaseModel):
    pose: str

@app.post('/api/movePose')
async def movePose(message:cartPose):
    message = message.pose
    try:
        message = json.loads(message)
        print("[SurgiBot Backend] message received: ", message)
        if len(message) == 6:
            app.Robot.moveRbtPose(10, message)
            return {"message": "[SurgiBot Backend]: robot move done"}
        else:
            return {"message": "[SurgiBot Backend]: Pose input not correct"}
    except Exception as e:
        return {"message": f"[SurgiBot Backend]: {e}"}


# Pydantic model for registration data
class JogCommand(BaseModel):
    jog_dir: str
    jog_step: float

@app.post('/api/jog')
async def moveJoint(message:JogCommand):
    jog_dir = message.jog_dir
    jog_step = message.jog_step
    try:
        print("[SurgiBot Backend] message received: ", message)
        if (jog_step and jog_dir):
            app.Robot.jogRbt(10, jog_dir, jog_step)
            return {"message": "[SurgiBot Backend]: robot move done"}
        else:
            return {"message": "[SurgiBot Backend]: Joints input not correct"}
    except Exception as e:
        return {"message": f"[SurgiBot Backend]: {e}"}


# import threading
# import asyncio
# import time
# from starlette.websockets import WebSocketDisconnect

# @app.websocket("/ws")
# async def getMecaRbt(websocket:WebSocket):
#     await websocket.accept()
#     print("[SurgiBot Backend]: WebSocket Connected")
#     # await websocket.send_text(f"[SurgiBot Backend]: txt from backend websocket")
    
#     try:
#         while True:
#             send_message_task = asyncio.create_task(send_message(websocket))
#             done, pending = await asyncio.wait(
#                 {send_message_task},
#                 return_when=asyncio.FIRST_COMPLETED,
#             )
#             for task in pending:
#                 task.cancel()
#             for task in done:
#                 task.result()
#     except WebSocketDisconnect:
#         pass
    
# async def send_message(websocket: WebSocket):
#     joints = getJoints(ip)
#     await websocket.send_text(str(joints))
#     await asyncio.sleep(1)
    