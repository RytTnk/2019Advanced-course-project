# -*- coding: utf-8 -*-

#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Include library -----
import socket
import numpy as np
import cv2

import configparser
import time
import datetime

import os
import smile_intensity

import upload_file
import qr_code
#_____________________________________________________________________


#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Utility of streaming client library -----
######################################################################
## @version    0.1.0
## @author     K.Ishimori
## @date       2019/12/13 Newly created.                  [K.Ishimori]
## @brief      Utility of streaming client library
######################################################################
class streaming_server_utility:
    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Initialized utility class -----
    ######################################################################
    ## @brief      Initialized utility class
    ######################################################################
    def __init__(self):
        ## Read setting infomation file
        self.config = configparser.ConfigParser()
        self.config.read('./connection.ini', 'UTF-8')
        # Settig for server
        self.SERVER_IP = self.config.get('server', 'ip')
        self.SERVER_PORT = int(self.config.get('server', 'port'))
        # Setting for streaming condition
        self.IMG_FPS = int(self.config.get('packet', 'image_fps'))
        self.HEADER_SIZE = int(self.config.get('bytes', 'header_size'))
        self.IMAGE_WIDTH = int(self.config.get('pixels', 'image_width'))
        self.IMAGE_HEIGHT = int(self.config.get('pixels', 'image_height'))
        self.IMAGE_QUALITY = int(self.config.get('pixels', 'image_quality'))
        # Setting for debug string
        self.INDENT = '    '

        ## For control FPS
        self.start_time = time.perf_counter()
        self.fps = 0.0
        self.delay_time = 0.0
        self.fps_cnt = 0
        self.fps_ave = 0.0
        self.fps_ave_rng = 100

        ## For receive data
        self.buff = bytes()
        self.packets_info = list()

        ## Created smile intensity utility
        self.si_utility = smile_intensity.smile_intensity_utility()
        self.smile_intensity_point = 0
        self.smile_intensity_point_prev = 0
        self.smile_intensity_point_th = 30
        dt_now = datetime.datetime.now()
        self.folder_name = str(dt_now.year)+str(dt_now.month).zfill(2)+str(dt_now.day).zfill(2)+str(dt_now.hour).zfill(2)+str(dt_now.minute).zfill(2)+str(dt_now.second).zfill(2)
        print(self.folder_name)
        os.mkdir(self.folder_name)
        self.end_time = 0
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Set time processing -----
    ######################################################################
    ## @brief      Set time processing
    ######################################################################
    def set_time_proc(self):
        self.start_time = time.perf_counter()
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Print FPS processing -----
    ######################################################################
    ## @brief      Print FPS processing
    ######################################################################
    def print_fps_proc(self):
        self.fps_cnt = self.fps_cnt + 1

        if self.fps_cnt == self.fps_ave_rng:
            print(self.fps_ave / self.fps_ave_rng)
            self.fps_cnt = 0
            self.fps_ave = 0.0
        else:
            self.fps_ave = self.fps_ave + self.fps
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Print delay time processing -----
    ######################################################################
    ## @brief      Print delay time processing
    ######################################################################
    def print_delay_time_proc(self):
        print(self.delay_time)
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Print buffer size processing -----
    ######################################################################
    ## @brief      Print buffer size processing
    ######################################################################
    def print_buff_size_proc(self):
        print(len(self.buff))
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Print binary size processing -----
    ######################################################################
    ## @brief      Print binary size processing
    ######################################################################
    def print_bin_size_proc(self):
        print(self.binary_size)
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Print image processing -----
    ######################################################################
    ## @brief      Print image processing
    ######################################################################
    def print_img_proc(self):
        cv2.imshow('img',self.img)
        cv2.waitKey(1)
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Calculate FPS processing -----
    ######################################################################
    ## @brief      Calculate FPS processing
    ######################################################################
    def calc_fps_proc(self):
        diff_time = time.perf_counter() - self.start_time
        self.fps = 1.0 / diff_time
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Control FPS processing -----
    ######################################################################
    ## @brief      Control FPS processing
    ######################################################################
    def ctrl_fps_proc(self):
        diff_time = time.perf_counter() - self.start_time
        self.delay_time = max(0, (1 / self.IMG_FPS - diff_time))
        time.sleep(self.delay_time)
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Restore image processing -----
    ######################################################################
    ## @brief      Restore image processing
    ######################################################################
    def restore_img_proc(self):
        if len(self.packets_info) > 0:
            packet_head_address, binary_size = self.packets_info.pop()
            img_bytes = self.buff[packet_head_address + self.HEADER_SIZE : packet_head_address + self.HEADER_SIZE + binary_size]
            self.buff = self.buff[packet_head_address + self.HEADER_SIZE + binary_size:]

            # Restore image
            self.img = np.frombuffer(img_bytes, dtype=np.uint8)

            try:
                self.img = cv2.imdecode(self.img, 1)
            except:
                self.img = self.img_prev

            self.img_prev = self.img
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Receive prepare setting processing -----
    ######################################################################
    ## @brief      Receive prepare setting processing
    ######################################################################
    def receive_prepare_set_proc(self):
        # Create socket comunication object
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect((self.SERVER_IP, self.SERVER_PORT))
        print('Completed connection.')
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Receive to client processing -----
    ######################################################################
    ## @brief      Receive to client processing
    ######################################################################
    def receive_from_server_proc(self):
        # Processing for receive
        data = self.soc.recv(self.IMAGE_HEIGHT * self.IMAGE_WIDTH * 3)
        self.buff += data

        # Seek to latest frame
        packet_head = 0
        while True:
            if len(self.buff) >= packet_head + self.HEADER_SIZE:
                self.binary_size = int.from_bytes(self.buff[packet_head:packet_head + self.HEADER_SIZE], 'big')
                if len(self.buff) >= packet_head + self.HEADER_SIZE + self.binary_size:
                    self.packets_info.append((packet_head, self.binary_size))
                    packet_head += self.HEADER_SIZE + self.binary_size
                else:
                    break
            else:
                break
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Smile intensity processing -----
    ######################################################################
    ## @brief      Smile intensity processing
    ######################################################################
    def smile_intensity_proc(self):
        self.si_utility.smile_intensity_check_proc(self.img)
        self.smile_intensity_point = self.si_utility.store_smile_intensity_proc()
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Print smile intensity processing -----
    ######################################################################
    ## @brief      Store smile intensity processing
    ######################################################################
    def print_smile_intensity_proc(self):
        print(self.smile_intensity_point)
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Get save folder name processing -----
    ######################################################################
    ## @brief      Get save folder name processing
    ######################################################################
    def get_save_folder_name_proc(self):
        return self.folder_name
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Save smile image processing -----
    ######################################################################
    ## @brief      Save smile image processing
    ######################################################################
    def save_smile_img_proc(self):
        end_flag = 1
        dt_now = datetime.datetime.now()
        nowtime = str(dt_now.year)+str(dt_now.month).zfill(2)+str(dt_now.day).zfill(2)+str(dt_now.hour).zfill(2)+str(dt_now.minute).zfill(2)+str(dt_now.second).zfill(2)
        self.save_name = self.folder_name + '\\' + str(self.smile_intensity_point).zfill(3) + "_" + nowtime + ".png"
        if self.smile_intensity_point > self.smile_intensity_point_prev:
            cv2.imwrite(self.save_name,self.img)
            self.smile_intensity_point_prev = self.smile_intensity_point
        elif self.smile_intensity_point > self.smile_intensity_point_th:
            cv2.imwrite(self.save_name,self.img)

        if self.smile_intensity_point > self.smile_intensity_point_th:
            if self.end_time == 0:
                self.end_time = time.time() + 5
        if self.end_time != 0:
            if time.time() > self.end_time:
                print("end")
                end_flag = 0

        return end_flag

    #_____________________________________________________________________


