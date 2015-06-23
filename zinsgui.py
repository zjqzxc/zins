# -*- coding: utf-8 -*-
from mainclass import *
from tkinter import *
import tkinter.messagebox,threading
from tkinter.constants import *

a=Zins()
b=userData()
event=threading.Event()

__author__ = {'name' : 'Flagplus',
              'Email' : 'zjqzxc@flagplus.net',
              'Created' : '2015-02-19'}
def Version():
    filewin = Toplevel()
    tmpcnf = '%dx%d'%(350, 150)
    filewin.geometry(tmpcnf)
    filewin.title('版本')
    txt='\
Zins登陆器（女生版）测试版\n\
    V 1.0。0 Alpha\n\
如果距离编译时间过久，请前往http://zins.flagplue.net查找更新\n\
有任何问题，请描述问题并截图后发邮件至i@flagplus.net\n\
编译日期2015-02\
         '
    Label(filewin,text=txt).pack()
    button = Button(filewin, text='我会记得更新的',command=filewin.destroy)
    button.pack(side=BOTTOM)
def Help():
    filewin = Toplevel()
    tmpcnf = '%dx%d'%(350, 150)
    filewin.geometry(tmpcnf)
    filewin.title('帮助')
    txt='\
Zins登陆器（女生版）简易使用帮助\n\
输入用户名和密码，然后“登陆”就可以了。\n\
什么“在线人数已达上限”“IP已存在”，都交给Zins就可以啦~\n\
使用前请保证打开任意网页可以跳转到网关登陆页面^_^\n\
编译日期2015-02\
         '
    Label(filewin,text=txt).pack()
    button = Button(filewin, text='本宫知道了',command=filewin.destroy)
    button.pack(side=BOTTOM)
def About():
    filewin = Toplevel()
    tmpcnf = '%dx%d'%(350, 200)
    filewin.geometry(tmpcnf)
    filewin.title('关于')
    txt='\
关于Zins\n\
Zins是一款用于深澜公司网关登陆的跨平台非官方登录工具,\n\
详情请参阅http://zins.flagplus.net，并获得更新。\n\
网页版登陆器请访问http://gate.cugbteam.org(仅校内)\n\
开发者\n\
算法院子网路破\n\
部分核心代码@怡红公子\n\
@Flagplus进行功能完善及GUI编写\
         '
    Label(filewin,text=txt).pack()
    button = Button(filewin, text='都退下吧',command=filewin.destroy)
    button.pack(side=BOTTOM)
def alert(txt1,txt2):
    filewin = Toplevel()
    tmpcnf = '%dx%d'%(350, 150)
    filewin.geometry(tmpcnf)
    filewin.title(txt1)
    Label(filewin,text=txt2).pack()
    button = Button(filewin, text='确认',command=filewin.destroy)
    button.pack(side=BOTTOM)


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
        b.update(username, 'password', password)
    btn1['state']=DISABLED 

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
    l1['text']='logout'
    a.do_logout()    

root = Tk()
root.title('Zins')
root.geometry('350x500')
root.resizable(0, 0)
root.iconbitmap('.//ico//ico_64X64.ico')     
#UI
filename = r".//ico//zinsg.gif"
img = PhotoImage(file=filename)
#Canvas(root,bg='red',width=350,height=100).grid(row=0,columnspan=6,sticky=W)
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
                 width = 20, state=DISABLED)

C1.grid(row=5,column=0,columnspan=3,sticky=W)
C2.grid(row=5,column=3,columnspan=3,sticky=W)
C3.grid(row=6,column=0,columnspan=3,sticky=W)
C4.grid(row=6,column=3,columnspan=3,sticky=W)

Canvas(root,width=350,height=10).grid(row=4,columnspan=7,sticky=W)

btn1=Button(root,text='登陆',width=10,command=login)
btn1.grid(row=8,column=0,columnspan=3)
btn2=Button(root,text='注销',width=10,command=logout)
btn2.grid(row=8,column=3,columnspan=3)

Canvas(root,width=350,height=15).grid(row=9,columnspan=7,sticky=W)

cv = Canvas(root)
cv.create_rectangle(10,10,340,160,outline = 'gray')
cv.create_line(10,60,340,60,arrow='none',fill='gray',dash=10)
cv.create_line(10,110,340,110,arrow='none',fill='gray',dash=10)
cv.grid(row=10,rowspan=6,columnspan=6)
    
Label(root, text="剩余流量：", fg="black").grid(row=10,column=1)
l1=Label(root, text="NaN", fg="red")
l1.grid(row=10,column=3)
Label(root, text="登陆状态：", fg="black").grid(row=11,column=1)
l21=Label(root, text="IPv4：NaN", fg="red")
l21.grid(row=11,column=2)
l22=Label(root, text="IPv6：NaN", fg="red")
l22.grid(row=11,column=3)
#已连接，已断开，未连接，未启用，意外离线
Label(root, text="登陆时长：", fg="black").grid(row=12,column=1)
l3=Label(root, text="NaN", fg="black")
l3.grid(row=12,column=3)
    
l4=Label(root, text="Zins测试版", fg="black")
l4.grid(row=13,column=2)

#UI END

#init()
root.mainloop()