# -*- coding: utf-8 -*-
from mainclass import *
import sys,getopt
from configparser import NoSectionError
from _csv import Error

a=Zins()
#b=userData()
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
    print("--logout")
    print("--logoutuser")
    print("--logoutip")
    print("--info")
    
def Version():
    print("ZINS v0.9 Preview for Developers Commandline Only. Suit but not only suit for CUGB")

def login(user,password=0):
    #print('login!')
    #print(user)
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
    a.login(str(user), str(password))
def logout():
    print('logout')
    rst=a.uid_logout()
    
def logoutip():
    a.do_logout()
    
def logoutuser(user,password):
    a.force_logout(user, password)


try:
    options,args=getopt.getopt(sys.argv[1:],"hvu:p:r", ["help","username=","password=","logout","logoutip","logoutuser","version"])
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
    if name in ("--logout"):
        logout();
    if name in ("--logoutip"):
        logoutip()
    if name in ("--logoutuser"):
        function = 'logoutuser'
    if name in ("-r"):
        if username and password:
            a.update(username, 'password', password)
            print('r')
        else :
            print('Missing username or password,"-r" will be ignore')

if function == 'logoutip':
    print('logoutip')
elif function == 'logoutuser':
    if username and password:
        print('logoutuser')
        logoutuser(username, password)
        sys.exit(3)
    else:
        print('Missing Parameters! Please use "--logoutuser" wieht "--username" and "--password"')
        sys.exit(3)
    
login(username,password)