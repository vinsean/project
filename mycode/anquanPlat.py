import pandas as pd
import requests
import re
import time


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
            'Cookie':''
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
                                        huodongres = session.get(
                                            'https://huodongapi.xueanquan.com/p/guangdong/Topic/topic/platformapi/api/v1/records/finish-status?specialId='+str(huodongId)).json()
                                        if huodongres['finishStatus']:
                                            huodongfinishNum = huodongfinishNum + 1
                                            print('   专题活动：' + couseTitle + '完成')
                                        else:
                                            print('   专题活动：' + couseTitle + '×××未完成×××')
                                    else:
                                        print('specialId为空')

                                #安全技能学习
                                elif couse['subTitle'] == '安全学习':
                                    

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
                    

    print('安全平台完成情况：')
    print('  活动专题完成人数：' + str(huodongfinishNum) +',未完成人数：' +str(len(users['name'])-huodongfinishNum))
    print('  安全技能完成人数：' + str(skillfinishNum) +',未完成人数：' +str(len(users['name'])-skillfinishNum))



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


users = pd.read_excel('C:\\Users\\retir\\Desktop\\账号资料\\zhu.xlsx')
#users = users.drop(index=users[(users.name == '谢紫宁')].index.tolist())

todo = ['谢紫宁', '杨希']
#todolist = users[users['name'].isin(todo)]

todolist = users[users['name'].isin(users['name'])]

study(todolist)
