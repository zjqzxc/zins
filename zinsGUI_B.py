# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.messagebox,threading
from tkinter.constants import *
from mainclass import *

a=Zins()
event=threading.Event()
event2=threading.Event()

def print(str):
    l4['text']=str

__author__ = {'name' : 'Flagplus',
              'Email' : 'zjqzxc@flagplus.net',
              'Created' : '2015-03-09'}
def donothing():
    filewin = Toplevel()
    button = Button(filewin, text="Do nothing button")
    button.pack()
def Version():
    filewin = Toplevel()
    tmpcnf = '%dx%d'%(350, 180)
    filewin.geometry(tmpcnf)
    filewin.title('版本')
    txt='\
Zins登陆器（男生版）测试版\n\
    V 1.0.2 Alpha\n\
如果距离编译时间过久，请前往http://zins.flagplue.net查找更新\n\
另：男生版讲在后续版本中提供更多稀奇古怪的功能，\n\
详情课参阅更新日志:)\n\
有任何问题，请描述问题并截图后发邮件至i@flagplus.net\n\
当然，您也可以邮件告诉我您还想要什么样的功能:)\n\
编译日期2015-03-09\
         '
    Label(filewin,text=txt).pack()
    button = Button(filewin, text='作者太啰嗦了',command=filewin.destroy)
    button.pack(side=BOTTOM)
def Help():
    filewin = Toplevel()
    tmpcnf = '%dx%d'%(350, 180)
    filewin.geometry(tmpcnf)
    filewin.title('帮助')
    txt='\
Zins登陆器（男生版）简易使用帮助\n\
输入用户名和密码，然后“登陆”就可以了。\n\
什么“在线人数已达上限”“IP已存在”，都交给Zins就可以啦~\n\
使用前请保证打开任意网页可以跳转到网关登陆页面^_^\n\
如有需求，可以使用不同的注销按钮，详情前参阅网站说明\n\
编译日期2015-03-09\
         '
    Label(filewin,text=txt).pack()
    button = Button(filewin, text='好的',command=filewin.destroy)
    button.pack(side=BOTTOM)
def About():
    filewin = Toplevel()
    tmpcnf = '%dx%d'%(350, 180)
    filewin.geometry(tmpcnf)
    filewin.title('关于')
    txt='\
关于Zins\n\
Zins是一款用于深澜公司网关登陆的跨平台非官方登录工具,\n\
详情请参阅http://zins.flagplus.net，并获得更新。\n\
网页版登陆器请访问http://gate.cugbteam.org(仅校内)\n\
开发者\n\
算法源自网路\n\
部分核心代码@怡红公子\n\
@Flagplus进行功能完善及GUI编写\
         '
    Label(filewin,text=txt).pack()
    button = Button(filewin, text='我知道了',command=filewin.destroy)
    button.pack(side=BOTTOM)
def alert(txt1,txt2):
    filewin = Toplevel()
    tmpcnf = '%dx%d'%(350, 150)
    filewin.geometry(tmpcnf)
    filewin.title(txt1)
    Label(filewin,text=txt2).pack()
    button = Button(filewin, text='确认',command=filewin.destroy)
    button.pack(side=BOTTOM)
    
def ConnectInfo():
    filewin = Toplevel()
    tmpcnf = '%dx%d'%(350, 180)
    filewin.geometry(tmpcnf)
    filewin.title('连接信息')
    
    txt='正在加载'
    conninfo=Label(filewin,text=txt)
    conninfo.pack()
    def destroythis():
        conninfo['text']='等待线程结束'
        event2.clear()
        time.sleep(0.6)
        filewin.destroy()        
    filewin.protocol("WM_DELETE_WINDOW", destroythis)
    button = Button(filewin, text='确认',command=destroythis)
    button.pack(side=BOTTOM)
    def showspeed():
        t=0
        while(True):
            if(event2.isSet()):
                time.sleep(0.5)
                t+=1
                if(t>=2):
                    try:
                        arr=a.getSpeed()
                        title1='实时速度\n'
                        txs='发送：'+str(arr['txspeed']/1000)+'KB/s'+'\n'
                        rxs='接收：'+str(arr['rxspeed']/1000)+'KB/s'+'\n'
                        title2='其他实时信息：\n'
                        timeshow='登陆时间：'+str(arr['time'])+'秒\n'
                        avaliabe='可用流量：'+str(arr['avaliable'])+'(0为不限制)\n'
                        used='已用流量：'+str(int(arr['used'])/1000000)+'MB/s （非实时更新）\n'
                        usershow='当前登陆：'+str(arr['user'])+'\n'
                        conninfo['text']=title1+txs+rxs+timeshow+avaliabe+used+usershow
                    except:
                        pass
                    t=0
            else:
                break
    threads2 = []
    t1 = threading.Thread(target=showspeed)
    threads2.append(t1)
    event2.set()   
    for t in threads2:
        t.setDaemon(True)
        t.start()
    
        

