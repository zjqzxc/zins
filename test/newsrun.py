import math, urllib.request, urllib.parse,time,re,time

def encrypt( password, time ):
    key = str( math.floor( time / 60 ) )
    ret = ""
    for i in range( len(password[:16]) ):
        k = ord( key[ len(key) - i % len(key) - 1 ] ) ^ ord( password[i] )
        l = chr( (k & 0x0f) + 0x36 )
        h = chr( ((k >> 4) & 0x0f) + 0x63 )
        ret += h+l if i%2 else l+h
    return ret
def post( url, data = {}):
    params = urllib.parse.urlencode( data )
    request = urllib.request.Request( url, data = params.encode("utf-8") )
    response = urllib.request.urlopen( request )
    return response.read().decode("utf-8")


def force_logout(username,password): #logout this user
    data = {
        "username": username,
        "password": password,
    }
    url="http://202.204.105.195:3333/cgi-bin/force_logout"
    str1=post(url,data)
    return str1

def do_logout(): #logout this ip
    url="http://202.204.105.195:3333/cgi-bin/do_logout"
    response = urllib.request.urlopen( url )
    return response.read().decode("utf-8")

def relogin( username, password,pwdstr ):
    serverUrl = "http://202.204.105.195:3333/cgi-bin/do_login"
    data = {
    "username": username,
     "password": encrypt( password, float(pwdstr.split("@")[1]) ),
     "drop": 0,
     "type": 10,
     "n": 117,
     "pop": 0,
     "ac_type": "h3c",
     "mac": ""
    }
    return post(serverUrl, data)

def login(username,password):
    serverUrl = "http://202.204.105.195:3333/cgi-bin/do_login"
    data = {
    "username": username,
    "password": encrypt( password, time.time()),
    "drop": 0,
    "type": 10,
    "n": 117,
    "pop": 0,
    "ac_type": "h3c",
    "mac": ""
    }
    str1=post(serverUrl, data)
    
    if re.match(r"\d{3}",str1[:3]):
        return str1
    elif re.match(r"password_error",str1):
        return relogin(username,password,str1)
    else:
        return str1
def keeplive():
    url="http://202.204.105.195:3333/cgi-bin/keeplive"
    response = urllib.request.urlopen( url )
    str1=response.read().decode("utf-8")
    str2=str1.split(",")
    time.sleep(1)
    response = urllib.request.urlopen( url )
    str3=response.read().decode("utf-8")
    str4=str3.split(",")
    info={
          "time":str2[0],
          "rx":str2[1],
          "tx":str2[2],
          "user":str2[7]
    }
    rx=int(str4[1])-int(str2[1])
    tx=int(str4[2])-int(str2[2])
    print(rx/1024,'KB/s')
    print(tx/1024,'KB/s')
    #print(info)
    return str1
#uid=24670292149586
#print (login("1009111230", "inter80x86"))
#print(do_logout())
#print(force_logout("1009111230", "inter80x86"))
print(keeplive())