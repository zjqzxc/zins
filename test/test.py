from tkinter import *
import time,threading

def func():
    t=0
    while(True):
        if(event.isSet()):
            time.sleep(0.5)
            t+=1
            if(t>1):
                print(int(time.time()))
                t=0
        else:
            print('exit!')
            break
def sta():
    threads = []
    t1 = threading.Thread(target=func)
    threads.append(t1)
    event.set()   
    for t in threads:
        t.setDaemon(True)
        t.start()

def sto():
    print('stop')
    event.clear()

event=threading.Event()
flag=0

    
root=Tk()
Button(root,text='start',command=sta).pack()
Button(root,text='stop',command=sto).pack()
root.mainloop()
