import pandas as pd
import requests
import re
import datetime
from random import randint
from urllib import parse


'''
1.修改学生名单url
2.修改未完成平台的学生名单（3处）
3.修改班主任cookie
'''


def loginPlat(session, student, headers):
    name = student[2]
    session.get(url=mainurl, headers=headers)

    userData = {"username": name, "password": "Ab123456", "loginOrigin": 1}
    logres = session.post(loginUrl, json=userData, headers=headers).json()
    print('\n')
    print(student[0]+":")
    print(logres['err_desc'])

    if logres['err_desc'] != "":
        print("   正在修改"+student[0]+'的密码')

        #管理员Cookie
        gheader = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            #'Cookie': 'SpecialGID=49ff050117b9427f94db4a9ec7187064; accessId=dd39b150-a934-11e9-b073-e9b8d9c630e7; SafeApp=true; RiskApp=true; Training=true; uuid_dd39b150-a934-11e9-b073-e9b8d9c630e7=9679805b-ad5a-42a1-9fea-5c2bd29b8f1c; href=https%3A%2F%2Fjiangmen.xueanquan.com%2Flogin.html; ASP.NET_SessionId=biesenhpre20xtdhndfozh2k; _UCodeStr={%0d%0a  "Grade": 4,%0d%0a  "ClassRoom": 533908841,%0d%0a  "CityCode": 120017%0d%0a}; UserID=B870FF5CD7E11693F318AF60966A7781; ServerSide=https://jiangmen.xueanquan.com; _UserID=aNWVg82ctFcU7bw15m+xkcfDW5AgaF3uvCrjO4M9asA=; PeiXun_UserID=BE80E175CE7735332909F542A3993661; qimo_seosource_0=%E7%AB%99%E5%86%85; qimo_seokeywords_0=; qimo_seosource_dd39b150-a934-11e9-b073-e9b8d9c630e7=%E7%AB%99%E5%86%85; qimo_seokeywords_dd39b150-a934-11e9-b073-e9b8d9c630e7=; qimo_xstKeywords_dd39b150-a934-11e9-b073-e9b8d9c630e7=; pageViewNum=47'
            'Cookie':'SpecialGID=49ff050117b9427f94db4a9ec7187064; qimo_seosource_0=%E7%AB%99%E5%86%85; qimo_seokeywords_0=; uuid_dd39b150-a934-11e9-b073-e9b8d9c630e7=c3bf6d6f-cd24-46ec-912c-75fa9a62ccca; qimo_seosource_dd39b150-a934-11e9-b073-e9b8d9c630e7=%E7%AB%99%E5%86%85; qimo_seokeywords_dd39b150-a934-11e9-b073-e9b8d9c630e7=; qimo_xstKeywords_dd39b150-a934-11e9-b073-e9b8d9c630e7=; href=https%3A%2F%2Fjiangmen.xueanquan.com%2Flogin.html; accessId=dd39b150-a934-11e9-b073-e9b8d9c630e7; ASP.NET_SessionId=m0d5ujnz4k4xs3lnyrdgfuqi; UserID=6C811E0E8AF1C013FE3F6A841B4F084A; ServerSide=https://jiangmen.xueanquan.com; _UCodeStr={%0d%0a  "Grade": 5,%0d%0a  "ClassRoom": 533908960,%0d%0a  "CityCode": 120017%0d%0a}; _UserID=KPKy5xA86SEC2dnmlaX6oYh709sj4EGdLzyv5HPMnfk=; SafeApp=true; RiskApp=true; PeiXun_UserID=26BF96B8787BF0E02EC3609F8067252D; Training=true; pageViewNum=3'
        }

        #重置密码
        resp = requests.post('https://jiangmen.xueanquan.com/eduadmin/ClassManagement/StudentPassWordReset?studentid=' + str(student[1]),headers=gheader).json()
        print("  "+resp['message'])

        userData = {"username": name, "password": "123456", "loginOrigin": 1}
        logres = session.post(loginUrl, json=userData, headers=headers).json()
        if logres['err_desc'] == "":
            print("   使用原始密码登陆成功")

        #设置密码
        session.headers['Authorization'] = logres['data']['token']
        setpd = {"oldPwd": "123456", "newPwd": "Ab123456"}
        setpdres = session.post('https://appapi.xueanquan.com/usercenter/api/users/edit-pwd-byoldpwd?api-version=2',json=setpd, headers=headers).json()
        print("   密码" +setpdres['message'])

        userData = {"username": name, "password": "Ab123456", "loginOrigin": 1}
        logres = session.post(loginUrl, json=userData, headers=headers).json()

    return logres

