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

# 画像設定
config = configparser.ConfigParser()
config.read('./connection.ini', 'UTF-8')

IMAGE_WIDTH = int(config.get('packet', 'image_width'))
IMAGE_HEIGHT = int(config.get('packet', 'image_height'))
IMAGE_QUALITY = 100

# 全体の設定
FPS = int(config.get('packet', 'fps'))
INDENT = '    '

# サーバ設定
SERVER_IP = config.get('server', 'ip')
SERVER_PORT = int(config.get('server', 'port'))

# パケット設定
HEADER_SIZE = int(config.get('packet', 'header_size'))

# クライアントに接続
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER_IP, SERVER_PORT))
s.listen(1)
soc, addr = s.accept()

print('Server {')
print(INDENT + 'IP   : {},'.format(SERVER_IP))
print(INDENT + 'PORT : {}'.format(SERVER_PORT))
print('}')

# クライアント情報表示
print('Client {')
print(INDENT + 'IP   : {},'.format(addr[0]))
print(INDENT + 'PORT : {}'.format(addr[1]))
print('}')

# 計測用
now_time = time.time()
old_time = now_time

# メインループ
while True:
    loop_start_time = time.time()

    # 送信用画像データ作成
    x = 0
    y = 0
    width = IMAGE_WIDTH
    height = IMAGE_HEIGHT
    img = np.asarray(ImageGrab.grab(bbox=(x, y, x+width, y+height)))
    img = img[:, :, [2, 1, 0]]

    # データ圧縮
    #resized_img = cv2.resize(img, (IMAGE_WIDTH, IMAGE_HEIGHT))
    resized_img = img
    (status, encoded_img) = cv2.imencode('.jpg', resized_img, [int(cv2.IMWRITE_JPEG_QUALITY), IMAGE_QUALITY])
    #encoded_img = img

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
    time.sleep(max(0, 1 / FPS - (time.time() - loop_start_time)))

    #sleep_time = max(0, 1 / FPS - (time.time() - loop_start_time))
    #print(sleep_time)

    #now_time = time.time()
    #print(1.0/(now_time-old_time))
    #old_time = now_time

s.close()