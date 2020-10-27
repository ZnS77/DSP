
def endPointDetect(data) :
    sum = 0
    energyAverage = 0
    for en in data.En[0] :
        sum = sum + en
    energyAverage = sum / len(data.En[0])

    sum = 0
    for en in data.En[0][:5] :
        sum = sum + en
    ML = sum / 5
    MH = energyAverage / 4              #较高的能量阈值
    ML = (ML + MH) / 4    #较低的能量阈值
    sum = 0
    for zcr in data.Zt :
        sum = float(sum) + zcr
    Zs = sum / len(data.Zt)                    #过零率阈值
    print(Zs)

    A = []
    B = []
    C = []

    # 首先利用较大能量阈值 MH 进行初步检测
    flag = 0
    for i in range(len(data.En[0])):
        if len(A) == 0 and flag == 0 and data.En[0][i] > MH :
            A.append(i)
            flag = 1
        elif flag == 0 and data.En[0][i] > MH and i - 21 > A[len(A) - 1]:
            A.append(i)
            flag = 1
        elif flag == 0 and data.En[0][i] > MH and i - 21 <= A[len(A) - 1]:
            A = A[:len(A) - 1]
            flag = 1

        if flag == 1 and data.En[0][i] < MH :
            A.append(i)
            flag = 0
        elif flag == 1 and i ==  len(data.En[0])-1:
            A.append(i)
            flag = 0

    # 取长的一段为主值
    length = []
    print(A)
    for i in range(len(A)//2):
        length.append(A[2*i+1]-A[2*i])
    Al =[]
    print(length)
    index = length.index(max(length))
    Al.append(A[2*index])
    Al.append(A[2 * index + 1])


    print("较高能量阈值，计算后的浊音A:" + str(Al))

    # 利用较小能量阈值 ML 进行第二步能量检测
    for j in range(len(Al)) :
        i = Al[j]
        if j % 2 == 1 :
            while i < len(data.En[0]) and data.En[0][i] > ML :
                i = i + 1
            B.append(i)
        else :
            while i > 0 and data.En[0][i] > ML :
                i = i - 1
            B.append(i)
    print("较低能量阈值，增加一段语言B:" + str(B))

    # 利用过零率进行最后一步检测
    for j in range(len(B)) :
        i = B[j]
        if j % 2 == 1 :
            while i < len(data.Zt) and data.Zt[i] >= Zs :
                i = i + 1
            C.append(i)
        else :
            while i > 0 and data.Zt[i] >= Zs :
                i = i - 1
            C.append(i)
    print("过零率阈值，最终语音分段C:" + str(C))
    return C
