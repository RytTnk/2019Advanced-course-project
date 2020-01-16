#! /usr/bin/env python
# -*- coding: utf-8 -*-

#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Include library -----
import pyautogui as pgui

import time
import msvcrt as ms
#_____________________________________________________________________


#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Utility of control drone library -----
######################################################################
## @version    0.1.0
## @author     K.Ishimori
## @date       2020/01/16 Newly created.                  [K.Ishimori]
## @brief      Utility of control drone library
######################################################################
class control_drone_utility:
    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Initialized utility class -----
    ######################################################################
    ## @brief      Initialized utility class
    ######################################################################
    def __init__(self):
        self.init = False
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Take off processing -----
    ######################################################################
    ## @brief      Take off processing
    ######################################################################
    def take_off_proc(self):
        pgui.moveTo(100, 100)
        distance = 200
        pgui.dragRel(distance, 0, duration=0.5)     # →
        #pgui.dragRel(0, distance, duration=0.5)     # ↓
        #pgui.dragRel(-distance, 0, duration=0.5)    # ←
        #pgui.dragRel(0, -distance, duration=0.5)    # ↑
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Active console processing -----
    ######################################################################
    ## @brief      Active console processing
    ######################################################################
    def active_console_proc(self):
        pgui.moveTo(2000, 1000)
        pgui.click()
    #_____________________________________________________________________


    def main_proc(self):

        #Ctrl+cが押されるまでループ
        try:
            while True:
                if ms.kbhit():     # 何かキーが押されるのを待つ
                    key = ms.getch()   # 1文字取得

                    # キーに応じた処理
                    if key == b't':      # 離陸
                        print('離陸')
                        self.take_off_proc()
                        self.active_console_proc()
                    if key == b'l':    # 着陸
                        print('着陸')
                    if key == b'w':    # 前進
                        print('前進')
                    if key == b's':    # 後進
                        print('後進')
                    if key == b'a':    # 左移動
                        print('左移動')
                    if key == b'd':    # 右移動
                        print('右移動')
                    if key == b'q':    # 左旋回
                        print('左旋回')
                    if key == b'e':    # 右旋回
                        print('右旋回')
                    if key == b'r':    # 上昇
                        print('上昇')
                    if key == b'f':    # 下降
                        print('下降')

                    #print("test")
                    #print(key)

                time.sleep(0.3) # 適度にウェイトを入れてCPU負荷を下げる

        except( KeyboardInterrupt, SystemExit):    # Ctrl+cが押されたら離脱
            print( "SIGINTを検知" )

#_____________________________________________________________________


#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Main processing -----
######################################################################
## @brief      Main processing
## @callgraph
## @callergraph
######################################################################
def main_proc():

    cd_utility = control_drone_utility()

    #cd_utility.take_off_proc()
    cd_utility.main_proc()


if __name__ == '__main__':
    main_proc()
