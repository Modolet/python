from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from browsermobproxy import Server
import urllib.request
import time
import json


def switchWindow(name,wd):#切换窗口的函数
    for handle in wd.window_handles:
        wd.switch_to.window(handle)
        if name in wd.title:
            break

def entryFind(url,result):#找链接的函数
    for entry in result['log']['entries']:
        _url = entry['request']['url']
        if url in _url:
            return entry

def ready(wd):#开始前准备
    usr = '15912604113'
    pwd = 'mm.195874'
    #usr = input('请输入用户名')
    #pwd = input('请输入密码')
    wd.get("https://u.unipus.cn")
    wd.find_element_by_css_selector('body #SignIn').click()
    wd.find_element_by_css_selector('.form-group > input[name="username"').send_keys(usr)
    wd.find_element_by_css_selector('.form-group > input[name="password"').send_keys(pwd)
    wd.find_element_by_css_selector('button[id="login"]').click()
    wd.find_element_by_css_selector('a.layui-layer-btn0').click()
    switchWindow('环境检测', wd)
    time.sleep(2)
    wd.find_element_by_css_selector('.text >.btn-bar > .btn.nextStep').click()
    print(wd.find_element_by_css_selector('.text >.btn-bar > .btn.nextStep').text)
    wd.find_element_by_css_selector('.play_properly[onclick="next_handler()"]').click()
    wd.find_element_by_css_selector('.btn.yes').click()
    wd.find_element_by_css_selector('.btn-text >.btn-bar > .btn.nextStep').click()
    time.sleep(8)
    wd.find_element_by_css_selector('.beginEnjoy').click()
    switchWindow('U校园', wd)
    wd.find_element_by_css_selector('.course-content > .my_course_item').click()
    first = wd.find_elements_by_css_selector('.group.courseware > div:nth-child(1)')# 获取题目的元素
    time.sleep(5)
    first[0].click()

def getAnswerUrl(wd):#获取答案的url
    currentUrl = str(wd.current_url)
    return 'https://ucontent.unipus.cn/course/api/content/course-v1:Unipus+nhce_3_rwzh_2+2018_09/' + currentUrl.split('/')[-2] + '/default/'


server = Server(r".\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat")#初始化抓包服务
server.start()
proxy = server.create_proxy()#创建代理
proxy.wait_for_traffic_to_stop(1,60)#设置
options = webdriver.ChromeOptions()#实例化chromeoptions
options.add_argument('--proxy-server={0}'.format(proxy.proxy))#设置代理
wd = webdriver.Chrome(chrome_options=options)#启动浏览器
wd.implicitly_wait(10)#设置等待元素的超时时间
num = ready(wd)#登录，选择课程
print("共有",num,"个大题")
num = 1

for page in wd.find_elements_by_css_selector('.group.lock.courseware>.name'):#依次点击所有题目
    time.sleep(3)
    try:
        wd.find_element_by_css_selector('[style="position: relative; opacity: 1; font-size: 14px; letter-spacing: 0px; text-transform: uppercase; font-weight: normal; margin: 0px; user-select: none; padding-left: 20px; padding-right: 20px; color: rgb(255, 255, 255);"]').click()
    except:
        pass
    n = 0
    page.click()#点击
    proxy.new_har(num,options={'captureHeaders': True, 'captureContent': True,'captureBinaryContent':True})#开始抓包
    time.sleep(5)
    try:#找确认按钮
        wd.find_element_by_css_selector('[style="position: relative; opacity: 1; font-size: 14px; letter-spacing: 0px; text-transform: uppercase; font-weight: normal; margin: 0px; user-select: none; padding-left: 20px; padding-right: 20px; color: rgb(255, 255, 255);"]').click()
    except:#找不到直接过
        pass
    AnswerUrl = getAnswerUrl(wd)#获取答案链接
    try:
        answers = entryFind(AnswerUrl, proxy.har)
        answers = json.loads(answers['response']['content']['text'])
        answers = json.loads(answers['content'])
        inputAnswer = wd.find_elements_by_css_selector('[type="text"].fill-blank--bc-input-DelG1')
        if inputAnswer == None:
            inputAnswer = wd.find_element_by_css_selector('.writing--writing-margin-bshnP>.writing--textarea-36VPs')
        print('共有', inputAnswer.__len__(), '个空')
        for answer in answers['questions:scoopquestions']['questions']:
            for each in answer['answers']:
                print('第', num,'页','第',n + 1, '题答案为:', each)
                inputAnswer[n].send_keys(each)
                n += 1
    except:
        print("本页未找到答案")
        continue
    try:
        wd.find_element_by_css_selector('button.submit-bar-pc--btn-1_Xvo').click()
        wd.find_element_by_css_selector('[style="height: 30px; border-radius: 2px; transition: all 450ms cubic-bezier(0.23, 1, 0.32, 1) 0ms; top: 0px;"]').click()
        next = wd.find_elements_by_css_selector('[style="position: relative; opacity: 1; font-size: 14px; letter-spacing: 0px; text-transform: uppercase; font-weight: normal; margin: 0px; user-select: none; padding-left: 20px; padding-right: 20px; color: rgb(255, 255, 255);"]')
        next[1].click()
    except:
        pass
    try:
        page.send_keys(Keys.F5)
    except:
        pass