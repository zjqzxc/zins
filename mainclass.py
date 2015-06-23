# -*- coding: utf-8 -*-
#from socket import *
from userdata import *
import math, urllib.request, urllib.parse,time,re,os
import struct, traceback,binascii,socket,configparser

class Zins:
    def __init__( self ):#设置常用变量
        if os.path.exists('config1.ini'):
            print('use config.ini settings')
        else :
            print('config.ini not found!Try to use default settings.')
            self.host='202.204.105.195'
            self.host6='[2001:da8:214:102:d6be:d9ff:feaa:422a]'
            self.port='3333'
            self.keepliveport='3335'
            self.server=self.host+':'+self.port
            self.server6=self.host6
            self.loginurl='/cgi-bin/do_login'
            self.keepliveurl='/cgi-bin/keeplive'
            self.dologout='/cgi-bin/do_logout'
            self.forcelogout='/cgi-bin/force_logout'
        self.userdata=userData()
    
    def update(self,section,key,value):#配置文件更新操作,由userdata.py提供
        return self.userdata.update(section, key, value)
    
    def show(self,section,key):#配置文件读取,由userdata.py提供
        return self.userdata.show(section, key)
    def checkfile(self):#配置文件完整性检查，由userdata.py提供
        return self.userdata.checkfile()

    def usage(self):#还没来及认真写，其实也没啥用
        print('About Zins')
        print('登陆IPv4：login（用户名，密码）')
        print('登陆IPv6：login6（用户名，密码）')
        print('注销：do_logout()')
        print('详情请参阅说明文档')
        
        
    def encrypt( self, password, time ):#密码加密处理（算法源自网络）
        key = str( math.floor( time / 60 ) )
        ret = ""
        for i in range( len(password[:16]) ):
            k = ord( key[ len(key) - i % len(key) - 1 ] ) ^ ord( password[i] )
            l = chr( (k & 0x0f) + 0x36 )
            h = chr( ((k >> 4) & 0x0f) + 0x63 )
            ret += h+l if i%2 else l+h
        return ret
    def post( self, url, data = {}):#将数据post至服务器
        params = urllib.parse.urlencode( data )
        request = urllib.request.Request( url, data = params.encode("utf-8") )
        try :
            response = urllib.request.urlopen( request ,timeout=3)
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.timeout):
                print('timeout')
                return 'timeout'
        return response.read().decode("utf-8")
    
    def relogin(self, username, password, pwdstr, protocol = 'ipv4'):#使用系统返回的时间戳加密密码并登陆
        if protocol=='ipv6':
            self.type=self.userdata.show('system', 'type6')
            serverUrl='http://'+self.server6+self.loginurl
        else:
            self.type=self.userdata.show('system', 'type')
            serverUrl='http://'+self.server+self.loginurl
        data = {
    "username": username,
     "password": self.encrypt( password, float(pwdstr.split("@")[1]) ),
     "drop": 0,
     "type": self.type,
     "n": 117,
     "pop": 0,
     "ac_type": "h3c",
     "mac": ""
    }
        #print(self.type)
        timeoffset=int(pwdstr.split("@")[1])-int(time.time())
        self.userdata.update('system','timeoffset',str(timeoffset))
        return self.post(serverUrl, data)
    
    def trylogin(self, username, password, protocol = 'ipv4'):#使用系统时间作为时间戳加密密码并尝试登陆
        if protocol=='ipv6':
            self.type=self.userdata.show('system', 'type6')
            serverUrl='http://'+self.server6+self.loginurl
            serverTime=int(self.userdata.show('system', 'timeoffset6'))+int(time.time())
        else:
            self.type=self.userdata.show('system', 'type')
            serverUrl='http://'+self.server+self.loginurl
            serverTime=int(self.userdata.show('system', 'timeoffset'))+int(time.time())
        if self.type=='1':
            data={
    "username": username,
    "password": password,
    "drop": 0,
    "is_pad":1,
    "type": self.type,
    "n": 117,
    "pop": 0,
    "ac_type": "h3c",
    "mac": ""
    }
        else:
            data={
    "username": username,
    "password": self.encrypt( password, serverTime),
    "drop": 0,
    "type": self.type,
    "n": 117,
    "pop": 0,
    "ac_type": "h3c",
    "mac": ""
    }
        #print(self.type)
        return self.post(serverUrl, data)
    
    def force_logout(self, username, password, protocol = 'ipv4'): #logout by user
        data = {
        "username": username,
        "password": password,
        }
        if protocol=='ipv6':
            url='http://'+self.server6+self.forcelogout
        else:
            url='http://'+self.server+self.forcelogout
        str1=self.post(url,data)
        return str1
    
    def do_logout(self, protocol = 'ipv4'): #logout by ip
        if protocol=='ipv6':
            url='http://'+self.server6+self.dologout
        else:
            url='http://'+self.server+self.dologout
        response = urllib.request.urlopen( url )
        return response.read().decode("utf-8")
    
    def uid_logout(self, uid = 0, protocol = 'ipv4'):#logout by uid
        if uid==0:
            lastuser=self.userdata.show('system', 'last')
            try:
                if protocol=='ipv6':
                    uid=self.userdata.show(lastuser,'uid6')
                else:
                    uid=self.userdata.show(lastuser,'uid')
            except configparser.NoSectionError:
                print('uid not available')
                return 1
            except configparser.NoOptionError:
                print('uid not found')
                return 2
        data = {"UID": uid}
        #print(data)
        if protocol=='ipv6':
            url='http://'+self.server6+self.dologout
        else:
            url='http://'+self.server+self.dologout
        str1=self.post(url,data)
        return str1
        
    def getKeeplive(self, protocol = 'ipv4'):  #获取keeplive脚本的返回值
        #url="http://202.204.105.195:3333/cgi-bin/keeplive"
        url='http://'+self.server+self.keepliveurl
        print(url)
        try:
            response = urllib.request.urlopen( url ,timeout=3)
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.timeout):
                print('timeout')
                return 'timeout'
        try:
            str1=response.read().decode("utf-8")
        except :
            print('Network Connection Failure')
            return 'networkfailure'
        if str1=='error':
            return 0
        str2=str1.split(",")
        info={
              "time":str2[0],
              "rx":str2[1],
              "tx":str2[2],
              "avaliable":str2[3],
              "used":str2[4],
              "timeUsed":str2[5],
              "timeAvaliable":str2[6],
              "user":str2[7]
              }
        return info
    
    def getSpeed(self, protocol = 'ipv4'):#获取keeplive脚本的返回值两次，间隔一秒，用于计算实时网速
        #url="http://202.204.105.195:3333/cgi-bin/keeplive"
        url='http://'+self.server+self.keepliveurl
        response = urllib.request.urlopen( url )
        str1=response.read().decode("utf-8")
        if str1=='error':
            return 0
        str2=str1.split(",")
        time.sleep(1)
        response = urllib.request.urlopen( url )
        str3=response.read().decode("utf-8")
        str4=str3.split(",")
        rx=int(str4[1])-int(str2[1])
        tx=int(str4[2])-int(str2[2])
        speed={
              "rxspeed":rx,
              "txspeed":tx,
              "time":str2[0],
              "rx":str2[1],
              "tx":str2[2],
              "avaliable":str2[3],
              "used":str2[4],
              "timeUsed":str2[5],
              "timeAvaliable":str2[6],
              "user":str2[7]
              }
        return speed
    
    def CheckError(self,errorstr):#将服务器返回的错误信息翻译成人能理解的语言
        if re.match(r"password_error",errorstr):
            return '密码错误'
        else:
            dict1={
                "user_tab_error":"认证程序未启动",
                "username_error":"用户名错误",
                "non_auth_error":"您无须认证，可直接上网",
                "password_error":"密码错误",
                "status_error":"用户已欠费，请尽快充值",
                "available_error":"用户已禁用",
                "ip_exist_error":"您的IP尚未下线，请强制该IP下线",
                "usernum_error":"用户数已达上限",
                "online_num_error":"该帐号的登录人数已超过限额",
                "mode_error":"系统已禁止WEB方式登录，请更改配置文件中type值",
                "time_policy_error":"当前时段不允许连接",
                "flux_error":"您的流量已超支",
                "minutes_error":"您的时长已超支",
                "ip_error":"您的IP地址不合法",
                "mac_error":"您的MAC地址不合法",
                "sync_error":"您的资料已修改，正在等待同步，请2分钟后再试",
                "timeout":"Socket超时，请检查网络连接",
                "帐号的在线人数已达上限。":"帐号的在线人数已达上限。"
                }
            return dict1[errorstr]
    
    def sendHeartbeatPacket(self,flag=1, protocol = 'ipv4'): #发送心跳包
        HOST = self.host
        PORT = int(self.keepliveport)
        BUFSIZ = 128
        ADDR=(HOST,PORT)
        
        user=self.userdata.show('system', 'last')
        uid=self.userdata.show(user, 'uid')
        hexuid=hex(int(uid))[2:]
        hexuid='0000'+hexuid
        l=len(hexuid)
        data=''
        while (l>0):
            s=hexuid[l-8:l]
            l=l-8
            data+=s+'.'
        data=data.split('.')
        data.pop()
        #print(data)
        str=struct.pack("ii",int(data[0],16),int(data[1],16))
        #print(str)
        str2=struct.pack("14i",int(data[0],16),int(data[1],16),
                 int('0000',16),int('0000',16),int('0000',16),int('0000',16),
                 int('0000',16),int('0000',16),int('0000',16),int('0000',16),
                 int('0000',16),int('0000',16),int('0000',16),int('0000',16))
        udpsend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if flag:
            udpsend.sendto(str2, ADDR)
        else:
            udpsend.sendto(str, ADDR)
        udpsend.settimeout(5)
        try:
            data, ADDR = udpsend.recvfrom(BUFSIZ)
            return data
        except socket.error:
            print('Recv time out!')
        if not data:
            print('get Null!')
        udpsend.close()
    