def reset():
    logout()
    val1.set('')
    val2.set('')
    C1.deselect()
    C2.deselect()
    C3.deselect()
    C4.deselect()

 
def menu(root):
    def ct():
        #b.update('system', 'type', str(val3.get()))
        if(val3.get()==2):
            strtype='Windows模式登陆'
        elif(val3.get()==10):
            strtype='iOS模式登陆'
        else:
            strtype='其他模式'
        print(strtype)
        if(val3.get()!=1):
            a.update('system', 'type', str(val3.get()))
            a.update('system', 'type6', str(val3.get()))
        else:
            a.update('system', 'type6', str(val3.get()))
    menubar = Menu(root)
    
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Reset", command=reset)
    filemenu.add_command(label="ConnectInfo", command=ConnectInfo)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    
    editmenu = Menu(menubar, tearoff=0)
    
    changtypemenu=Menu(editmenu)
    val3 = IntVar()
    changtypemenu.add_radiobutton(label="Windows",command=ct,variable=val3,value=2)
    changtypemenu.add_radiobutton(label="iOS",command=ct,variable=val3,value=10)
    changtypemenu.add_radiobutton(label="IPv6备用模式",command=ct,variable=val3,value=1)

    editmenu.add_cascade(label="ChangeType",menu=changtypemenu)
    editmenu.add_command(label="NetworkCheck",state=DISABLED)
    menubar.add_cascade(label="Edit", menu=editmenu)
    
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help", command=Help)
    helpmenu.add_command(label="Version", command=Version)
    helpmenu.add_command(label="About", command=About)
    menubar.add_cascade(label="Help", menu=helpmenu)
    
    root.config(menu=menubar)

def init():
    print('初始化...')
    try:
        lastuser=a.show('system', 'last')
    except:
        a.checkfile()
        return 1
    if lastuser and lastuser !='0':
        val1.set(lastuser)
        passwd=a.show(lastuser,'password')
        if passwd != '0':
            val2.set(passwd)
    if int(a.show('system', 'rememberpwd')):
        C1.select()
    if int(a.show('system', 'autologin')):
        C2.select()
    if int(a.show('system', 'ipv4')):
        C3.select()
    if int(a.show('system', 'ipv6')):
        C4.select()
    if CheckVar2.get()==1:
        login()
    print('初始化完成')
    updatestatus()

def keeplive():
    t=0
    while(True):
        if(event.isSet()):
            time.sleep(1)
            t+=1
            if(t>=60):
                print('keeplive')
                a.sendHeartbeatPacket()
                t=0
        else:
            print('exit!')
            break

def updatestatus():
    ipv4status=a.getKeeplive()
    if ipv4status:
        if ipv4status=='timeout':
            l21['text']='IPv4:超时'
            alert('IPv4超时', 'IPv4检测超时，可能是由于您不在校园内网或服务器错误\n请检查您的网络环境或尝试登陆')
            return 4
        l21['text']='IPv4:已登录'
        alert('此IP已登录','此IP已被：'+ipv4status['user']+'登录，若非自己请先单击注销')
        print('此IP已被 ：'+ipv4status['user']+'登录')
    else:
        rst1=a.keepOnlineIPv4()
        if rst1=='e':
            l21['text']='IPv4:未启用'
        elif rst1=='off':
            l21['text']='IPv4:已离线'
        else:
            l21['text']='IPv4:无需认证'
    rst2=a.keepOnlineIPv6()
    if rst2==0:
        l22['text']='IPv6:已登录'
    elif rst2=='off':
        l22['text']="IPv6:未登录"
    elif rst2=='notsupport':
        l22['text']='IPv6:未启用'
        C4.deselect()
        C4['state']='disabled'
    else :
        l22['text']="IPv6:不可用"
        C4.deselect()
        C4['state']='disabled'
    
