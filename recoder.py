import pyaudio
import wave
import numpy as np
import os
# init

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2

USERNAME="lyq"
DATAPATH="./origin_data/"
def mkdir(dir_name=USERNAME,datapath=DATAPATH):
    path = datapath + dir_name # path of dir
    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        print(path + ' created successfully!')
    else:
        print(path + ' is existed!')

mkdir(USERNAME,DATAPATH)

print("请在看见 *recording 后发音")
for m in range(20):
    for n in range(10):
        WAVE_OUTPUT_FILENAME = USERNAME+"_"+str(n)+"_"+str(m)+".wav"
        print("第"+str(m)+"组：")
        print("请按enter，说"+str(n))
        x=input()

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(DATAPATH+"/"+USERNAME+"/"+WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

print("* completed")