#    def keepOnline(self): #持续不断的执行发送心跳包操作
#        while True: 
#            rst=self.sendHeartbeatPacket()
#            print(rst)
#            time.sleep(60)
    
    def checkOnline(self, protocol = 'ipv4'): #检查账户登录状态及网络状态
        if protocol == 'ipv6':
            url='http://ipv6.baidu.com'
        else:
            url='http://www.baidu.com'

        try:
            response = urllib.request.urlopen( url )
        except:
            return 'e'
        try:
            rst=response.read().decode("utf-8")
        except:
            return 'notsupport'
        if rst.find(self.host6)==-1:
            return 0
        else:
            return 'off'
        
    def checkNetConnect(self): #测试网关的可到达性，用于判断网络物理连接是否正常
        url='http://'+self.host
        try:
            response = urllib.request.urlopen( url )
        except:
            return 'e'
        return response.read().decode("utf-8")
        
    def login(self,username,password):#封装后的登陆IPv4的函数
        self.userdata.checkfile()
        self.userdata.checksys()
        self.userdata.checkuser(username)
        
        rs=self.trylogin(username, password, 'ipv4')
        #print(rs)
        if re.match(r"\d{3}",rs[:3]):
            print('loginok!')
            self.userdata.update('system','last',username)
            uid=rs.split(',')[0]
            self.userdata.update(username, 'uid', str(uid))
            self.userdata.update(username,'logintime', str(int(time.time())))
            count=int(self.userdata.show(username, 'logincount'))+1
            self.userdata.update(username, 'logincount' ,str(count))
            self.sendHeartbeatPacket(0)
            self.sendHeartbeatPacket()
            time.sleep(1)
            return rs
        elif re.match(r"password_error",rs):
            rs = self.relogin(username,password,rs)
            if re.match(r"\d{3}",rs[:3]):
                print('reloginok!')
                self.userdata.update('system','last',username)
                uid=rs.split(',')[0]
                self.userdata.update(username, 'uid', str(uid))
                self.userdata.update(username,'logintime', str(int(time.time())))
                count=int(self.userdata.show(username, 'logincount'))+1
                self.userdata.update(username, 'logincount' ,str(count))
                self.sendHeartbeatPacket(0)
                self.sendHeartbeatPacket()
                return rs
            else:
                return self.CheckError(rs)            
        else:
            return self.CheckError(rs)
        
    def login6(self,username,password):#封装后的登陆IPv6的函数
        self.userdata.checkfile()
        self.userdata.checksys()
        self.userdata.checkuser(username)
        
        rs=self.trylogin(username, password, 'ipv6')
        print(rs)
        if re.match(r"\d{3}",rs[:3]):
            print('loginok!')
            self.userdata.update('system','last',username)
            uid=rs.split(',')[0]
            self.userdata.update(username, 'uid6', str(uid))
            count=int(self.userdata.show(username, 'logincount6'))+1
            self.userdata.update(username, 'logincount6' ,str(count))
            #self.sendHeartbeatPacket(0)
            #self.sendHeartbeatPacket()
            time.sleep(1)
        elif re.match(r"password_error",rs):
            rs = self.relogin(username, password, rs, 'ipv6')
            if re.match(r"\d{3}",rs[:3]):
                print('reloginok!')
                self.userdata.update('system','last',username)
                uid=rs.split(',')[0]
                self.userdata.update(username, 'uid6', str(uid))
                count=int(self.userdata.show(username, 'logincount6'))+1
                self.userdata.update(username, 'logincount6' ,str(count))
                #self.sendHeartbeatPacket(0)
                #self.sendHeartbeatPacket()
            else:
                return self.CheckError(rs)
        elif rs.find("登录成功"):
            print('备用模式登陆成功')
            self.userdata.update('system','last',username)
            uid='0'
            self.userdata.update(username, 'uid6', str(uid))
            count=int(self.userdata.show(username, 'logincount6'))+1
            self.userdata.update(username, 'logincount6' ,str(count))
            return 0        
        else:
            return self.CheckError(rs)
        