def summer():
    userinfores = session.get('https://huodongapi.xueanquan.com/p/guangdong/Topic/topic/platformapi/api/v1/users/user-info').json()
    truename = userinfores['trueName']
    sex = str(userinfores['sex'])

    r = randint(1000000000000000,9999999999999999)/10000000000000000                                  
    answerstr = '[{"ID":1,"N":'+ sex +',"M":""},{"ID":2,"N":"1","M":""},{"ID":3,"N":"4","M":""},{"ID":4,"N":"2","M":""},{"ID":5,"N":"3","M":""},{"ID":6,"N":"2","M":""},{"ID":7,"N":"3","M":""},{"ID":8,"N":"2","M":""},{"ID":9,"N":"2","M":""},{"ID":10,"N":"2","M":""},{"ID":11,"N":"3","M":""},{"ID":12,"N":"1","M":""},{"ID":13,"N":"3","M":""},{"ID":14,"N":"3","M":""},{"ID":15,"N":"1","M":""},{"ID":16,"N":"1","M":""},{"ID":17,"N":"2","M":""},{"ID":18,"N":"1","M":""},{"ID":19,"N":"3","M":""},{"ID":20,"N":"1","M":""},{"ID":21,"N":"2","M":""},{"ID":22,"N":"1","M":""},{"ID":23,"N":"2","M":""},{"ID":24,"N":"2","M":""},{"ID":25,"N":"2","M":""},{"ID":26,"N":"2","M":""},{"ID":27,"N":"2","M":""},{"ID":28,"N":"3","M":""},{"ID":29,"N":"1","M":""},{"ID":30,"N":"2","M":""},{"ID":31,"N":"2","M":""},{"ID":32,"N":"3","M":""},{"ID":33,"N":"3","M":""},{"ID":34,"N":"1","M":""},{"ID":35,"N":"2","M":""},{"ID":36,"N":"5","M":""},{"ID":37,"N":"5","M":""},{"ID":38,"N":"5","M":""},{"ID":39,"N":"5","M":""},{"ID":40,"N":"5","M":""},{"ID":41,"N":"1","M":""},{"ID":42,"N":"5","M":""},{"ID":43,"N":"5","M":""},{"ID":44,"N":"5","M":""},{"ID":45,"N":"5","M":""},{"ID":46,"N":"5","M":""},{"ID":47,"N":"1","M":""},{"ID":48,"N":"5","M":""},{"ID":49,"N":"5","M":""},{"ID":50,"N":"5","M":""},{"ID":51,"N":"5","M":""},{"ID":52,"N":"1","M":""},{"ID":53,"N":"5","M":""},{"ID":54,"N":"5","M":""},{"ID":55,"N":"5","M":""},{"ID":56,"N":"5","M":""},{"ID":57,"N":"5","M":""},{"ID":58,"N":"5","M":""},{"ID":59,"N":"1","M":""},{"ID":60,"N":"5","M":""},{"ID":61,"N":"5","M":""},{"ID":62,"N":"5","M":""},{"ID":63,"N":"4","M":""},{"ID":64,"N":"5","M":""},{"ID":65,"N":"5","M":""},{"ID":66,"N":"5","M":""},{"ID":67,"N":"5","M":""},{"ID":68,"N":"5","M":""},{"ID":69,"N":"5","M":""},{"ID":70,"N":"5","M":""},{"ID":71,"N":"5","M":""},{"ID":72,"N":"5","M":""},{"ID":73,"N":"5","M":""},{"ID":74,"N":"5","M":""}]'
    sstr1 = '&schoolYear=2023&semester=2&userType=0&answerJson='
    sstr2 = '&prv=12&city=120017&county=120017004&school=331227891&grade=5&Class=533908960&comefrom=20230&version=2&prvName2=&cityName2=&shcoolName=%E5%8F%B0%E5%B1%B1%E5%B8%82%E8%B5%A4%E6%BA%AA%E9%95%87%E4%B8%AD%E5%BF%83%E5%B0%8F%E5%AD%A6&TrueName='
    substr = 'r='+str(r) + sstr1 + parse.quote(answerstr) + sstr2 + parse.quote(truename)
  
    signdata = {"schoolYear":2023,"semester":2,"step":1}
    signres = session.post('https://huodongapi.xueanquan.com/p/guangdong/Topic/topic/platformapi/api/v1/holiday/sign', json=signdata).json()

    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    infores = session.post('https://huodong.xueanquan.com/HolidayService/SubmitTest', headers = headers, data=substr).json()
    signdata = {"schoolYear":2023,"semester":2,"step":2}
    signres = session.post('https://huodongapi.xueanquan.com/p/guangdong/Topic/topic/platformapi/api/v1/holiday/sign', json=signdata).json()

    huodongres = session.get('https://huodongapi.xueanquan.com/p/guangdong/Topic/topic/platformapi/api/v1/holiday/finish-status?schoolYear=2023&semester=2').json()
    if huodongres['finishStatus']:
        print('   暑假专题完成')
    else:
        print('   暑假专题×××未完成×××')


