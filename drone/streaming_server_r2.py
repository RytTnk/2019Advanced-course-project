#! /usr/bin/env python
# -*- coding: utf-8 -*-

#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Include library -----
import socket

import configparser
import d3dshot
import numpy as np
import cv2

import sys
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
        self.IMG_FPS = int(self.config.get('packet', 'image_fps'))
        self.HEADER_SIZE = int(self.config.get('bytes', 'header_size'))
        self.IMAGE_WIDTH = int(self.config.get('pixels', 'image_width'))
        self.IMAGE_HEIGHT = int(self.config.get('pixels', 'image_height'))
        self.IMAGE_QUALITY = int(self.config.get('pixels', 'image_quality'))
        self.PHOTO_IMG_X = int(self.config.get('pixels', 'photo_image_x'))
        self.PHOTO_IMG_Y = int(self.config.get('pixels', 'photo_image_y'))
        self.PHOTO_IMG_W = int(self.config.get('pixels', 'photo_image_w'))
        self.PHOTO_IMG_H = int(self.config.get('pixels', 'photo_image_h'))
        # Setting for debug string
        self.INDENT = '    '

        ## For control FPS
        self.start_time = time.perf_counter()
        self.fps = 0.0
        self.delay_time = 0.0

        ## For D3Dshot module
        self.d = d3dshot.create(capture_output="numpy")
        x = 0
        y = 0
        width = self.IMAGE_WIDTH
        height = self.IMAGE_HEIGHT
        self.d.capture(region=(x, y, x+width, y+height))
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
        print(self.fps)
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
    # ----- Get image processing -----
    ######################################################################
    ## @brief      Get image processing
    ######################################################################
    def get_img_proc(self):
        self.img = self.d.get_latest_frame()
        left   = self.PHOTO_IMG_X
        top    = self.PHOTO_IMG_Y
        right  = self.PHOTO_IMG_X + self.PHOTO_IMG_W
        bottom = self.PHOTO_IMG_Y + self.PHOTO_IMG_H
        self.img = self.img[top : bottom, left : right]
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Transmit prepare setting processing -----
    ######################################################################
    ## @brief      Transmit prepare setting processing
    ######################################################################
    def transmit_prepare_set_proc(self):
        # Create socket comunication object
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.SERVER_IP, self.SERVER_PORT))

        print("Wait for communication.")
        self.s.listen(1)
        self.soc, self.addr = self.s.accept()
        print("Start transmit to "+str(self.addr)+".")
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Transmit to client processing -----
    ######################################################################
    ## @brief      Transmit to client processing
    ######################################################################
    def transmit_to_client_proc(self):
        # Default return value
        ret = 1

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
            print('Closed connection.')
            ret = 0

        return ret
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

    # Prepare socket communication
    ss_utility = streaming_server_utility()
    init_flg = 0

    while (True):
        if init_flg == 1:
            # Set timer counter
            ss_utility.set_time_proc()

            # Transmit image to client
            ss_utility.get_img_proc()
            init_flg = ss_utility.transmit_to_client_proc()

            # Control and calc fps
            ss_utility.ctrl_fps_proc()
            ss_utility.calc_fps_proc()

            # Print for debug
            #ss_utility.print_fps_proc()
            #ss_utility.print_delay_time_proc()
        else:
            ss_utility.transmit_prepare_set_proc()

            init_flg = 1


if __name__ == '__main__':
    main_proc()
