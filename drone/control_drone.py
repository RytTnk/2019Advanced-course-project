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
        self.rb_dist = 50
        self.rb_sleep = 0.5

        self.mark_flg = False
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Click button of take on/off -----
    ######################################################################
    ## @brief      Click button of take on/off
    ######################################################################
    def click_btn_take_on_off(self):
        pgui.moveTo(  67, 354)    # Button of take off position
        pgui.click()
        time.sleep(0.5)
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Accept button of take off -----
    ######################################################################
    ## @brief      Accept button of take off
    ######################################################################
    def accept_btn_take_off(self):
        pgui.moveTo( 882, 646)    # Accept button of take off position
        distance = 600
        pgui.dragRel(distance, 0, duration=0.5)     # →
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Accept button of take on -----
    ######################################################################
    ## @brief      Accept button of take on
    ######################################################################
    def accept_btn_take_on(self):
        pgui.moveTo( 1325, 783)    # Accept button of take on position
        pgui.click()
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Cntrol button of right -----
    ######################################################################
    ## @brief      Control button of right
    ######################################################################
    def ctrl_btn_right(self, case):
        x = 2052
        y = 970

        if case == 'Move':
            pgui.moveTo(x, y)
        elif case == 'MDown':
            pgui.mouseDown(x, y, button='left')
        elif case == 'MUp':
            pgui.mouseUp(x, y, button='left')
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Take off processing -----
    ######################################################################
    ## @brief      Take off processing
    ######################################################################
    def take_off_proc(self):
        self.click_btn_take_on_off()
        self.accept_btn_take_off()
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Take on processing -----
    ######################################################################
    ## @brief      Take on processing
    ######################################################################
    def take_on_proc(self):
        self.click_btn_take_on_off()
        self.accept_btn_take_on()
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Go ahead processing -----
    ######################################################################
    ## @brief      Go ahead processing
    ######################################################################
    def go_ahead_proc(self):
        distance = self.rb_dist

        self.ctrl_btn_right('Move')
        self.ctrl_btn_right('MDown')
        pgui.moveRel(0, -distance, 0)   # ↑
        time.sleep(self.rb_sleep)
        self.ctrl_btn_right('MUp')
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Go back processing -----
    ######################################################################
    ## @brief      Go back processing
    ######################################################################
    def go_back_proc(self):
        distance = self.rb_dist

        self.ctrl_btn_right('Move')
        self.ctrl_btn_right('MDown')
        pgui.moveRel(0,  distance, 0)   # ↓
        time.sleep(self.rb_sleep)
        self.ctrl_btn_right('MUp')
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Go right processing -----
    ######################################################################
    ## @brief      Go right processing
    ######################################################################
    def go_right_proc(self):
        distance = self.rb_dist

        self.ctrl_btn_right('Move')
        self.ctrl_btn_right('MDown')
        pgui.moveRel( distance, 0, 0)   # →
        time.sleep(self.rb_sleep)
        self.ctrl_btn_right('MUp')
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Go left processing -----
    ######################################################################
    ## @brief      Go left processing
    ######################################################################
    def go_left_proc(self):
        distance = self.rb_dist

        self.ctrl_btn_right('Move')
        self.ctrl_btn_right('MDown')
        pgui.moveRel(-distance, 0, 0)   # ←
        time.sleep(self.rb_sleep)
        self.ctrl_btn_right('MUp')
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Active console processing -----
    ######################################################################
    ## @brief      Active console processing
    ######################################################################
    def active_console_proc(self):
        pgui.moveTo(2000, 1200)
        pgui.click()
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Debug mouse position processing -----
    ######################################################################
    ## @brief      Debug mouse position processing
    ######################################################################
    def debug_pos_proc(self):
        while 1:
            px,py = pgui.position()
            print(px, py)
    #_____________________________________________________________________

    def main_proc(self):

        #Ctrl+cが押されるまでループ
        try:
            while True:
                if ms.kbhit():     # 何かキーが押されるのを待つ
                    key = ms.getch()   # 1文字取得

                    if self.mark_flg == False:
                        # キーに応じた処理
                        if key == b't':      # 離陸
                            print('離陸')
                            self.take_off_proc()
                            self.active_console_proc()
                        if key == b'l':    # 着陸
                            print('着陸')
                            self.take_on_proc()
                            self.active_console_proc()
                        if key == b'w':    # 前進
                            print('前進')
                            self.go_ahead_proc()
                            self.active_console_proc()
                        if key == b's':    # 後進
                            print('後進')
                            self.go_back_proc()
                            self.active_console_proc()
                        if key == b'a':    # 左移動
                            print('左移動')
                            self.go_left_proc()
                            self.active_console_proc()
                        if key == b'd':    # 右移動
                            print('右移動')
                            self.go_right_proc()
                            self.active_console_proc()
                        if key == b'q':    # 左旋回
                            print('左旋回')
                        if key == b'e':    # 右旋回
                            print('右旋回')
                        if key == b'r':    # 上昇
                            print('上昇')
                        if key == b'f':    # 下降
                            print('下降')
                    else:
                        self.mark_flg = False
                        if key == b'H':    # 前進
                            print('前進')
                            self.go_ahead_proc()
                            self.active_console_proc()
                        if key == b'P':    # 後進
                            print('後進')
                            self.go_back_proc()
                            self.active_console_proc()
                        if key == b'K':    # 左移動
                            print('左移動')
                            self.go_left_proc()
                            self.active_console_proc()
                        if key == b'M':    # 右移動
                            print('右移動')
                            self.go_right_proc()
                            self.active_console_proc()

                    if key == b'\xe0':
                        self.mark_flg = True

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
    #cd_utility.go_ahead_proc()

    cd_utility.main_proc()

    #cd_utility.debug_pos_proc()


if __name__ == '__main__':
    main_proc()
