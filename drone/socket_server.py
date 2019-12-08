# -*- coding: utf-8 -*-

#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Include library -----
import socket
import numpy as np
import cv2
import time

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

    cam = cv2.VideoCapture(0)#カメラオブジェクト作成

    while (True):

        flag,img = cam.read()       #カメラから画像データを受け取る
        #img = cv2.resize(img, dsize=(480, 640))
        #height, width, channels = img.shape[:3]
        #print("width: " + str(width) + "height: " + str(height))

        img = img.tostring()        #numpy行列からバイトデータに変換
        soc.send(img)              # ソケットにデータを送信

        time.sleep(0.01)            #フリーズするなら#を外す。

        k = cv2.waitKey(1)         #↖
        if k== 13 :                #←　ENTERキーで終了
            break                  #↙

    cam.releace()                  #カメラオブジェクト破棄


if __name__ == '__main__':
    main_proc()
