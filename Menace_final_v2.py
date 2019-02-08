import pickle
import time
import random
import tkinter as tk
from tkinter import font
class GUI:
	def __init__(self):
		self.move_no=1

		self.obj_names=[]
		self.Temp_obj_list=[]
		try:
			with open('dict.pkl','rb') as file:
				self.Menace_obj_list=pickle.load(file)
		except:
			self.Menace_obj_list={}

		self.mv=3
		self.board=tk.Tk()
		self.board.title("Tic-Tac-Toe")
		self.buttons=[]
		self.font1=font.Font(size=36)
		for x in range(0,3):
			for y in range(0,3):
				b=tk.Button(self.board,height=2,width=6,text='',font=self.font1)
				b.config(command=lambda widget=b:self.on_click(widget))
				b.grid(row=x,column=y)
				b.position=(x,y)
				self.buttons.append(b)

		self.b1=tk.Button(self.board,height=1,width=6,text='Exit',font=self.font1)
		self.b1.config(command=lambda:self.Destroy())
		self.b1.grid(row=3,column=0)
		'''
		self.b2=tk.Button(self.board,height=1,width=6,text='Next',font=self.font1)
		self.b2.config(command=lambda:self.Runprog())
		self.b2.grid(row=3,column=2)
		
		self.win_button=tk.Button(self.board,height=2,width=6,text='M Win',font=self.font1)
		self.win_button.config(command=lambda:self.GUI_win())
		self.win_button.grid(row=0,column=3)

		self.win_button=tk.Button(self.board,height=2,width=6,text='M Draw',font=self.font1)
		self.win_button.config(command=lambda:self.GUI_draw())
		self.win_button.grid(row=1,column=3)

		self.win_button=tk.Button(self.board,height=2,width=6,text='M Loss',font=self.font1)
		self.win_button.config(command=lambda:self.GUI_loss())
		self.win_button.grid(row=2,column=3)
		'''
		self.reset_B=tk.Button(self.board,height=1,width=6,text='Reset',font=self.font1)
		self.reset_B.config(command=lambda:self.reset())
		self.reset_B.grid(row=3,column=1)
		self.Runprog()

		self.board.mainloop()
	def Invalid_Moves(self):
		invalid_m=[]
		for x in range(0,9):
			if self.buttons[x]["text"] == "X" or self.buttons[x]["text"]=="O":
				invalid_m.append(x)		
		return invalid_m
	def on_click(self,widget):
		r,c=widget.position
		convert=[[0,1,2],[3,4,5],[6,7,8]]
		num=convert[r][c]
		iv=self.Invalid_Moves()
		if num not in iv and self.mv%2!=1:
			self.buttons[num]["text"]="O"
			self.mv=3
			self.obj_names.append(str(num))
			check=self.Invalid_Moves()
			check2=[0,1,2,3,4,5,6,7,8]
			Check_if_Won=self.Has_Won()
			if check != check2 and Check_if_Won=="Continue":
				self.Runprog()
			if Check_if_Won=="O":
				self.GUI_loss()
			elif Check_if_Won=="X":
				self.GUI_win()
			elif Check_if_Won=="Draw":
				self.GUI_draw()

	def Menace_click(self,Menace_obj):
		click=Menace_obj.r_select()
		if click=="Draw":
			self.GUI_draw()
		else:
			invalid_m=self.Invalid_Moves()
			if click not in invalid_m and self.mv%2!=0:
				self.buttons[click]["text"]="X"
				self.mv=2
				self.obj_names.append(str(click))
			Check_if_Won=self.Has_Won()
			if Check_if_Won=="O":
				self.GUI_loss()
			elif Check_if_Won=="X":
				self.GUI_win()
			elif Check_if_Won=="Draw":
				self.GUI_draw()
			self.move_no+=2
	def Runprog(self):
		listX=[]
		listO=[]
		listAll=[]
		for x in range(0,9):
			if self.buttons[x]["text"]=="X":
				listX.append(x)
			elif self.buttons[x]["text"]=="O":
				listO.append(x)
		listAll=listO+listX
		
		name=""
		name=''.join(self.obj_names)
		name="_"+name
		
		if name not in self.Menace_obj_list:
			#print(self.move_no)
			M_obj=MENACE(listAll,self.move_no)
			self.Menace_obj_list[name]=M_obj
			self.Menace_click(self.Menace_obj_list[name])
			self.Temp_obj_list.append(self.Menace_obj_list[name])
		else:
			self.Menace_click(self.Menace_obj_list[name])
			self.Temp_obj_list.append(self.Menace_obj_list[name])

	def reset(self):
		for x in range(0,9):
			self.buttons[x]["text"]=''
		self.obj_names=[]
		self.move_no=1
		self.Runprog()
	def GUI_win(self):
		for x in range(0,len(self.Temp_obj_list)):
			self.Temp_obj_list[x].win()
		self.Temp_obj_list=[]
		print("Win call")
		self.mv=3
		self.board.after(1000,lambda:self.reset())
	def GUI_draw(self):
		for x in range(0,len(self.Temp_obj_list)):
			self.Temp_obj_list[x].draw()
		self.Temp_obj_list=[]
		print("Draw call")
		self.mv=3
		self.board.after(1000,lambda:self.reset())
	def GUI_loss(self):
		for x in range(0,len(self.Temp_obj_list)):
			self.Temp_obj_list[x].loss()
		print(self.Temp_obj_list[len(self.Temp_obj_list)-1].probab,"<--")
		self.Temp_obj_list=[]
		print("Loss call")
		self.mv=3
		self.board.after(1000,lambda:self.reset())
	def Has_Won(self):
		#Horizontal
		for x in range(0,7,3):
			if self.buttons[x]["text"]==self.buttons[x+1]["text"]==self.buttons[x+2]["text"]=="X":
				return "X"
			elif self.buttons[x]["text"]==self.buttons[x+1]["text"]==self.buttons[x+2]["text"]=="O":
				return "O"
		#Vertical
		for x in range(0,3):
			if self.buttons[x]["text"]==self.buttons[x+3]["text"]==self.buttons[x+6]["text"]=="X":
				return "X"
			elif self.buttons[x]["text"]==self.buttons[x+3]["text"]==self.buttons[x+6]["text"]=="O":
				return "O"
		#Diagonal
		if self.buttons[0]["text"]==self.buttons[4]["text"]==self.buttons[8]["text"]=="X":
			return "X"
		elif self.buttons[0]["text"]==self.buttons[4]["text"]==self.buttons[8]["text"]=="O":
			return "O"
		elif self.buttons[2]["text"]==self.buttons[4]["text"]==self.buttons[6]["text"]=="X":
			return "X"
		elif self.buttons[2]["text"]==self.buttons[4]["text"]==self.buttons[6]["text"]=="O":
			return "O"
		#Draw
		inv=self.Invalid_Moves()
		invcheck=[0,1,2,3,4,5,6,7,8]
		if invcheck == inv:
			return "Draw"
		return "Continue"
	def Destroy(self):
		with open('dict.pkl','wb') as file:
			pickle.dump(self.Menace_obj_list,file)
		self.board.destroy()


class MENACE:
	def __init__(self,prob,mv_no):
		self.buffer=100
		self.mv=mv_no
		if mv_no==1:
			self.l1 = [4,4,4,4,4,4,4,4,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8]
		elif mv_no==3:
			self.l1 = [0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8]
		elif mv_no==5:
			self.l1 = [0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8]
		elif mv_no==7:
			self.l1 = [0,1,2,3,4,5,6,7,8]
		elif mv_no==9:
			self.l1 = [0,0,0,0,0,1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,8,8,8,8,8]
		self.probab = [x for x in self.l1 if x not in prob]
	def r_select(self):
		try:
			new_cell=random.choice(self.probab)
			self.buffer=new_cell
			print(self.probab)
			return new_cell
		except:
			return "Draw"
	def loss(self):
		self.probab.remove(self.buffer)
	def win(self):
		for x in range(0,3):
			self.probab.append(self.buffer)
	def draw(self):
		self.probab.append(self.buffer)



W=GUI()