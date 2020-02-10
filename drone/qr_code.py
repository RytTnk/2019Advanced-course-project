# coding: utf-8
import os, qrcode				# ライブラリ読み込み
from PIL import Image

def qr_and_photo_show(url, photo_file):

    create_qrcode(url)
    # im1: QRコード(笑顔度最高)、 im2: 笑顔度最高写真
    im1 = Image.open('qr_code.png')
    im2 = Image.open(photo_file)
#    get_concat_h_blank(im1, im2, color=(0, 0, 0))
#    get_concat_h_blank(im1, im2).save('pillow_concat_h_blank.jpg')
    get_concat_h_blank(im1, im2).show()


def create_qrcode(url):
    file_name = "qr_code.png"		#保存するQRコードのファイル名
    #print("QRコードに変換したい文字列を入力してください: ")
    qr_string = url				# キーボードから変換したい文字列を入力させる
    img = qrcode.make(qr_string)		# QRコード画像データ生成
    img.save(file_name)				# 画像ファイルとして保存
    current_dir = os.getcwd()			# 現在のディレクトリ位置を取得
    print("「{0}\\{1}」にQRコード画像を保存しました".format(current_dir, file_name))	# 終了メッセージ出力
#    img.show()

# color 余白の色

# 横に2個並べる
def get_concat_h_blank(im1, im2, color=(0, 0, 0)):
    dst = Image.new('RGB', (im1.width + im2.width, max(im1.height, im2.height)), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst