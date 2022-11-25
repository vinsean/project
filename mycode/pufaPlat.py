import uuid
import requests
import os
import ddddocr
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
import base64
import json
import time

def getimgcode(uuidstr):

    mainstr = 'https://service-rr3eta5l-1251413566.sh.apigw.tencentcs.com/userAuthApi/user/captcha?uuid='

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

    res = requests.get(mainstr + uuidstr, headers=headers)

    if os.path.exists('./imgcode/img_code.jpg'):
        os.remove('./imgcode/img_code.jpg')

    with open('./imgcode/img_code.jpg', 'wb') as f:
        f.write(res.content)

def ocrimgcode():
    ocr = ddddocr.DdddOcr()

    with open('./imgcode/img_code.jpg', 'rb') as f:
        img_bytes = f.read()

    img_result = ocr.classification(img_bytes)
    print('验证码：'+ img_result)
    return img_result


def encrypt(text, uuidstr):
    pubkey = '-----BEGIN PUBLIC KEY-----\n'+ getrsakey(uuidstr) + '\n-----END PUBLIC KEY-----'
    
    rsakey = RSA.importKey(pubkey.encode())
    ciper = Cipher_pksc1_v1_5.new(rsakey)
    text = text + ',' + str(int(time.time() * 1000))

    en_data = base64.b64encode(ciper.encrypt(text.encode())).decode()
    print(en_data)

def getrsakey(uuidstr):
    rsakeyurl = 'https://service-rr3eta5l-1251413566.sh.apigw.tencentcs.com/userAuthApi/user/login/rsaKey?uuid=' + uuidstr

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

    res = requests.get(rsakeyurl + uuidstr, headers=headers).content.decode('utf-8')
    
    return json.loads(res)['data']

def login(userInfo, uuidstr):
    loginurl = 'https://service-rr3eta5l-1251413566.sh.apigw.tencentcs.com/userAuthApi/authorization/web/login/auth'

    getimgcode(uuidstr)
    code = ocrimgcode()

    loginInfo = encrypt(userInfo[0], uuidstr)
    pwd = encrypt(userInfo[2], uuidstr)
    
    data = {"loginInfo":loginInfo,"userName": userInfo[1],"password":pwd,"captcha":code,"source":2,"sourceId":3,"uuid":uuidstr}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

    res = requests.post(loginurl, json=data, headers=headers).content.decode('utf-8')
    print(res)
    return res
    
uuidstr = str(uuid.uuid1())

userInfo = ['G440781201303128917', '曾圣朗', '128917']

login(userInfo, uuidstr)


