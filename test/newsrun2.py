import math, urllib.request, urllib.parse,time
def login( username, password ):
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
    serverUrl = "http://202.204.105.195:3333/cgi-bin/do_login"
    data = {
        "username": username,
        "password": encrypt( password, time.time()+99),
        "drop": 0,
        "type": 10,
        "n": 117,
        "pop": 0,
        "ac_type": "h3c",
        "mac": ""
    }
    #ret = post( serverUrl, data )
    #data["password"] = encrypt( password, float(ret.split("@")[1]) )
    return post(serverUrl, data)
 
print (login("1009111230", "inter80x86"))
