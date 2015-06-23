import math

def encrypt( password, time ):
    key = str( math.floor( time ) / 60 )
    ret = ""
    for i in range( len(password[:16]) ):
        k = ord( key[ len(key) - i % len(key) - 1 ] ) ^ ord( password[i] )
        l = chr( (k & 0x0f) + 0x36 )
        h = chr( ((k >> 4) & 0x0f) + 0x63 )
        ret += h+l if i%2 else l+h
    return ret

print( encrypt("235698765", 123456789) )
