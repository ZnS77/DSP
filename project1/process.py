# -*- coding: utf-8 -*-
import wave
import pylab as pl
import numpy as np
import math
import sys
import time as t
import edit

pi = 3.1415926536
set_channel = 1 # 即使是双声道也只采样单声道数据 

def sgn(num):
    return 1 if (num >= 0) else 0

class wavDATA(object):
    def __init__(self):
        self.y=[[] for i in range(2)]
        self.t=[]
        self.nchannels = 0
        self.sampwidth = 0 # The byte width of each frame
        self.framerate = 0
        self.nframes = 0

        self.n_fl = 0 # frame length
        self.n_fs = 0 # frame shift
        self.flist = [0] # 分帧后开始帧序列
        self.mlist = [] # 分帧后帧中点序列（取每帧正中间点，最后一帧直接取max（尾值，中值））

        self.En = [[],[]]
        self.Mn = [[],[]]
        self.Zn = [[],[]]

        # 滤波结果
        self.yt=[]
        self.Zt=[]

        self.clist = []


    def addconf(self,nc,sw,fr,nf):
        self.nchannels = nc
        self.sampwidth = sw  # The byte width of each frame
        self.framerate = fr
        self.nframes = nf

def paintwave(data):
    # 绘制声波波形

    for i in range(data.nchannels):
        pl.subplot(data.nchannels,1,i+1)
        pl.plot(data.t, data.y[i])
        pl.ylabel("Y"+str(i))

    pl.xlabel("time (seconds)")
    pl.show()

def paint(data):
    # 绘制
    pl.subplot(221)
    pl.plot(data.t, data.y[0])
    pl.plot(data.t, data.yt, c="k")
    pl.plot(data.t, data.clist, c="r")
    pl.ylabel("Y1")
    pl.subplot(222)
    pl.plot(np.array(data.flist)/data.nframes, data.En[0], c="b")
    pl.ylabel("En1")
    pl.subplot(223)
    pl.plot(np.array(data.flist)/data.nframes, data.Mn[0], c="r")
    pl.ylabel("Mn1")
    pl.subplot(224)
    pl.plot(np.array(data.flist)*2/data.nframes, data.Zn[0], c="g")
    pl.plot(np.array(data.flist)*2/data.nframes, data.Zt, c="k")
    pl.ylabel("Zn1")
    # pl.xlabel("time (seconds)")
    pl.show()

def read(filename,data):
    f = wave.open(filename,"rb")
    # (nchannels, sampwidth, framerate, nframes, comptype, compname)
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    # 读取波形数据
    str_data = f.readframes(nframes)
    f.close()

    wave_data = np.frombuffer(str_data, dtype=np.short)
    wave_data.shape = -1, nchannels
    wave_data = wave_data.T

    time = np.arange(0, nframes) * (1.0 / framerate)

    data.addconf(nchannels, sampwidth, framerate, nframes)
    for i in range(nchannels):
        data.y[i] = wave_data[i]

    data.t = time

# 分帧
def process(data,FL,FS):
    framerate = data.framerate
    nframes = data.nframes
    n_fl = int(FL /1000 * framerate)
    n_fs = int(FS /1000 * framerate)
    data.n_fl = n_fl
    data.n_fs = n_fs

    n=0
    while (n<nframes-n_fl):
        n = n + (n_fl - n_fs)
        data.flist.append(n)
    for fl in data.flist[:-1]:
        data.mlist.append(fl+int(n_fl/2))
    data.mlist.append(min(data.flist[-1]+int(n_fl/2),nframes))


def chuang(n,N,method):
    # 窗函数
    if method == "square":
        return 1
    elif method == "hamming":
        # print("n="+str(n))
        # print("N="+str(N))
        return (0.54 - 0.46 * math.cos(2 * pi * n / (N - 1)))

    elif method == "hanning":
        return (0.5 * (1 - math.cos(2 * pi * n / (N - 1))))
    else:
        print("Method set wrong!")
        sys.exit(0)

# def square(data)
#     for i in range(2):
#         # En
#         for fl in data.flist[:-1]:
#             E = 0
#             for m in range(fl,fl+data.n_fl):
#                 E = E + int(data.y[i][m]) * int(data.y[i][m])
#             data.En[i].append(E)
#         E = 0
#         for m in range(data.flist[-1],data.nframes):
#             E = E + int(data.y[i][m]) * int(data.y[i][m])
#         data.En[i].append(E)
#
#         # Mn
#         for fl in data.flist[:-1]:
#             M = 0
#             for m in range(fl,fl+data.n_fl):
#                 M = M + abs(data.y[i][m])
#             data.Mn[i].append(M)
#         M = 0
#         for m in range(data.flist[-1],data.nframes):
#             M = M + abs(data.y[i][m])
#         data.Mn[i].append(M)
#
#         # Zn #引用函数
#         # for fl in data.flist[:-1]:
#         #     Z = 0
#         #     for m in range(fl,fl+data.n_fl-1):
#         #         Z = Z + abs(sgn(data.y[i][m])-sgn(data.y[i][m-1]))/2 # 调用好慢
#         #         # tmp = (data.y[i][m-1]>=0) #更慢
#         #         # Z = (Z + 1) if ((tmp and (data.y[i][m]<0)) or ((not tmp) and (data.y[i][m]>=0))) else 0
#         #     data.Zn[i].append(Z)
#         # Z=0
#         # for m in range(data.flist[-1],data.nframes-1):
#         #     Z = Z + abs(sgn(data.y[i][m])-sgn(data.y[i][m-1]))/2
#         # data.Zn[i].append(Z)
#
#         # Zn #标志位数组异或
#         sign = []
#         for fl in data.flist[:-1]:
#             Z = 0
#             sign.append(sgn(data.y[i][0]))
#             for m in range(fl,fl+data.n_fl-1):
#                 sign.append(sgn(data.y[i][m+1]))
#                 Z = Z + (sign[m]^sign[m+1])
#             data.Zn[i].append(Z)
#         Z=0
#         for m in range(data.flist[-1],data.nframes-1):
#             sign.append(sgn(data.y[i][m + 1]))
#             Z = Z + (sign[m]^sign[m + 1])
#         data.Zn[i].append(Z)

