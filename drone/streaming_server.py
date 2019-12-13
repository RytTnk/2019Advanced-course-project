#! /usr/bin/env python
# -*- coding: utf-8 -*-

#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Include library -----
import socket

import configparser
import d3dshot
import numpy as np
import cv2

import time
#_____________________________________________________________________


#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Utility of streaming server library -----
######################################################################
## @version    0.1.0
## @author     K.Ishimori
## @date       2019/12/13 Newly created.                  [K.Ishimori]
## @brief      Utility of streaming server library
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
        self.FPS = int(self.config.get('packet', 'fps'))
        self.HEADER_SIZE = int(self.config.get('bytes', 'header_size'))
        self.IMAGE_WIDTH = int(self.config.get('pixels', 'image_width'))
        self.IMAGE_HEIGHT = int(self.config.get('pixels', 'image_height'))
        self.IMAGE_QUALITY = int(self.config.get('pixels', 'image_quality'))
        # Setting for debug string
        self.INDENT = '    '

        ## For control FPS
        self.now_time = time.time()
        self.old_time = self.now_time

        ## For D3Dshot module
        self.d = d3dshot.create(capture_output="numpy")
        x = 0
        y = 0
        width = self.IMAGE_WIDTH
        height = self.IMAGE_HEIGHT
        self.d.capture(region=(x, y, x+width, y+height))
        time.sleep(1)  # Capture is non-blocking so we wait explicitely

    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Get time processing -----
    ######################################################################
    ## @brief      Get time processing
    ######################################################################
    def get_time_proc(self):
        self.now_time = time.time()
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Get image processing -----
    ######################################################################
    ## @brief      Get image processing
    ######################################################################
    def get_img_proc(self):
        self.img = self.d.get_latest_frame()
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
    #_____________________________________________________________________


    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Transmit prepare setting processing -----
    ######################################################################
    ## @brief      Transmit prepare setting processing
    ######################################################################
    def transmit_prepare_set_proc(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#ソケットオブジェクト作成
        self.s.bind((self.SERVER_IP, self.SERVER_PORT)) # サーバー側PCのipと使用するポート
        print("接続待機中")
        self.s.listen(1)                                # 接続要求を待機
        self.soc, self.addr = self.s.accept()           # 要求が来るまでブロック
        print(str(self.addr)+"と接続完了")
    #_____________________________________________________________________


    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Transmit to client processing -----
    ######################################################################
    ## @brief      Transmit to client processing
    ######################################################################
    def transmit_to_client_proc(self):
        # Processing for compressed image
        resized_img = self.img
        (status, encoded_img) = cv2.imencode('.jpg', resized_img, [int(cv2.IMWRITE_JPEG_QUALITY), self.IMAGE_QUALITY])

        # Processing for packet building
        packet_body = encoded_img.tostring()
        packet_header = len(packet_body).to_bytes(self.HEADER_SIZE, 'big')
        packet = packet_header + packet_body

        # Processing for transmit
        try:
            self.soc.sendall(packet)
        except socket.error as e:
            print('Connection closed.')
            exit()
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

    sc_utility = streaming_server_utility()

    sc_utility.transmit_prepare_set_proc()

    # 計測用
    cnt = 0
    ave = 0.0
    old_time = 0

    while (True):
        loop_start_time = time.time()

        sc_utility.get_img_proc()
        sc_utility.transmit_to_client_proc()

        # FPS制御
        #time.sleep(max(0, 1 / FPS - (time.time() - loop_start_time)))

        #sleep_time = max(0, 1 / FPS - (time.time() - loop_start_time))
        #print(sleep_time)

        now_time = time.time()

        cnt = cnt + 1
        if now_time != old_time:
            ave = ave + 1.0/(now_time-old_time)
        cycle = 10

        if cnt == cycle:
            print(ave/cycle)
            ave = 0.0
            cnt = 0

        #print(1.0/(now_time-old_time))
        old_time = now_time

        k = cv2.waitKey(1)         #↖
        if k== 13 :                #←　ENTERキーで終了
            break                  #↙

    #cam.releace()                  #カメラオブジェクト破棄


if __name__ == '__main__':
    main_proc()
