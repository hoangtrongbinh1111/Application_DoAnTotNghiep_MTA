from typing import List, Union

from beanie import PydanticObjectId

from models.admin import Admin
from models.student import Student
from models.device import Device

admin_collection = Admin
student_collection = Student
device_collection = Device

'''
    ADMIN
'''

async def add_admin(new_admin: Admin) -> Admin:
    admin = await new_admin.create()
    return admin

'''
    STUDENT
'''

async def retrieve_students() -> List[Student]:
    students = await student_collection.all().to_list()
    return students


async def add_student(new_student: Student) -> Student:
    student = await new_student.create()
    return student


async def retrieve_student(id: PydanticObjectId) -> Student:
    student = await student_collection.get(id)
    if student:
        return student


async def delete_student(id: PydanticObjectId) -> bool:
    student = await student_collection.get(id)
    if student:
        await student.delete()
        return True


async def update_student_data(id: PydanticObjectId, data: dict) -> Union[bool, Student]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in des_body.items()
    }}
    student = await student_collection.get(id)
    if student:
        await student.update(update_query)
        return student
    return False

'''
    IoT Device
'''
async def retrieve_devices() -> List[Device]:
    devices = await device_collection.all().to_list()
    return devices


async def add_device(new_device: Device) -> Device:
    device = await new_device.create()
    return device


async def retrieve_device(id: PydanticObjectId) -> Device:
    device = await device_collection.get(id)
    if device:
        return device


async def delete_device(id: PydanticObjectId) -> bool:
    device = await device_collection.get(id)
    if device:
        await device.delete()
        return True


async def update_device_data(id: PydanticObjectId, data: dict) -> Union[bool, Device]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in des_body.items()
    }}
    device = await device_collection.get(id)
    if device:
        await device.update(update_query)
        return device
    return False
