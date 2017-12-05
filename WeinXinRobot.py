import requests
import itchat
from bs4 import BeautifulSoup
import time
from itchat.content import *
import threading
# 设置图灵机器码
KEY = 'f82c17286c6c4e7fab69b14ad3ca8fdf'

# 声明一个计数器，储存回复的次数，达到获取更多帖子的目的
i = 1

# status
replyToChat = 1



# 构造请求头
headers = {
    'authority': 'news.dmzj.com',
    'method': 'GET',
    'path': '/article/11873.html',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': 'UM_distinctid=15eef7c416b5a5-05bf2c59a72025-3e63430c-100200-15eef7c416c601; bdshare_firstime=1507256451687; show_tip_1=0; CNZZDATA1000465408=808515455-1507256101-null%7C1507263505; CNZZDATA1255208924=1644658608-1507253867-null%7C1507261388',
    'referer': 'http://news.dmzj.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}


# 注册方法,isGroupChat=True

@itchat.msg_register(TEXT)
def auto_reply(msg):
    print("自动回复线程执行中")
    if msg['ToUserName'] == 'filehelper':
    # itchat.send('拦截到了你发的信息',toUserName='filehelper')
        tofilehelper_msg(msg)
        return
    else:
        print("全局变量为reply的值为"+str(replyToChat))
    
        #defaultReply = 'I received you msg: \n' + msg['Text']+' at '+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 如果图灵Key出现问题，那么reply将会是None
        reply = get_response(msg['Text']) + "[来自Cy的Python小机器人]"

        if replyToChat!=1:
            reply=None

        if reply!=None:
            itchat.send("TuLing回复了一条信息 " + reply, 'filehelper')
        # a or b的意思是，如果a有内容，那么返回a，否则返回b
        # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
    return reply






# 图灵回复接口
def get_response(msg):
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')

    except:
        # 将会返回一个None
        return


# filehelper回复处理
def tofilehelper_msg(msg):
    global replyToChat
    if msg['Text'] == "情感专区":
        AcFun_Emotion()
        return

    if msg['Text'] == "更多":
        global i
        i = i + 1
        AcFun_More(i)
        return

    if msg['Text'] == "乱弹":
        Osc_Topic()
        return

    if msg['Text'] == "课表":

        return

    if msg['Text'] == "关闭":
        replyToChat = 0
        print("设置为状态："+str(replyToChat))
        itchat.send('已关闭','filehelper')
        return replyToChat

    if msg['Text'] ==  "开启":
        replyToChat = 1
        print("设置为状态：" + str(replyToChat))
        itchat.send('已启动', 'filehelper')
        return replyToChat




def AcFun_Emotion():
    i = 1
    r = requests.get("http://www.acfun.cn/v/list73/index_" + str(i) + ".htm")
    soup = BeautifulSoup(r.text, 'html.parser')
    titles = soup.select('div[class=mainer] div[class=item] a[class=title]')
    for title in titles:
        itchat.send(title.text + '\n' + "http://www.acfun.cn" + title.get('href'), 'filehelper')
        # 测试发给发来信息的人
        # itchat.send(title.text + '\n' + "http://www.acfun.cn" + title.get('href'), toUserName=msg['FromUserName'])
    itchat.send("回复更多获取更多帖子", 'filehelper')
    return


def AcFun_More(i):
    r = requests.get("http://www.acfun.cn/v/list73/index_" + str(i) + ".htm")
    soup = BeautifulSoup(r.text, 'html.parser')
    titles = soup.select('div[class=mainer] div[class=item] a[class=title]')
    for title in titles:
        itchat.send(title.text + '\n' + "http://www.acfun.cn" + title.get('href'), 'filehelper')
        # 同上itchat.send(title.text + '\n' + "http://www.acfun.cn" + title.get('href'),toUserName=msg['FromUserName'])
    itchat.send("回复更多获取更多帖子", 'filehelper')
    return


def Osc_Topic():
    r = requests.get("https://my.oschina.net/xxiaobian/blog", headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    titles = soup.select('div[class=title] a')
    for title in titles:
        itchat.send(title.text + '\n' + title.get('href'), 'filehelper')
        return
    return


# hotReload=True
itchat.auto_login()
itchat.run()


