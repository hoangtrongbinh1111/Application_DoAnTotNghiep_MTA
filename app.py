import os
import time
from pcap_splitter.splitter import PcapSplitter
import subprocess

FILE_EXTRACT = "/home/hoangtrongbinh/HoangTrongBinh/DoAnUngDung/dataset/WIRESHARK_FILE"
DIR_EXTRACT = "/home/hoangtrongbinh/HoangTrongBinh/DoAnUngDung/dataset/PCAP"
SAVE_PATH_BIN = "/home/hoangtrongbinh/HoangTrongBinh/DoAnUngDung/dataset/PAYLOAD"

COUNTER = 0
'''
    Handle convert file pcap to bin
'''
def _handlePcapToBin():
    for ind, it in enumerate(os.listdir(FILE_EXTRACT)):
        file_extract_path = os.path.join(FILE_EXTRACT, it)
        ps = PcapSplitter(file_extract_path)
        print(ps.split_by_session(DIR_EXTRACT, pkts_bpf_filter="tcp"))
        for index, item in enumerate(os.listdir(DIR_EXTRACT)):
            listdir_item = os.path.join(DIR_EXTRACT, item)
            file_save_path_bin = os.path.join(SAVE_PATH_BIN,f"iot_{COUNTER}_{ind}_{index}.bin")
            try:
                os.system(f"tshark -2 -r {listdir_item} -T fields -e tcp.payload > {file_save_path_bin}")
                os.remove(listdir_item)
            except FileNotFoundError:
                print("File error!")
        os.remove(file_extract_path)

'''
    Infinite loop to check item in folder
'''
while(True):
    print("Start check file in folder!!!")
    if os.listdir(FILE_EXTRACT):
        _handlePcapToBin()
        COUNTER += 1
    print("End check file in folder and wait for 60s to recheck!!!")
    time.sleep(60)




''' TEST '''

# def _handlePcapToBin():
#     list_file_extract = os.listdir(FILE_EXTRACT)
#     for ind, it in enumerate(list_file_extract):
#         file_extract_path = os.path.join(FILE_EXTRACT, it)
#         ps = PcapSplitter(file_extract_path)
#         print(ps.split_by_session(DIR_EXTRACT, pkts_bpf_filter="tcp"))
#         list_dir_extract = os.listdir(DIR_EXTRACT)
#         for index, item in enumerate(list_dir_extract):
#             listdir_item = os.path.join(DIR_EXTRACT, item)
#             file_save_path_bin = os.path.join(SAVE_PATH_BIN,f"iot_{COUNTER}_{ind}_{index}.bin")
#             try:
#                 os.system(f"tshark -2 -r {listdir_item} -T fields -e tcp.payload > {file_save_path_bin}")
#             except FileNotFoundError:
#                 print("File error!")
#     # remove file
#     for ind, it in enumerate(list_file_extract):
#         file_extract_path = os.path.join(FILE_EXTRACT, it)
#         os.remove(file_extract_path)
#     for index, item in enumerate(list_dir_extract):
#         listdir_item = os.path.join(DIR_EXTRACT, item)
#         os.remove(listdir_item)


