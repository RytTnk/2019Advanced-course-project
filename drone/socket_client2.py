# -*- coding: utf-8 -*-

#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Include library -----
import socket
import numpy as np
import cv2

import configparser
import time
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

    config_header_size = int(config.get('bytes', 'header_size'))
    config_image_width = int(config.get('pixels', 'image_width'))
    config_image_height = int(config.get('pixels', 'image_height'))
    config_image_fps = int(config.get('packet', 'fps'))


    # 通信用設定
    buff = bytes()
    PACKET_HEADER_SIZE = config_header_size
    IMAGE_WIDTH = config_image_width
    IMAGE_HEIGHT = config_image_height

    # 表示設定
    allow_stretch = True
    VIEW_FPS = config_image_fps
    VIEW_WIDTH = config_image_width
    VIEW_HEIGHT = config_image_height

    # 計測用
    now_time = time.time()
    old_time = time.time()

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#ソケットオブジェクト作成

    #soc.connect(("192.168.11.100", 50000))#サーバー側のipと使用するポート(ポートはサーバーと同じにする。)
    #soc.connect(("192.168.5.53", 50000))#サーバー側のipと使用するポート(ポートはサーバーと同じにする。)
    #soc.connect(("10.208.46.153", 50000))#サーバー側のipと使用するポート(ポートはサーバーと同じにする。)
    soc.connect((SERVER_IP, SERVER_PORT))    # サーバー側PCのipと使用するポート


    print("接続完了")

    while(1):
        # サーバからのデータをバッファに蓄積
        data = soc.recv(IMAGE_HEIGHT * IMAGE_WIDTH * 3)
        buff += data

        # 最新のパケットの先頭までシーク
        # バッファに溜まってるパケット全ての情報を取得
        packet_head = 0
        packets_info = list()
        while True:
            if len(buff) >= packet_head + PACKET_HEADER_SIZE:
                binary_size = int.from_bytes(buff[packet_head:packet_head + PACKET_HEADER_SIZE], 'big')
                if len(buff) >= packet_head + PACKET_HEADER_SIZE + binary_size:
                    packets_info.append((packet_head, binary_size))
                    packet_head += PACKET_HEADER_SIZE + binary_size
                else:
                    break
            else:
                break

        # バッファの中に完成したパケットがあれば、画像を更新
        if len(packets_info) > 0:
            # 最新の完成したパケットの情報を取得
            packet_head, binary_size = packets_info.pop()
            # パケットから画像のバイナリを取得
            img_bytes = buff[packet_head + PACKET_HEADER_SIZE:packet_head + PACKET_HEADER_SIZE + binary_size]
            # バッファから不要なバイナリを削除
            buff = buff[packet_head + PACKET_HEADER_SIZE + binary_size:]

            # 画像をバイナリから復元
            img = np.frombuffer(img_bytes, dtype=np.uint8)
            img = cv2.imdecode(img, 1)

            cv2.imshow('img',img)

            # 画像を表示用に加工
            #img = cv2.flip(img, 0)
            #img = cv2.resize(img, (VIEW_WIDTH, VIEW_HEIGHT))
            # 画像をバイナリに変換
            #img = img.tostring()

            # 作成した画像をテクスチャに設定
            #img_texture = Texture.create(size=(VIEW_WIDTH, VIEW_HEIGHT), colorfmt='bgr')
            #img_texture.blit_buffer(img, colorfmt='bgr', bufferfmt='ubyte')
            #texture = img_texture

            now_time = time.time()
            print(1.0/(now_time-old_time))
            old_time = now_time
            #time.sleep(1)

        k = cv2.waitKey(1)
        if k== 13 :
            break

    cv2.destroyAllWindows() # 作成したウィンドウを破棄


if __name__ == '__main__':
    main_proc()
