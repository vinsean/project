import pandas as pd
import requests


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
    print(student[0]+":")
    print(logres['err_desc'])

    if logres['err_desc'] != "":
        print("   正在修改"+student[0]+'的密码')

        #管理员Cookie
        gheader = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            #'Cookie': 'SpecialGID = 8b0b7f7cc7c44030a28d39b69737069b;uuid_dd39b150 - a934 - 11e9 - b073 - e9b8d9c630e7 = fd5c360e - e0f1 - 43a2 - 84f7 - e722e5360f12;accessId = dd39b150 - a934 - 11e9 - b073 - e9b8d9c630e7;href = https % 3A % 2F % 2Fjiangmen.xueanquan.com % 2Flogin.html;ASP.NET_SessionId = gw1unorxc3s3bqt2erbm2zhd;_UCodeStr = { % 0d % a"Grade": 4, % 0d % 0a"ClassRoom": 533908841, % 0d % 0a"CityCode": 120017 % 0d % 0a}; SafeApp = true;_UserID = aNWVg82ctFcU7bw15m + xkcfDW5AgaF3uvCrjO4M9asA =;RiskApp = true;PeiXun_UserID = BE80E175CE7735332909F542A3993661;Training = true;qimo_seosource_0 = % E7 % AB % 99 % E5 % 86 % 85;qimo_seokeywords_0 =;qimo_seosource_dd39b150 - a934 - 11e9 - b073 - e9b8d9c630e7 = % E7 % AB % 99 % E5 % 86 % 85;qimo_seokeywords_dd39b150 - a934 - 11e9 - b073 - e9b8d9c630e7 =;qimo_xstKeywords_dd39b150 - a934 - 11e9-b073-e9b8d9c630e7=;UserID=B870FF5CD7E11693F318AF60966A7781;ServerSide=https://jiangmen.xueanquan.com;pageViewNum=47'
            'Cookie':'qimo_seosource_0=%E7%AB%99%E5%86%85; qimo_seokeywords_0=; uuid_dd39b150-a934-11e9-b073-e9b8d9c630e7=ab282226-7003-440b-a556-bd4cbd7d5662; qimo_seosource_dd39b150-a934-11e9-b073-e9b8d9c630e7=%E7%AB%99%E5%86%85; qimo_seokeywords_dd39b150-a934-11e9-b073-e9b8d9c630e7=; qimo_xstKeywords_dd39b150-a934-11e9-b073-e9b8d9c630e7=; href=https%3A%2F%2Fjiangmen.xueanquan.com%2Flogin.html; accessId=dd39b150-a934-11e9-b073-e9b8d9c630e7; ASP.NET_SessionId=dspqvujdr513ygnxg2ozw5d0; UserID=6C811E0E8AF1C013FE3F6A841B4F084A; ServerSide=https://jiangmen.xueanquan.com; _UCodeStr={%0d%0a  "Grade": 5,%0d%0a  "ClassRoom": 533908960,%0d%0a  "CityCode": 120017%0d%0a}; _UserID=KPKy5xA86SEC2dnmlaX6oYh709sj4EGdLzyv5HPMnfk=; SafeApp=true; RiskApp=true; PeiXun_UserID=26BF96B8787BF0E02EC3609F8067252D; Training=true; pageViewNum=5'
        }

        #重置密码
        resp = requests.post(
            'https://jiangmen.xueanquan.com/eduadmin/ClassManagement/StudentPassWordReset?studentid=' + str(student[1]),
            headers=gheader).json()
        print("  "+resp['message'])

        userData = {"username": name, "password": "123456", "loginOrigin": 1}
        logres = session.post(loginUrl, json=userData, headers=headers).json()
        if logres['err_desc'] == "":
            print("   使用原始密码登陆成功")

        #设置密码
        session.headers['Authorization'] = logres['data']['token']
        setpd = {"oldPwd": "123456", "newPwd": "Ab123456"}
        setpdres = session.post('https://appapi.xueanquan.com/usercenter/api/users/edit-pwd-byoldpwd?api-version=2',
                                json=setpd, headers=headers).json()
        print("   密码" +setpdres['message'])

        userData = {"username": name, "password": "Ab123456", "loginOrigin": 1}
        logres = session.post(loginUrl, json=userData, headers=headers).json()

    return logres

def study(users):
    couseNum = 0
    huodongfinishNum = 0
    skillfinishNum = 0
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
                    huodongfinishNum = huodongfinishNum + 1
                    skillfinishNum = skillfinishNum + 1
                    print("恭喜" + studentName + "不用学习")
                else:
                    homeworklistres = session.get(homeworklistUrl).json()

                    if len(homeworklistres) > 0:
                        for couse in homeworklistres:
                            if couse['workStatus'] == 'UnFinish':

                                couseTitle = couse['title']

                                #专题活动学习
                                if couse['subTitle'] == '专题活动':

                                    step1data = {"specialId": 839, "step": 1}
                                    session.post(huodongSignUrl, json=step1data).json()
                                    step2data = {"specialId": 839, "step": 2}
                                    session.post(huodongSignUrl, json=step2data).json()
                                    huodongres = session.get(
                                        'https://huodongapi.xueanquan.com/p/guangdong/Topic/topic/platformapi/api/v1/records/finish-status?specialId=839').json()
                                    if huodongres['finishStatus']:
                                        huodongfinishNum = huodongfinishNum + 1
                                        print('   专题活动：' + couseTitle + '完成')
                                    else:
                                        print('   专题活动：' + couseTitle + '×××未完成×××')

                                #安全技能学习
                                elif couse['subTitle'] == '安全学习':

                                    print('   正在学习:' + couseTitle)
                                    couseId = couse['url'].split('=')[-1]

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
                    

    print('安全平台完成情况：')
    print('  活动专题完成人数：' + str(huodongfinishNum) +',未完成人数：' +str(len(users['name'])-huodongfinishNum))
    print('  安全技能完成人数：' + str(huodongfinishNum) +',未完成人数：' +str(len(users['name'])-huodongfinishNum))



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
todo = ['周晓平', '朱安轩']
todolist = users[users['name'].isin(todo)]

study(todolist)
