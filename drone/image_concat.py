# -*- coding: utf-8 -*-

#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Include library -----
from PIL import Image

#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- test for picture file concatenation with pillow -----
######################################################################
## @version    0.0.1
## @author     K.Kosaka
## @date       2020/01/25 Newly created.                  [K.Kosaka]
## @brief      test for picture file concatenation with pillow
## https://note.nkmk.me/python-pillow-concat-images/
######################################################################

# テスト用サンプルファイル
# im1: QRコード(笑顔度最高)、 im2: 笑顔度最高写真、 im3: 笑顔度(保存ファイル内)最低写真
im1 = Image.open('qr_code.png')
im2 = Image.open('20200119095652/066_20200119095704.png')
im3 = Image.open('20200119095652/030_20200119095657.png')

# color 余白の色

# 横に2個並べる
def get_concat_h_blank(im1, im2, color=(0, 0, 0)):
    dst = Image.new('RGB', (im1.width + im2.width, max(im1.height, im2.height)), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

# 縦に2個並べる
def get_concat_v_blank(im1, im2, color=(0, 0, 0)):
    dst = Image.new('RGB', (max(im1.width, im2.width), im1.height + im2.height), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

# 2x2で計4個の写真を並べる
def get_concat_sq_blank(im1, im2, im3, im4, color=(0, 0, 0)):
    width_concat0 = max(im1.width, im3.width)
    width_concat1 = max(im2.width, im4.width)
    height_concat0 = max(im1.height, im2.height)
    height_concat1 = max(im3.height, im4.height)
    
    dst = Image.new('RGB', ((width_concat0 + width_concat1), (height_concat0 + height_concat1)), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (width_concat0, 0))
    dst.paste(im3, (0, height_concat0))
    dst.paste(im4, (width_concat0, height_concat0))
    return dst

# get_concat_h_blank(im1, im2).save('pillow_concat_h_blank.jpg')
# get_concat_v_blank(im1, im2, (0, 64, 128)).save('pillow_concat_v_blank.jpg')
get_concat_sq_blank(im1, im2, im1, im3, (255, 255, 255)).save('pillow_concat_sq_blank.jpg')
