import process as p
import os
import edit

# def writeTXT(data,txt_path):
#
#

def main():

    txt_path="feature/"
    wav_path="origin_data/zty/"

    files = os.listdir(wav_path)
    cnt = 0
    for file in files:
        print(file)
        print(str(cnt)+"/"+str(len(files)))
        cnt = cnt + 1

        d = p.wavDATA()
        p.read(wav_path+file, d)
        p.process(d, 25, 10)
        p.calculate(d, "square")
        p.MeanFilter(d, 40)

        # 取特征向量前将原本88064数据除10
        data10=[]
        for i in range(d.nframes//10):
            data10.append(d.y[0][10*i])

        print(d.y)

        c = p.edit.endPointDetect(d)

        with open(txt_path+file[:-4]+".txt","w") as f:
            for i in range(len(data10)):
                if (i < d.mlist[c[0]-1]/10):
                    f.write("0 ")
                elif (i > d.mlist[c[1]-1]/10):
                    f.write("0 ")
                else:
                    f.write(str(data10[i])+" ")


if __name__ == '__main__':
    main()