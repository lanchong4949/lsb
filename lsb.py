# __*__ encoding: utf-8 __*__
import sys
import PIL.Image
import os


def plus(string):
    return string.zfill(8)  # 用0左填充至8位（方便解码）


# 获取图片的RGB的二进制字符串
def git_bimg(img):
    brgb = ''
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            rgb = img.getpixel((i, j))
            brgb = brgb + plus(bin(rgb[0]).replace('0b', ''))  # 将RGB的R值转为01二进制字符串，并将0b用空字符替换
            brgb = brgb + plus(bin(rgb[1]).replace('0b', ''))  # 将RGB的G值转为01二进制字符串，并将0b用空字符替换
            brgb = brgb + plus(bin(rgb[2]).replace('0b', ''))  # 将RGB的B值转为01二进制字符串，并将0b用空字符替换
    return brgb


# 获取要隐写的文件的二进制字符串
def git_text(text):
    with open(text, 'rb') as f:
        data = f.read()
    text = ''
    for i in data:
        text = text + plus(bin(i).replace('0b', ''))  # 将文件转换为01二进制字符串，并将0b用空字符替换
    return text


# 将要隐写的文件的二进制字符串替换掉图片的RGB最低位
def git_string(imgb, textb):
    count = 1
    imgblist = list(imgb)
    for i in textb:
        imgblist[count * 8 - 1] = i
        count = count + 1
    imgbstr = ''
    for i in imgblist:
        imgbstr += i
    return imgbstr


# 用替换后的二进制RGB绘制成图片
def git_img(img, imgb):
    imglist = []
    imglenth = len(imgb) // 8
    for i in range(imglenth):
        imglist.append(int(imgb[i * 8:i * 8 + 8], 2))  # 将01二进制串按8个一组按R ，G，B的顺序转换位10进制数
    count = 0
    count1 = 1
    lenth = len(imglist)
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            img.putpixel((i, j), (imglist[count], imglist[count + 1], imglist[count + 2]))  # 按照原有的点位将修改后的RGB值写入
            count = count + 3
            if count1 == lenth:
                break
            count1 += 1
        if count1 == lenth:
            break
    img.save('img.png')


#  对加密的图片进行解密，得到插入的内容
def get_code(imgb,textlenth):
    count = 1
    imgblist = list(imgb)
    codebstring = ''
    lenth = len(imgblist) // 8  # 总为8的整数倍
    while True:
        if count == lenth:
            break
        codebstring += imgblist[count * 8 - 1]  # 取出第8位
        count = count + 1
    lentgh = len(codebstring) // 8
    count = 0
    codestring1 = ''
    while True:
        if count == textlenth:
            break
        codestring1 += chr(int(codebstring[count * 8:count * 8 + 8], 2))  # 按8个一组转换为字符
        count = count + 1
    with open('code.txt', 'w', encoding='utf-8') as f:
        f.write(codestring1)


if __name__ == '__main__':
    print('********************************* Lsb_img *****************************\n', 'starting...')
    if len(sys.argv) == 4:
        abs = sys.argv[1]
        imgpath = os.path.abspath(sys.argv[2])
        textpath = os.path.abspath(sys.argv[3])
    else:
        abs = '-d'
        textlenth = sys.argv[2]  # 要解码的文件长度
        imgpath = os.path.abspath(sys.argv[3])
    if os.path.splitext(imgpath)[-1] != '.png' and os.path.splitext(imgpath)[-1] != '.bmp':  # 判断文件格式是否可以隐写
        print('[*] There is a mistake in the format of your image,only support png and bmp')
        sys.exit()
    try:
        data = PIL.Image.open(imgpath)
        img = data.convert('RGB')

    except:
        print('[!] The img path is invalid')
        sys.exit()
    bimg = git_bimg(img)
    if abs == '-e' or abs == '-E' or abs == 'e' or abs == 'E':
        btext = git_text(textpath)
        if len(bimg) / 8 < len(btext):
            print('[!] The image pixel size used is not large enough to fully insert the selection...')
            chooes = input('[*] If you want to continue, please press Enter, else press q/Q to quit')
            if chooes == 'q' or chooes == 'Q':
                sys.exit()
        imgb = git_string(bimg, btext)
        git_img(img, imgb)
    if abs == '-d' or abs == '-D' or abs == 'd' or abs == 'D':
        get_code(bimg,textlenth)
    print('[*] successfully')
