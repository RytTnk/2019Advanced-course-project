# coding: utf-8
import os, qrcode				# ライブラリ読み込み

def create_qrcode(url):
    file_name = "qr_code.png"		#保存するQRコードのファイル名
    #print("QRコードに変換したい文字列を入力してください: ")
    qr_string = url				# キーボードから変換したい文字列を入力させる
    img = qrcode.make(qr_string)		# QRコード画像データ生成
    img.save(file_name)				# 画像ファイルとして保存
    current_dir = os.getcwd()			# 現在のディレクトリ位置を取得
    print("「{0}\\{1}」にQRコード画像を保存しました".format(current_dir, file_name))	# 終了メッセージ出力
    img.show()
