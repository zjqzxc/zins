import platform,configparser,os,socket

class userData:
    def __init__( self ):
        self.filename="user.dat"
        self.userconfig = configparser.ConfigParser()
        self.userconfig.read(self.filename)        
        self.hostName=socket.gethostname()
        self.localIP = socket.gethostbyname(self.hostName)
        self.localUserName=os.getlogin()
    def get_mac_address(self):
        import uuid
        node = uuid.getnode()
        mac = uuid.UUID(int = node).hex[-12:]
        return mac
    def reset_userdat(self,filename):
        self.userconfig.add_section('system')
        self.userconfig.set('system','hostname',self.hostName)
        self.userconfig.set('system','localUserName',self.localUserName)
        self.userconfig.set('system','localIP',self.localIP)
        self.userconfig.set('system','macAddress',self.get_mac_address())
        self.userconfig.set('system','type','10')
        self.userconfig.set('system','type6','10')
        self.userconfig.set('system','timeoffset','0')
        self.userconfig.set('system','timeoffset6','0')
        self.userconfig.set('system','last','0')
        self.userconfig.set('system','rememberpwd','0')
        self.userconfig.set('system','autologin','0')
        self.userconfig.set('system','ipv4','0')
        self.userconfig.set('system','ipv6','0')
        self.userconfig.write(open(filename,"w"))
    
    def add_user_section(self,filename,user):
        self.userconfig.add_section(user)
        self.userconfig.set(user,'uid','0')
        self.userconfig.set(user,'uid6','0')
        self.userconfig.set(user,'password','0')
        self.userconfig.set(user,'logincount','0')
        self.userconfig.set(user,'logincount6','0')
        self.userconfig.set(user,'logintime','0')
        self.userconfig.write(open(filename,"w"))
        
    def init(self):
        print('initialise')
    def checkfile(self):
        print('Checking userdata file...')
        if self.userconfig.read(self.filename):
            try:
                self.userconfig.options('system')
                print('Pass')
            except configparser.NoSectionError :
                print('System Infomation Not Found,Try to reset to default.')
                fp=open((self.filename),'w')
                fp.truncate()
                fp.close()
                for sc in self.userconfig.sections():
                    self.userconfig.remove_section(sc)
                self.reset_userdat(self.filename)
                print('Done')
        else:
            print('Creat userdata file')
            self.reset_userdat(self.filename)
            print('Done')
    def checksys(self):
        print('Checking system...')
        count=0
        if self.hostName!=self.userconfig.get('system','hostname'):
            count+=1
        if self.localUserName!=self.userconfig.get('system','localUserName'):
            count+=1
        if self.localIP!=self.userconfig.get('system','localIP'):
            count+=1
        if self.get_mac_address()!=self.userconfig.get('system','macAddress'):
            count+=1
        if count >1 :
            print('Reset。。。')
            fp=open((self.filename),'w')
            fp.truncate()
            fp.close()
            for sc in self.userconfig.sections():
                self.userconfig.remove_section(sc)
            print(self.userconfig.sections())
            self.reset_userdat(self.filename)
            print('Done')  
        else:
            print('Pass')    
    def checkuser(self,user):
        print('Checking user')#若存在，则更新，若不存在，则创建
        try:
            self.userconfig.options(user)
            print('Pass')
        except configparser.NoSectionError :
            print('Add new user')
            self.add_user_section(self.filename, user)
            print('Done')
    def checkOption(self,section,key):
        try:
            self.userconfig.get(section,key)
        except configparser.NoOptionError:
            self.userconfig.set(section,key,'0')
            self.userconfig.write(open(self.filename,"w"))
        
    def update(self,section,key,value):
        self.userconfig.set(section,key,value)
        self.userconfig.write(open(self.filename,"w"))
    def show(self,section,key):
        return self.userconfig.get(section,key)        
    