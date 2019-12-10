# -*- coding: utf-8 -*-

#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Include library -----
import socket
import numpy as np
import cv2
import time

import d3dshot

import configparser
from PIL import ImageGrab
from PIL import Image
#_____________________________________________________________________


#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Main processing -----
######################################################################
## @brief      Main processing
## @callgraph
## @callergraph
######################################################################
def main_proc():

    # Read setting infomation file
    config = configparser.ConfigParser()
    config.read('./connection.ini', 'UTF-8')

    # サーバ設定
    SERVER_IP = config.get('server', 'ip')
    SERVER_PORT = int(config.get('server', 'port'))

    # 全体の設定
    FPS = int(config.get('packet', 'fps'))
    INDENT = '    '
    # パケット設定
    HEADER_SIZE = int(config.get('bytes', 'header_size'))

    IMAGE_WIDTH = int(config.get('pixels', 'image_width'))
    IMAGE_HEIGHT = int(config.get('pixels', 'image_height'))
    IMAGE_QUALITY = int(config.get('pixels', 'image_quality'))

    # クライアントに接続
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.bind((SERVER_IP, SERVER_PORT))
    #s.listen(1)
    #soc, addr = s.accept()

    #print('Server {')
    #print(INDENT + 'IP   : {},'.format(SERVER_IP))
    #print(INDENT + 'PORT : {}'.format(SERVER_PORT))
    #print('}')

    # クライアント情報表示
    #print('Client {')
    #print(INDENT + 'IP   : {},'.format(addr[0]))
    #print(INDENT + 'PORT : {}'.format(addr[1]))
    #print('}')

    # 計測用
    now_time = time.time()
    old_time = now_time

    d = d3dshot.create(capture_output="numpy")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#ソケットオブジェクト作成

    #s.bind(("192.168.0.15", 50000))    # サーバー側PCのipと使用するポート
    #s.bind(("192.168.5.53", 50000))    # サーバー側PCのipと使用するポート
    #print(""+SERVER_IP+"")
    s.bind((SERVER_IP, SERVER_PORT))    # サーバー側PCのipと使用するポート

    #print(SERVER_IP)
    print("接続待機中")

    s.listen(1)                     # 接続要求を待機

    soc, addr = s.accept()          # 要求が来るまでブロック

    print(str(addr)+"と接続完了")

    # 計測用
    now_time = time.time()
    old_time = 0

    cnt = 0
    ave = 0.0

    x = 0
    y = 0
    width = IMAGE_WIDTH
    height = IMAGE_HEIGHT
    d.capture(region=(x, y, x+width, y+height))
    time.sleep(3)  # Capture is non-blocking so we wait explicitely

    #cam = cv2.VideoCapture(0)#カメラオブジェクト作成

    while (True):
        loop_start_time = time.time()

        #flag,img = cam.read()       #カメラから画像データを受け取る

        # 送信用画像データ作成
        #img = np.asarray(ImageGrab.grab(bbox=(x, y, x+width, y+height)))
        #img = d.screenshot(region=(x, y, x+width, y+height))
        img = d.get_latest_frame()
        #img = img[:, :, [2, 1, 0]]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # データ圧縮
        if 1:
            resized_img = img
            (status, encoded_img) = cv2.imencode('.jpg', resized_img, [int(cv2.IMWRITE_JPEG_QUALITY), IMAGE_QUALITY])
        else:
            encoded_img = img

        # パケット構築
        packet_body = encoded_img.tostring()
        packet_header = len(packet_body).to_bytes(HEADER_SIZE, 'big')
        packet = packet_header + packet_body

        # パケット送信
        try:
            soc.sendall(packet)
        except socket.error as e:
            print('Connection closed.')
            break

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
