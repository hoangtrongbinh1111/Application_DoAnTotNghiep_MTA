from fastapi import APIRouter, Body

from database.database import *
from models.log import *

router = APIRouter()


@router.get("/", response_description="Logs retrieved", response_model=Response)
async def get_logs():
    logs = await retrieve_logs()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Logs data retrieved successfully",
        "data": logs
    }

@router.post("/", response_description="Log data added into the database", response_model=Response)
async def add_log_data(log: Log = Body(...)):
    new_log = await add_log(log)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Log created successfully",
        "data": new_log
    }