def study(users):
    couseNum = 0
    huodongunfinishNum = 0
    skillunfinishNum = 0

    if len(users) > 0:
        for i in range(len(users)):
            student = users.iloc[i].values
            studentName = student[0]
            logres = loginPlat(session, student, session.headers)

            if logres['err_code'] == 0:
                studentName = logres['data']['trueName']
                print(studentName + '登陆成功')

                couseres = session.get(courseurl).json()
                
                couseNum = couseres['result']

                if couseNum == 0:
                    print("恭喜" + studentName + "不用学习")
                else:
                    homeworklistres = session.get(homeworklistUrl).json()

                    if len(homeworklistres) > 0:

                        #需要完成专题活动、安全技能课程数
                        huodongtotal = 0
                        skilltotal = 0 

                        huodongfinishNum = 0
                        skillfinishNum = 0

                        for couse in homeworklistres:
                            if couse['workStatus'] == 'UnFinish':

                                couseTitle = couse['title']

                                #专题活动学习
                                if couse['subTitle'] == '专题活动':

                                    huodongtotal = huodongtotal + 1

                                    huodongurl = couse['url']
                                    huodongmessageurl = huodongurl.replace('index.html', 'message.html')
                                    html = session.get(huodongmessageurl).text
                                    title=re.findall('<title>(.+)</title>',html)

                                    if len(title)>0:
                                    
                                        huodongId = str(title[0])
                                        step1data = {"specialId": huodongId, "step": 1}
                                        session.post(huodongSignUrl, json=step1data).json()
                                        step2data = {"specialId": huodongId, "step": 2}
                                        session.post(huodongSignUrl, json=step2data).json()
                                        '''
                                        huodongres = session.get(
                                            'https://huodongapi.xueanquan.com/p/guangdong/Topic/topic/platformapi/api/v1/records/finish-status?specialId='+str(huodongId)).json()
                                        if huodongres['finishStatus']:
                                            huodongfinishNum = huodongfinishNum + 1
                                            print('   专题活动：' + couseTitle + '完成')
                                        else:
                                            print('   专题活动：' + couseTitle + '×××未完成×××')
                                        '''
                                        summer()
                                    else:
                                        print('specialId为空')

                                #安全技能学习
                                elif couse['subTitle'] == '安全学习':
                                    
                                    skilltotal = skilltotal + 1

                                    print('   正在学习:' + couseTitle)
                                    couseId = couse['url'].split('=')[2].split('&')[0]

                                    videores = session.get(couse['url'])

                                    gid = couse['url'].split('=')[1].split('&')[0]
                                    seevideoUrl = 'https://yyapi.xueanquan.com/guangdong/JiaTing/CommonHandler/info?api-version=1&contentId=0&gradeId=' + gid+'&courseId=' + couseId
                                    seevideores = session.get(seevideoUrl)

                                    session.get(testPaperUrl + couseId)
                                    testres = session.get(testPaperUrl + couseId).json()
                                  
                                    fid = testres['result']['fid']
                                    workId = testres['result']['workId']

                                    answer = {"workId": workId, "fid": fid, "title": couseTitle, "require": "",
                                            "purpose": "",
                                            "contents": "", "testanswer": "0|0|0", "testinfo": "已掌握技能", "testMark": 100,
                                            "testResult": 1, "siteName": "", "siteAddrees": "",
                                            "watchTime": "2022-04-08T02:45:24.323Z", "courseID": couseId}
                                    submitres = session.post(submitUrl, json=answer).json()

                                    if submitres['success']:
                                        skillfinishNum = skillfinishNum + 1
                                        print("   " + couseTitle + '问卷测试完成')
                                    else:
                                        print("   问卷未完成！！！ "+submitres['message'])

                            else:
                                continue

                            if huodongfinishNum < huodongtotal:
                                huodongunfinishNum = huodongunfinishNum + 1
                            
                            if skillfinishNum < skilltotal:
                                skillunfinishNum = skillunfinishNum + 1
                    

    print('安全平台完成情况：')
    print('  活动专题完成人数：' + str(len(users['name'])-huodongunfinishNum) +',未完成人数：' + str(huodongunfinishNum))
    print('  安全技能完成人数：' + str(len(users['name'])-skillunfinishNum) +',未完成人数：' + str(skillunfinishNum))



