# -*- coding: utf-8 -*-
from mainclass import *
import sys,getopt
from configparser import NoSectionError

a=Zins()
#print(len(sys.argv))
#print(sys.argv)

def Usage():
    print("Welcom to use ZINS! You can use it to login if your system is srun.")
    print("")
    print("Usage: zins.exe [-u username] [-p password] [options]")
    print("OR:python zins.py [-u username] [-p password] [options]")
    print("")
    print("Options are:")
    print("-u,--username:  the username you want to use")
    print("-p,--password:  the password of the username")
    print("-h,--help:      print this message")
    print("-v,--version:   print the version")
    print("-r:             remember the password.If you use this option at once ,you can only use '-u username' to login next time.")
    print("-4:             IPv4 Only。")
    print("-6:             IPv6 Only.")
    print("                If either -4 or -6 exist ,we will login/logout with both of them.")
    print("--logoutuid     logout with uid if uid exist")
    print("--logoutuser    logout with username and password,username and password is needed")
    print("--logoutip      logout with ip")
    print("--info          show information")
    
def Version():
    print("ZINS v1.13 Alpha Preview for Developers Commandline Only. Suit but not only suit for CUGB")

def login(user, password=0, type='ipv4'):
    if password=='0':
        try:
            password=a.show(user, 'password')
        except configparser.NoSectionError:
            print('UserData not found!，Please use username and password login')
            sys.exit(4)
        if password=='0':
            print('This user not allow to remember the password!')
            sys.exit(4)
        else:
            print(user)
            print(password)
    else:
        print(user)
        print(password)
    
    if type=='ipv6':
        a.login6(str(user), str(password))
    else:
        a.login(str(user), str(password))
    
    
def logout(type4,type6):
    print('logout by uid')
    if type4:
        a.uid_logout(0, 'ipv4')
    if type6:
        a.uid_logout(0, 'ipv6')
    if not type4 and not type6:
        a.uid_logout(0, 'ipv4')
        
def logoutip(type4,type6):
    print('logout by ip')
    if type4:
        a.do_logout('ipv4')
    if type6:
        a.do_logout('ipv6')
    if not type4 and not type6:
        a.do_logout('ipv4')
        a.do_logout('ipv6')
    
def logoutuser(user, password, type4, type6):
    print('logout by username')
    if type4:
        a.force_logout(user, password, 'ipv4')
    if type6:
        a.force_logout(user, password, 'ipv6')
    if not type4 and not type6:
        a.force_logout(user, password, 'ipv4')
        a.force_logout(user, password, 'ipv6')

def info():
    arr=a.getSpeed("ipv4")
    txs='发送：'+str(arr['txspeed']/1000)+'KB/s'+'\n'
    rxs='接收：'+str(arr['rxspeed']/1000)+'KB/s'+'\n'
    timeshow='登陆时间：'+str(arr['time'])+'秒\n'
    avaliabe='可用流量：'+str(arr['avaliable'])+'(0为不限制)\n'
    used='已用流量：'+str(int(arr['used'])/1000000)+'MB \n'
    usershow='当前登陆：'+str(arr['user'])+'\n'
    conninfo=txs+rxs+timeshow+avaliabe+used+usershow
    print(conninfo)

try:
    options,args=getopt.getopt(sys.argv[1:],"hvu:p:r46", ["help","username=","password=","logoutuid","logoutip","logoutuser","version","info"])
    if not options :
        try:
            user=a.show('system','last')
        except configparser.NoSectionError:
            print('Please try to login with username and password')
            Usage()
            sys.exit()
        try:
            password=a.show(user,'password') 
        except NoSectionError:
            print('Please try to login with username and password')
            Usage()
            sys.exit(3)
        if password=='0':
            print('The last user NOT allow remembering password,AutoLogin fail!')
            print('Please try to login with username and password')
            Usage()
            sys.exit(3)
        else:
            login(user,password)
            sys.exit(0)
except getopt.GetoptError:
    Usage()
 
type4=0
type6=0
function = ''
username = ''
password = '0'
for name,value in options:
    if name in ("--help","-h"):
        Usage()
        sys.exit(2)
    if name in ("-v","--version"):
        Version()
        sys.exit(2)
    if name in ("-u","--username"):
        username=value
    if name in ("-p","--password"):
        password=value
    if name in ("-4"):
        type4=1
    if name in ("-6"):
        type6=1
    if name in ("--logoutuid"):
        function = 'logoutuid'
    if name in ("--logoutip"):
        function = 'logoutip'
    if name in ("--logoutuser"):
        function = 'logoutuser'
    if name in ("--info"):
        function = 'info'
        info()
    if name in ("-r"):
        if username and password:
            a.update(username, 'password', password)
            print('r')
        else :
            print('Missing username or password,"-r" will be ignore')

if function == 'logoutuid':
    logout(type4,type6)
    sys.exit(3)
elif function == 'logoutip':
    logoutip(type4,type6)
elif function == 'logoutuser':
    if username and password:
        print('logoutuser')
        logoutuser(username, password,type4,type6)
        sys.exit(3)
    else:
        print('Missing Parameters! Please use "--logoutuser" with "--username" and "--password"')
        sys.exit(3)
        
if type4:
    login(username,password,'ipv4')
if type6:
    login(username,password,'ipv6')
if not type4 and not type6 and not function:
    print('Try login IPv4 and IPv6 .If you only want to login one of them ,please use "-4" or "-6" ')
    login(username,password,'ipv4')
    login(username,password,'ipv6')