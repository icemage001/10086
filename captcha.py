# -*- coding:UTF-8 -*-
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

#返回图片差异
def mse(imageA, imageB):
    err = np.sum((imageA.astype('float') - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err


def deCAPTCHA(png):
    image = cv2.imread(png)
    plt.interactive(False)

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #反色
    gray = cv2.bitwise_not(gray)
    #二值化
    ret, binary = cv2.threshold(gray, 90, 250, cv2.THRESH_BINARY)
    binarybak = binary
    #分割
    croped1 = binarybak[1:30, 0:13]
    croped2 = binarybak[1:30, 13:24]
    croped3 = binarybak[1:30, 24:35.5]
    croped4 = binarybak[1:30, 35.5:47]
    cropeds = []
    cropeds.append(croped1)
    cropeds.append(croped2)
    cropeds.append(croped3)
    cropeds.append(croped4)
    cropedAry = []
    #寻找边界
    for croped in cropeds:
        contours, hierarchy = cv2.findContours(croped.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x: x[1])
        ary = []
        for (c, _) in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            ary.append((x, y, w, h))
        #寻找边界
        minx = 99999
        miny = 99999
        maxw = 0
        maxh = 0
        for index, shape in enumerate(ary):
            minx = min(minx, shape[0])
            miny = min(miny, shape[1])
            maxw = max(maxw, shape[2] + shape[0])
            maxh = max(maxh, shape[3] + shape[1])
        maxw = maxw - minx
        maxh = maxh - miny
        cropedAry.append((minx, miny, maxw, maxh))

    # fig = plt.figure()
    #保存各个字符图片
    for id, (x, y, w, h) in enumerate(cropedAry):
        roi = cropeds[id][y:y + h, x:x + w]
        thresh = roi.copy()
        # a = fig.add_subplot(1, len(ary), id + 1)
        res = cv2.resize(thresh, (20, 25))
        vcode_folder = 'vcode'
        cv2.imwrite(vcode_folder + '\\' + 'code' + str(id) + '.jpg', res)
    pics = []
    for x in range(4):
        p = cv2.imread(vcode_folder + '\\' + 'code' + str(x) + '.jpg')
        pics.append(p)

    verifycode = ''
    for j in range(4):
         verifycode = verifycode + getnumber(pics[j])
    return verifycode

#将图片与指定图片做对比，返回与之相比差异最小的。
def getnumber(pic):
    min_a = 99999999
    min_png = None
    for i in os.listdir('mask'):
        png = cv2.imread('mask\\' + i)
        if mse(png, pic) < min_a:
            min_a = mse(png, pic)
            min_index = i
    return min_index[0]

