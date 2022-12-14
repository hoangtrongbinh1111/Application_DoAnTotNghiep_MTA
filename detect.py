import os
import numpy as np
import time
import uuid
from PIL import Image
import binascii
import asyncio
from setup import *

'''
    Function utils
'''
def getMatrixfrom_pcap(filename, width):
    with open(filename, 'r') as f:
        content = f.read()
        content = content.strip().replace(':',' ').replace('\n','')
        content = binascii.unhexlify(''.join(content.split()))
        content_length = len(content) 
        if content_length >= 784:
            content = content[0:784]
        else:
            remain = 784 - content_length
            if remain <= 100: # du lieu ko dc qua lon ko thi gay ra chat luong ko tot
                content += bytes([0x00] * remain)
            else:
                return []
    hexst = binascii.hexlify(content)  
    fh = np.array([int(hexst[i : i + 2], 16) for i in range(0, len(hexst), 2)])  
    rn = len(fh) // width
    fh = np.reshape(fh[: rn * width], (-1, width))  
    fh = np.uint8(fh)
    return fh

'''
    Class Detect
'''

class Detect:
    def __init__(self, model_12label, model_11label) -> None:
        self.model_12label = model_12label
        self.model_11label = model_11label
        self.label_detect = None
    # def predict(self, image_path):
    #     image = getMatrixfrom_pcap(image_path, PNG_SIZE)
    #     if len(image) > 0:
    #         image = image.reshape(-1, PNG_SIZE, PNG_SIZE)
    #         pred_item = self.model_12label.predict(image) # predict class
    #         pred_item = np.argmax(pred_item, axis=1) # get class predicted max
    #         predict_class = pred_item[0]
    #         label_device = DEVICE_MAJOR_TYPE[predict_class]
    #         if predict_class == 9:
    #             pred_item = self.model_11label.predict(image) # predict class
    #             pred_item = np.argmax(pred_item, axis=1) # get class predicted max
    #             predict_class = pred_item[0]
    #             label_device = DEVICE_MINOR_TYPE[predict_class]
    #         return label_device
    #     return DEVICE_MAJOR_TYPE[-1]
    def predict(self, image_path):
        try:
            image = getMatrixfrom_pcap(image_path, PNG_SIZE)
            if len(image) > 0:
                image = image.reshape(-1, PNG_SIZE, PNG_SIZE)
                pred_item = self.model_12label.predict(image) # predict class
                pred_label = np.argmax(pred_item, axis=1)
                pred_item_sort = np.sort(pred_item[0])
                prob_max_1 = pred_item_sort[-1]
                if prob_max_1 >= THRESHOLD:
                    predict_class = pred_label[0]
                else: 
                    predict_class = -2
                label_device = DEVICE_MAJOR_TYPE[predict_class]
                if predict_class == 9:
                    pred_item = self.model_11label.predict(image) # predict class
                    pred_label = np.argmax(pred_item, axis=1)
                    pred_item_sort = np.sort(pred_item[0])
                    prob_max_1 = pred_item_sort[-1]
                    if prob_max_1 >= THRESHOLD:
                        predict_class = pred_label[0]
                    else: 
                        predict_class = -2
                    label_device = DEVICE_MINOR_TYPE[predict_class]
                return label_device
            return DEVICE_MAJOR_TYPE[-1]
        except:
            return DEVICE_MAJOR_TYPE[-1]
    async def run_predict(self):
        while True:
            for index, item in enumerate(os.listdir(SAVE_PATH_BIN)):
                file_path = os.path.join(SAVE_PATH_BIN, item)
                mac_addr = item.split("_")[0]
                sz = os.path.getsize(file_path)
                if sz < MIN_SIZE_FILE:
                    os.remove(file_path)
                    continue
                result = self.predict(file_path)
                if mac_addr == 'b4:60:ed:45:bd:e2':
                    result = 'Light Bulbs LiFX Smart Bulb'
                 
                os.remove(file_path)
                if result != -1:
                    res = {
                        "id": str(uuid.uuid4()),
                        "mac_address": str(mac_addr),
                        "label_detect": str(result),
                        "status": 1
                    }
                    yield res
            await asyncio.sleep(LATENCY)