def calculate(data, method):
    # 分窗计算

    # 原计算两声道
    # for i in range(data.nchannels):
    # 锁定单声道
    for i in range(set_channel):
        # En
        for fl in data.flist[:-1]:
            E = 0
            for m in range(fl,fl+data.n_fl):
                tmp = int(chuang(m - fl, data.n_fl, method) * data.y[i][m])
                E = E + tmp * tmp
            data.En[i].append(E)
        E = 0
        for m in range(data.flist[-1],data.nframes):
            tmp = int(chuang(m - data.flist[-1], data.nframes - data.flist[-1], method) * data.y[i][m])
            E = E + tmp * tmp
        data.En[i].append(E)

        # Mn
        for fl in data.flist[:-1]:
            M = 0
            for m in range(fl,fl+data.n_fl):
                M = M + chuang(m - fl,data.n_fl, method) * abs(data.y[i][m])
            data.Mn[i].append(M)
        M = 0
        for m in range(data.flist[-1],data.nframes):
            M = M + chuang(m - data.flist[-1], data.nframes - data.flist[-1], method) * abs(data.y[i][m])
        data.Mn[i].append(M)
        # Zn
        # 汉明窗与海宁窗的Zn和矩形框一致（>0变换）
        # for fl in data.flist[:-1]:
        #     Z = 0
        #     sign = []
        #     sign.append(sgn(data.y[i][fl]))
        #     for m in range(fl,fl+data.n_fl-1):
        #         sign.append(sgn(data.y[i][m+1]))
        #         Z = Z + (sign[m-fl]^sign[m-fl+1])
        #     data.Zn[i].append(Z)
        # Z=0
        # sign = []
        # sign.append(sgn(data.y[i][data.flist[-1]]))
        # for m in range(data.flist[-1],data.nframes-1):
        #     sign.append(sgn(data.y[i][m + 1]))
        #     Z = Z + (sign[m-data.flist[-1]]^sign[m - data.flist[-1] + 1])
        # data.Zn[i].append(Z)

        # Zn #引用函数版本
        for fl in data.flist[:-1]:
            Z = 0
            for m in range(fl,fl+data.n_fl-1):
                Z = Z + (sgn(data.y[i][m])^sgn(data.y[i][m+1])) # 调用好慢
                # tmp = (data.y[i][m-1]>=0) #更慢
                # Z = (Z + 1) if ((tmp and (data.y[i][m]<0)) or ((not tmp) and (data.y[i][m]>=0))) else 0
            data.Zn[i].append(Z)
        Z=0
        for m in range(data.flist[-1],data.nframes-1):
            Z = Z + (sgn(data.y[i][m])^sgn(data.y[i][m+1]))
        data.Zn[i].append(Z)

def MeanFilter(data,length):
    # 均值滤波器
    # 前length/2帧
    len2 = int(length/2)
    for i in range(len2):
        tmp = 0
        for j in range(i+1):
            tmp = tmp + int((1/(i+1))*data.y[0][j])
        data.yt.append(tmp)

    for i in range(len2,data.nframes-len2):
        tmp = 0
        for j in range(i-len2,i+len2):
            tmp = tmp + int((1/(length))*data.y[0][j])
        data.yt.append(tmp)
    for i in range(data.nframes-len2,data.nframes):
        tmp = 0
        for j in range(i,i + 1):
            tmp = tmp + int((1 / (data.nframes - i)) * data.y[0][j])
        data.yt.append(tmp)

    # 均值后短时过零率Zt
    for fl in data.flist[:-1]:
        Z = 0
        for m in range(fl, fl + data.n_fl - 1):
            Z = Z + (sgn(data.yt[m]) ^ sgn(data.yt[m + 1]))  # 调用好慢
            # tmp = (data.y[i][m-1]>=0) #更慢
            # Z = (Z + 1) if ((tmp and (data.y[i][m]<0)) or ((not tmp) and (data.y[i][m]>=0))) else 0
        data.Zt.append(Z)
    Z = 0
    for m in range(data.flist[-1], data.nframes - 1):
        Z = Z + (sgn(data.yt[m]) ^ sgn(data.yt[m + 1]))
    data.Zt.append(Z)

def main():
    d = wavDATA()
    read("origin_data/zty_uesd/zty_0_2.wav", d)

    process(d, 25, 10)

    print(d.nchannels, d.sampwidth, d.framerate, d.nframes)
    calculate(d,"square")
    bt = t.time()
    MeanFilter(d, 40)
    print(len(d.yt))
    print(len(d.Zt))
    print(len(d.Zn[0]))
    et = t.time()
    print("time=" + str(et-bt) )
    # print(d.nframes)
    # print(d.flist)
    # print(d.mlist)
    # print(d.y[0])
    # # print(d.En)
    # # print(d.Mn)
    # print(d.Zn[0])
    c=edit.endPointDetect(d)

    for i in range(d.nframes):
        if(i<d.mlist[c[0]]):
            d.clist.append(0)
        elif (i > d.mlist[c[1]]):
            d.clist.append(0)
        else:
            d.clist.append(1000)



    paint(d)


    # print(out[1])
    # print(d[1])
    # print(d[2])
    # print(d)


if __name__ == '__main__':
    main()


