from tkinter import *

top = Tk()

L1 = Label(top, text="User Name")
L1.pack( side = LEFT)
E1 = Entry(top, bd =5)
E1.pack(side = RIGHT)

def a():
    print()
    
w=Button(top,text='btn',command=a,fg='#123456',bg='a.jpg')
w.pack(side= LEFT)

top.mainloop()