#_____________________________________________________________________


#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Main processing -----
######################################################################
## @brief      Main processing
## @callgraph
## @callergraph
######################################################################
def main_proc():

    if 1:
        # Prepare socket communication
        ss_utility = streaming_server_utility()
        ss_utility.receive_prepare_set_proc()

        end_flag = 1
        while(end_flag):
            # Set timer counter
            ss_utility.set_time_proc()

            # Receive image from server
            ss_utility.receive_from_server_proc()
            ss_utility.restore_img_proc()

            # Smile intensity processing
            ss_utility.smile_intensity_proc()
            ss_utility.print_smile_intensity_proc()
            end_flag = ss_utility.save_smile_img_proc()

            # Calculate fps
            ss_utility.calc_fps_proc()

            # Print for debug
            #ss_utility.print_fps_proc()
            #ss_utility.print_buff_size_proc()
            #ss_utility.print_bin_size_proc()
            #ss_utility.print_img_proc()

        cv2.destroyAllWindows() # 作成したウィンドウを破棄

        # Get best smile image name
        gd_utility = upload_file.google_drive_utility()

        folder_path = ss_utility.get_save_folder_name_proc()
        gd_utility.get_file_list_proc(folder_path)
        best_smile_img_name = gd_utility.get_last_file_proc()
    else:
        folder_path = "20191219093722"
        best_smile_img_name = "100_20191219093803.png"

    target_path = folder_path + '/' + best_smile_img_name

    # Set google drive file processing
    gd_utility.set_gd_file_proc(target_path)
    # Upload google drive file processing
    gd_utility.upload_gd_file_proc()
    # Get google drive file url processing
    url = gd_utility.get_gd_file_url_proc()
    print(url)

    qr_code.create_qrcode(url)


if __name__ == '__main__':
    main_proc()
