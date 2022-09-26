from fastapi import APIRouter, Body

from database.database import *
from models.device import *

router = APIRouter()


@router.get("/", response_description="Devices retrieved", response_model=Response)
async def get_devices():
    devices = await retrieve_devices()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Devices data retrieved successfully",
        "data": devices
    }


@router.get("/{id}", response_description="Device data retrieved", response_model=Response)
async def get_device_data(id: PydanticObjectId):
    device = await retrieve_device(id)
    if device:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Device data retrieved successfully",
            "data": device
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "device doesn't exist",
    }


@router.post("/", response_description="Device data added into the database", response_model=Response)
async def add_device_data(device: Device = Body(...)):
    new_device = await add_device(device)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Device created successfully",
        "data": new_device
    }


@router.delete("/{id}", response_description="Device data deleted from the database")
async def delete_device_data(id: PydanticObjectId):
    deleted_device = await delete_device(id)
    if deleted_device:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Device with ID: {} removed".format(id),
            "data": deleted_device
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "device with id {0} doesn't exist".format(id),
        "data": False
    }


@router.put("{id}", response_model=Response)
async def update_device(id: PydanticObjectId, req: UpdateDeviceModel = Body(...)):
    updated_device = await update_device_data(id, req.dict())
    if updated_device:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Device with ID: {} updated".format(id),
            "data": updated_device
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "An error occurred. Device with ID: {} not found".format(id),
        "data": False
    }
