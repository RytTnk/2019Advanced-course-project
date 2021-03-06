#! /usr/bin/env python
# -*- coding: utf-8 -*-

#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Include library -----
import rospy
from std_msgs.msg import String

import cv2
import numpy as np
import os
#_____________________________________________________________________


#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Utility of smile camera library -----
######################################################################
## @version    0.1.0
## @author     K.Ishimori
## @date       2019/10/23 Newly created.                  [K.Ishimori]
## @brief      Utility of smile camera library
######################################################################
class smile_camera_utility:
    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Initialized utility class -----
    ######################################################################
    ## @brief      Initialized utility class
    ######################################################################
    def __init__(self):
        rospy.init_node('smile_camera_node', anonymous=True)
        self.pub = rospy.Publisher('/camera/smile_intensity', String, queue_size=10)

        self.capture = cv2.VideoCapture(0)
        self.capture.set(3,320)  # 320 320 640 720　横の長さ
        self.capture.set(4,240)  # 180 240 360 405　縦の長さ
        ret, self.img = self.capture.read()

        cwd_path = os.path.dirname(os.path.abspath(__file__))
        self.face_cascade  = cv2.CascadeClassifier(cwd_path+'/haarcascade_frontalface_default.xml')
        self.smile_cascade = cv2.CascadeClassifier(cwd_path+'/haarcascade_smile.xml')

        self.smile_intensity = 0
        self.pub.publish(self.smile_intensity)
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Capture from camera processing -----
    ######################################################################
    ## @brief      Capture from camera processing
    ######################################################################
    def camera_capture_proc(self):
        ret, self.img = self.capture.read()
        self.img = cv2.flip(self.img, 1)   #鏡表示にするため．
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Print image processing -----
    ######################################################################
    ## @brief      Print image processing
    ######################################################################
    def print_img_proc(self):
        cv2.imshow('img',self.img)
        cv2.waitKey(10)


    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Camera operation check processing -----
    ######################################################################
    ## @brief      Camera operation check processing
    ######################################################################
    def camera_check_proc(self):
        self.camera_capture_proc()
        self.print_img_proc()
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Face detect check processing -----
    ######################################################################
    ## @brief      Face detect check processing
    ######################################################################
    def face_detect_check_proc(self):
        self.camera_capture_proc()

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)

        for (x,y,w,h) in faces:
            cv2.circle(self.img,(int(x+w/2),int(y+h/2)),int(w/2),(0, 0, 255),2) # red

        self.print_img_proc()
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Smile detect check processing -----
    ######################################################################
    ## @brief      Smile detect check processing
    ######################################################################
    def smile_detect_check_proc(self):
        self.camera_capture_proc()

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)
        for (x,y,w,h) in faces:
            cv2.circle(self.img,(int(x+w/2),int(y+h/2)),int(w/2),(255, 0, 0),2) # blue

            roi_gray = gray[y:y+h, x:x+w] # Gray画像から，顔領域を切り出す．
            smiles= self.smile_cascade.detectMultiScale(roi_gray,scaleFactor= 1.2, minNeighbors=10, minSize=(20, 20)) # 笑顔識別
            if len(smiles) > 0:
                for(sx,sy,sw,sh) in smiles:
                    cv2.circle(self.img,(int(x+sx+sw/2),int(y+sy+sh/2)),int(sw/2),(0, 0, 255),2) # red

        self.print_img_proc()
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Smile intensity check processing -----
    ######################################################################
    ## @brief      Smile intensity check processing
    ######################################################################
    def smile_intensity_check_proc(self):

        self.camera_capture_proc()
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(100,100))
        for (x,y,w,h) in faces:
            cv2.rectangle(self.img,(x,y),(x+w,y+h),(255, 0, 0),2) # blue
            # Gray画像から，顔領域を切り出す．
            roi_gray = gray[y:y+h, x:x+w]

            # サイズを縮小
            roi_gray = cv2.resize(roi_gray,(100,100))
            #cv2.imshow("roi_gray",roi_gray) # 確認のためサイズ統一させた画像を表示

            # 輝度で規格化
            lmin = roi_gray.min() # 輝度の最小値
            lmax = roi_gray.max() # 輝度の最大値
            for index1, item1 in enumerate(roi_gray):
                 for index2, item2 in enumerate(item1) :
                     roi_gray[index1][index2] = int(float(item2 - lmin)/float(lmax-lmin) * item2)
            #cv2.imshow("roi_gray2",roi_gray)  # 確認のため輝度を正規化した画像を表示

            smiles= self.smile_cascade.detectMultiScale(roi_gray,scaleFactor= 1.1, minNeighbors=0, minSize=(20, 20)) # 笑顔識別
            if len(smiles) > 0: # 笑顔領域がなければ以下の処理を飛ばす．#if len(smiles) <=0 : continue でもよい．その場合以下はインデント不要
                # サイズを考慮した笑顔認識
                smile_neighbors = len(smiles)
                #print("smile_neighbors=",smile_neighbors) #確認のため認識した近傍矩形数を出力
                LV = float(2)/100
                intensityZeroOne = smile_neighbors  * LV
                if intensityZeroOne > 1.0: intensityZeroOne = 1.0
                #確認のため強度を出力
                smile_intensity = int(float(intensityZeroOne) * 100)
                #print "笑顔度：", str(smile_intensity).rjust(3), "%"
                self.pub.publish(str(smile_intensity).rjust(3))
                for(sx,sy,sw,sh) in smiles:
                    cv2.circle(self.img,(int(x+(sx+sw/2)*w/100),int(y+(sy+sh/2)*h/100)),int(sw/2*w/100), (255*(1.0-intensityZeroOne), 0, 255*intensityZeroOne),2)#red

        self.print_img_proc()
    #_____________________________________________________________________

#_____________________________________________________________________


#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Main processing -----
######################################################################
## @brief      Main processing
## @callgraph
## @callergraph
######################################################################
if __name__ == '__main__':
    try:
        sc_utility = smile_camera_utility()
        while not rospy.is_shutdown():
            # Camera operation check processing
            #sc_utility.camera_check_proc()

            # Face detect check processing
            #sc_utility.face_detect_check_proc()

            # Smile detect check processing
            #sc_utility.smile_detect_check_proc()

            # Smile intensity check processin
            sc_utility.smile_intensity_check_proc()

    except rospy.ROSInterruptException:
        pass
