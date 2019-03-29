from _O import *
from _X import *
import tkinter as tk
from tkinter import font

def Func1(x):
	global checker
	checker.destroy()
	if x == 1:
		GUI()
	if x == 2:
		GUI2()  
checker = tk.Tk()
font1=font.Font(size=36)
checker.title("Tic-Tac-Toe")
b=tk.Button(checker,height=4,width=6,text='Play as 1',font=font1)
b.config(command=lambda:Func1(2))
b.grid(row=0,column=0)


a=tk.Button(checker,height=4,width=6,text='Play as 2',font=font1)
a.config(command=lambda:Func1(1))
a.grid(row=0,column=1)
checker.mainloop()


#project lab Day 1 29th