def updateinfo():
    t=28
    time1=int(time.time())
    while(True):
        if(event.isSet()):
            time.sleep(1)
            t+=1
            if(t % 1 ==0):
                t2=int(time.time())-time1+57600
                timeStr = time.strftime('%H:%M:%S', time.localtime(t2))
                l3['text']=timeStr+'.'+str(t)
            if(t % 30 ==29):
                ipv4status=a.getKeeplive()
                #print(ipv4status)
                if ipv4status!=0:
                    if int(ipv4status['avaliable'])==0:
                        l1['text']='不限制'
                    else:
                        if(int(ipv4status['avaliable'])<1000000000):
                            l1['text']=str(round(int(ipv4status['avaliable'])/1000000,2))+'MB'
                        else:
                            l1['text']=str(round(int(ipv4status['avaliable'])/1000000000,2))+'GB'
                else:
                    l1['text']='IPv4未登录'
                t=0
                    
        else:
            print('exit!')
            break

def keepOnlineIPv4():
    t=0
    while(True):
        if(event.isSet()):
            time.sleep(1)
            t+=1
            if(t % 60==0):
                print('keepAliveIPv4')
                username=a.show('system','last')
                uid=a.show(username, 'uid')
                a.sendHeartbeatPacket(uid)
            if(t==600):
                print('keepOnlineIPv4')
                rst1=a.keepOnlineIPv4()
                t=0
        else:
            print('exit!')
            break
def keepOnlineIPv6():
    t=0
    while(True):
        if(event.isSet()):
            time.sleep(1)
            t+=1
            if(t>=60):
                print('keepOnlineIPv6')
                rst2=a.keepOnlineIPv6()
                t=0
        else:
            print('exit!')
            break
        
def login():
    if(event.isSet()):
        print('无效操作')
        return 1;
    print('登陆')
    username=user.get()
    if len(username)<1:
        alert('缺少用户名','请输入用户名')
        return 1
    password=pwd.get()
    if len(password)<1:
        alert('缺少密码','请输入密码')
        return 1
    #print(CheckVar1.get())
    if not(CheckVar3.get() or CheckVar4.get()):
        alert('缺失必要参数','IPv4,IPv6中至少一项应被选中')
        return 1
    rst=str(a.login(username, password))
    if re.match(r"\d{3}",rst[:3]):
        print('登陆成功')
    else :
        print('登录失败')
        alert('登陆失败',rst)
        if rst=='您的IP尚未下线，请强制该IP下线':
            a.do_logout()
            print('等待注销')
            time.sleep(5)
            login()
        if rst=='该帐号的登录人数已超过限额':
            a.force_logout(username, password)
            print('等待状态同步后重试')
            time.sleep(10)
            login()
        return 3

    if CheckVar1.get()==1:
        a.update(username, 'password', password)
    if rst:
        threads = []
        t1 = threading.Thread(target=keeplive)
        t2 = threading.Thread(target=updateinfo)
        threads.append(t1)
        threads.append(t2)
        if CheckVar3.get():
            t3 = threading.Thread(target=keepOnlineIPv4)
            threads.append(t3)
        if CheckVar4.get():
            t4 = threading.Thread(target=keepOnlineIPv6)
            threads.append(t4)
        event.set()   
        for t in threads:
            t.setDaemon(True)
            t.start()
    btn1['state']=DISABLED
    l21['text']='IPv4:已登录'
    a.update('system','rememberpwd',str(CheckVar1.get()))
    a.update('system','autologin',str(CheckVar2.get()))
    a.update('system','ipv4',str(CheckVar3.get()))
    a.update('system','ipv6',str(CheckVar4.get()))

def logout():
    print('logout')
    username=user.get()
    if len(username)<1:
        alert('缺少用户名','请输入用户名')
        return 1
    password=pwd.get()
    if len(password)<1:
        alert('缺少密码','请输入密码')
        return 1
    event.clear()
    btn1['state']=NORMAL
    l4['text']='logout'
    a.uid_logout()
    a.uid_logout6()
    
    l21['text']='IPv4:已注销'
def logoutip():
    a.do_logout()
    a.do_logout6()
    event.clear()
    btn1['state']=NORMAL
    l4['text']='logout'
    l21['text']='IPv4:已注销'