session = requests.session()

mainurl = 'https://jiangmen.xueanquan.com/login.html'
loginUrl = 'https://appapi.xueanquan.com/usercenter/api/v3/wx/login?checkShowQrCode=true&tmp=false'
courseurl = 'https://yyapi.xueanquan.com/guangdong/api/v1/StudentHomeWork/NoFinishHomeWorkCount'
homeworklistUrl = 'https://yyapi.xueanquan.com/guangdong/safeapph5/api/v1/homework/homeworklist'
#seevideoUrl = 'https://yyapi.xueanquan.com/guangdong/JiaTing/CommonHandler/info?api-version=1&contentId=0&gradeId=488&courseId='
testPaperUrl = 'https://yyapi.xueanquan.com/guangdong/api/v1/StudentHomeWork/GetSkillTestPaper?courseId='
submitUrl = 'https://yyapi.xueanquan.com/guangdong/api/v1/StudentHomeWork/HomeWorkSign'
huodongSignUrl = 'https://huodongapi.xueanquan.com/p/guangdong/Topic/topic/platformapi/api/v1/records/sign'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
session.headers = headers


users = pd.read_excel('C:\\Users\\retir\\Desktop\\四3班\\账号资料\\zhu.xlsx')
#users = users.drop(index=users[(users.name == '罗宝砚') | (users.name == '罗颖晴')].index.tolist())

todo = ['谢紫宁', '杨希']
#todolist = users[users['name'].isin(todo)]

todolist = users[users['name'].isin(users['name'])]

study(todolist)
session.close()
