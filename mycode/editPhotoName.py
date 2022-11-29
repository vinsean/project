from cnocr import CnOcr
import os
import time
import uuid
import random

#把中文名的文件转换为纯数字
def renameDir():
    screenshots = os.listdir(screenshots_path)
    for scshot in screenshots:
        renamescshot = str(uuid.uuid1())
        os.rename(screenshots_path+scshot, screenshots_path+renamescshot+'.jpg')



screenshots_path = 'C:\\Users\\vinsean\\Desktop\\20221127\\'
key = ["蔡恒光","曾圣朗","曾鑫楠","陈家俊","陈俊儒","陈雅琳","陈子乐","邓振宇","付可馨","傅梦瑶","傅直霖","古文勋","李宸熙","李思婷","廖慧瑶","林凯欢","林悦娉","罗宝砚","罗晞妍","罗心雨","罗学为","罗颖晴","罗颖熙","彭晨峰","吴慧婷","吴俊承","吴梓诚","谢建航","谢紫宁","杨希","杨端渝","杨梦琪","叶绮珊","张俊鑫","张钰桐","郑狄瑞","钟嘉懿","钟贤军","钟卓汝","朱子琳","庄嘉熙","庄宇旭","邹雅芳"]

ocr = CnOcr()
renameDir()
screenshots = os.listdir(screenshots_path)

for screenshot in screenshots:
    scshot_path = screenshots_path + screenshot
    result = ocr.ocr(scshot_path)

    words = ''
    for word in result:
        words = words + word['text'] + ','

    for name in key:
        if name in words:
            if os.path.exists(screenshots_path + name + '.jpg'):
                rannum = str(random.randint(10000,100000))
                os.rename(scshot_path, screenshots_path + name + rannum + '.jpg')
            else:
                os.rename(scshot_path, screenshots_path + name + '.jpg')




