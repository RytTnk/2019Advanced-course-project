#-*- cording: utf-8 -*-

#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Include library -----
import numpy as np
import wave     #wavファイルを扱うためのライブラリ
import pyaudio
import matplotlib.pyplot as plt
#_____________________________________________________________________

#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Utility of control wavefile library -----
######################################################################
## @version    0.1.0
## @author     K.Ishimori
## @date       2020/01/31 Newly created.                  [K.Ishimori]
## @brief      Utility of wavefile library
######################################################################
class control_wavefile_utility:
    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Make wave file processing -----
    ######################################################################
    ## @brief      Make wave file processing
    ######################################################################
    def MakeWavFile(self, FileName = "sample.wav", Record_Seconds = 2, save = True):
        """
        録音して、波形表示
        """
        chunk = 1024
        FORMAT = pyaudio.paInt16

        CHANNELS = 1 #モノラル
        RATE = 44100 #サンプルレート（録音の音質）

        p = pyaudio.PyAudio()

        stream = p.open(format = FORMAT,
                        channels = CHANNELS,
                        rate = RATE,
                        input = True,
                        frames_per_buffer = chunk)

        #レコード開始
        print("Now Recording...")
        all = []
        for i in range(0, int(RATE / chunk * Record_Seconds)):
            data = stream.read(chunk) #音声を読み取って、
            all.append(data) #データを追加

        #レコード終了
        print("Finished Recording.")

        stream.close()
        p.terminate()

        #録音したデータを配列に変換
        #data = ''.join(all) #Python2用
        data = b"".join(all) #Python3用
        result = np.frombuffer(data,dtype="int16") / float(2**15)
        plt.plot(result)
        plt.show()

        if(save): #保存するか？
            wavFile = wave.open(FileName, 'wb')
            wavFile.setnchannels(CHANNELS)
            wavFile.setsampwidth(p.get_sample_size(FORMAT))
            wavFile.setframerate(RATE)
            #wavFile.writeframes(b''.join(all)) #Python2 用
            wavFile.writeframes(b"".join(all)) #Python3用
            wavFile.close()
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Read wave file processing -----
    ######################################################################
    ## @brief      Read wave file processing
    ######################################################################
    def ReadWavFile(self, FileName = "sample.wav"):
        """
        wavファイルを読み込み、波形表示＆高速降りえ変換（FFT）
        """
        try:
            wr = wave.open(FileName, "r")
        except FileNotFoundError: #ファイルが存在しなかった場合
            print("[Error 404] No such file or directory: " + FileName)
            return 0
        data = wr.readframes(wr.getnframes())
        wr.close()
        x = np.frombuffer(data, dtype="int16") / float(2**15)

        plt.figure(figsize=(15,3))
        plt.plot(x)
        plt.show()

        x = np.fft.fft(np.frombuffer(data, dtype="int16"))
        plt.figure(figsize=(15,3))
        plt.plot(x.real[:int(len(x)/2)])
        plt.show()
    #_____________________________________________________________________

    #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
    # ----- Play wave file processing -----
    ######################################################################
    ## @brief      Play wave file processing
    ######################################################################
    def PlayWavFie(self, Filename = "sample.wav"):
        """
        wavファイルを再生
        """
        try:
            wf = wave.open(Filename, "r")
        except FileNotFoundError: #ファイルが存在しなかった場合
            print("[Error 404] No such file or directory: " + Filename)
            return 0

        # ストリームを開く
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # チャンク単位でストリームに出力し音声を再生
        chunk = 1024
        data = wf.readframes(chunk)
        while data != b'':
            stream.write(data)
            data = wf.readframes(chunk)
        stream.close()
        p.terminate()
    #_____________________________________________________________________


#_____________________________________________________________________

#‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- Main processing -----
######################################################################
## @brief      Main processing
## @callgraph
## @callergraph
######################################################################
def main_proc():
    cw_utility = control_wavefile_utility()
    #WAVファイル作成, 引数は（ファイル名, 録音する秒数）
    #cw_utility.MakeWavFile("sample.wav", Record_Seconds = 2)
    #cw_utility.ReadWavFile("sample.wav")
    #cw_utility.PlayWavFie("sample2.wav")

    file_dir = 'wavefile'
    #cw_utility.PlayWavFie(file_dir+"\\01_start.wav")
    cw_utility.PlayWavFie(file_dir+"\\02_mid.wav")
    #cw_utility.PlayWavFie(file_dir+"\\03_end.wav")
    #cw_utility.PlayWavFie(file_dir+"\\04_class_a.wav")
    #cw_utility.PlayWavFie(file_dir+"\\04_class_b.wav")
    #cw_utility.PlayWavFie(file_dir+"\\04_class_c.wav")
#_____________________________________________________________________

if __name__ == '__main__':
    main_proc()
