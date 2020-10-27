import os
import re

# 因为命名不规范而写的函数 支持转换 n(m) -> name_n_m
def file_rename(filepath,username,file):

    # 将除数字字母字符转换为空格分割，存入列表
    name = re.sub('[^0-9a-zA-Z]',' ',file)
    name = re.split(' +',name)

    filetype = os.path.splitext(file)[1]  # 文件扩展名

    print(name)
    olddir = os.path.join(filepath,file)
    newdir = filepath + "/" + username +"_" + name[0] + "_" + name[1] + filetype
    os.rename(olddir,newdir)

def main():
    path = "origin_data/zty"
    files = os.listdir(path)
    print(files)
    for file in files:
        print(file)
        file_rename(path,"zty",file)


if __name__ == '__main__':
    main()