def logoutuser():
    username=user.get()
    if len(username)<1:
        alert('缺少用户名','请输入用户名')
        return 1
    password=pwd.get()
    if len(password)<1:
        alert('缺少密码','请输入密码')
        return 1
    event.clear()
    btn1['state']=NORMAL
    l4['text']='logout user'
    a.force_logout(username, password)
    a.force_logout6(username, password)
    l21['text']='IPv4:已注销'

root = Tk()
root.title('Zins')
root.geometry('350x500')
root.resizable(0, 0)
root.iconbitmap('.//ico//ico_64X64.ico')   
menu(root)    
#UI
filename = r".//ico//zinsb.gif"
img = PhotoImage(file=filename)
label = Label(root, text="titleimg",width=350,height=100,image=img).grid(row=0,columnspan=6,sticky=W)

Canvas(root,width=350,height=10).grid(row=1,columnspan=6,sticky=W)
 
val1=StringVar()
val2=StringVar()   
Label(root,text='用户名:').grid(row=2,column=0,columnspan=2)
user=Entry(root,textvariable=val1)
user.grid(row=2,column=2,columnspan=4)
Label(root,text='密    码:').grid(row=3,column=0,columnspan=2)
pwd=Entry(root,textvariable=val2)
pwd['show']='*'
pwd.grid(row=3,column=2,columnspan=4)

Canvas(root,width=350,height=10).grid(row=4,columnspan=6,sticky=W)

CheckVar1 = IntVar()
CheckVar2 = IntVar()
CheckVar3 = IntVar()
CheckVar4 = IntVar()
C1 = Checkbutton(root, text = "记住密码", variable = CheckVar1, \
                 onvalue = 1, offvalue = 0, height=1, \
                 width = 20)
C2 = Checkbutton(root, text = "自动登录", variable = CheckVar2, \
                 onvalue = 1, offvalue = 0, height=1, \
                 width = 20)
C3 = Checkbutton(root, text = "登陆IPV4", variable = CheckVar3, \
                 onvalue = 1, offvalue = 0, height=1, \
                 width = 20)
C4 = Checkbutton(root, text = "登陆IPV6", variable = CheckVar4, \
                 onvalue = 1, offvalue = 0, height=1, \
                 width = 20)
C1.grid(row=5,column=0,columnspan=3,sticky=W)
C2.grid(row=5,column=3,columnspan=3,sticky=W)
C3.grid(row=6,column=0,columnspan=3,sticky=W)
C4.grid(row=6,column=3,columnspan=3,sticky=W)

Canvas(root,width=350,height=10).grid(row=4,columnspan=7,sticky=W)

btn1=Button(root,text='登陆',width=8,command=login)
btn1.grid(row=8,column=1)
btn2=Button(root,text='注销',width=8,command=logout)
btn2.grid(row=8,column=2)
btn3=Button(root,text='IP注销',width=8,command=logoutip)
btn3.grid(row=8,column=3)
btn4=Button(root,text='用户注销',width=8,command=logoutuser)
btn4.grid(row=8,column=4)
Canvas(root,width=15,height=10).grid(row=8,column=5)

Canvas(root,width=350,height=15).grid(row=9,columnspan=7,sticky=W)

cv = Canvas(root)
cv.create_rectangle(10,10,340,160,outline = 'gray')
cv.create_line(10,60,340,60,arrow='none',fill='gray',dash=10)
cv.create_line(10,110,340,110,arrow='none',fill='gray',dash=10)
cv.grid(row=10,rowspan=6,columnspan=6)

Label(root, text="剩余流量：", fg="black").grid(row=10,column=1)
l1=Label(root, text="NaN", fg="black")
l1.grid(row=10,column=3)
Label(root, text="登陆状态：", fg="black").grid(row=11,column=1)
l21=Label(root, text="IPv4：NaN", fg="black")
l21.grid(row=11,column=2)
l22=Label(root, text="IPv6：NaN", fg="black")
l22.grid(row=11,column=3)
#已连接，已断开，未连接，未启用，意外离线
Label(root, text="登陆时长：", fg="black").grid(row=12,column=1)
l3=Label(root, text="NaN", fg="black")
l3.grid(row=12,column=3)
    
l4=Label(root, text="Zins测试版", fg="black")
l4.grid(row=13,column=2,columnspan=2)
#UI END

init()
root.mainloop()
