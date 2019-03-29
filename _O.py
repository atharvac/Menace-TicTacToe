import pickle
import random
import tkinter as tk
from tkinter import font
from collections import Counter
firstrun = 1

#Tkinter GUI
class GUI2:
    def __init__(self):
        self.move_no = 0

        self.obj_names = []
        self.Temp_obj_list = []
        try:
            with open('dictO.pkl', 'rb') as file:
                self.Menace_obj_list = pickle.load(file)
        except:
            self.Menace_obj_list = {}

        self.mv = 3
        self.board = tk.Tk()
        self.proBoard = tk.Tk()
        self.proBoard.title("Probability of earlier move")
        self.board.title("Tic-Tac-Toe")
        self.buttons = []
        self.proButtons = []
        self.font1 = font.Font(size=36)
        #Create buttons
        for x in range(0, 3):
            for y in range(0, 3):
                b = tk.Button(self.board, height=2, width=6, text='', font=self.font1)
                b.config(command=lambda widget=b: self.callProg(widget))
                b.grid(row=x, column=y)
                b.position = (x, y)
                self.buttons.append(b)

                p = tk.Button(self.proBoard, height=4, width=12, text='', font=self.font1)
                p.grid(row=x, column=y)
                p.position = (x, y)
                self.proButtons.append(p)

        self.b1 = tk.Button(self.board, height=1, width=6, text='Exit', font=self.font1)
        self.b1.config(command=lambda: self.Destroy())
        self.b1.grid(row=3, column=0)

        self.TextBox = tk.Label(self.board, text="",font = self.font1)
        self.TextBox.grid(row = 3, column = 2)
        self.Runprog()
        self.board.mainloop()

    def callProg(self,widget):
        k = self.on_click(widget)
        if k==0:
            self.Runprog()

    def Invalid_Moves(self):
        invalid_m = []
        for x in range(0, 9):
            if self.buttons[x]["text"] == "X" or self.buttons[x]["text"] == "O":
                invalid_m.append(x)
        return invalid_m

    def Disp_Probab(self,ll):
        ct = Counter(ll)
        for x in range(9):
            try:
                perc = str((ct[x]/len(ll))*100)+"0000"
                perc = perc[:4]
                self.proButtons[x]["text"] = perc + " %"
            except:
                self.proButtons[x]["text"] = "0 %"
    
    def on_click(self, widget):
        r, c = widget.position
        convert = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        num = convert[r][c]
        iv = self.Invalid_Moves()
        if num not in iv:
            self.move_no += 1
        else:
            return -1
        if num not in iv and self.mv % 2 != 0:
            self.buttons[num]["text"] = "X"
            self.mv = 2
            self.obj_names.append(str(num))
            check = self.Invalid_Moves()
            check2 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            Check_if_Won = self.Has_Won()
            if check != check2 and Check_if_Won == "Continue":
                return 0
            if Check_if_Won == "O":
                self.GUI2_win()
            elif Check_if_Won == "X":
                self.GUI2_loss()
            elif Check_if_Won == "Draw":
                self.GUI2_draw()

    def Menace_click(self, Menace_obj):
        click = Menace_obj.r_select()
        self.Disp_Probab(Menace_obj.probab)
        #Print probability
        if click == -1:
            self.GUI2_loss()
        else:
            invalid_m = self.Invalid_Moves()
            if click not in invalid_m and self.mv % 2 != 1:
                self.buttons[click]["text"] = "O"
                self.mv = 3
                self.obj_names.append(str(click))
            Check_if_Won = self.Has_Won()
            if Check_if_Won == "O":
                self.GUI2_win()
            elif Check_if_Won == "X":
                self.GUI2_loss()
            elif Check_if_Won == "Draw":
                self.GUI2_draw()

    def Runprog(self):
        global firstrun
        if firstrun == 1:
            firstrun=0
        else:
            self.move_no+=1
        listX = []
        listO = []
        listAll = []
        for x in range(0, 9):
            if self.buttons[x]["text"] == "X":
                listX.append(x)
            elif self.buttons[x]["text"] == "O":
                listO.append(x)
        listAll = listO + listX

        name = ""
        name = ''.join(self.obj_names)
        name = "_" + name
        if self.mv % 2 == 0:
            if name not in self.Menace_obj_list:
                # print(self.move_no)
                M_obj = MENACE2(listAll, self.move_no)
                self.Menace_obj_list[name] = M_obj
                self.Temp_obj_list.append(self.Menace_obj_list[name])
                self.Menace_click(self.Menace_obj_list[name])

            else:
                self.Temp_obj_list.append(self.Menace_obj_list[name])
                self.Menace_click(self.Menace_obj_list[name])

    def reset(self):
        global firstrun
        firstrun = 1
        self.TextBox["text"] = ""
        for x in range(0, 9):
            self.buttons[x]["text"] = ''
        self.obj_names = []
        self.move_no = 0
        self.mv = 1
        self.Runprog()

    def GUI2_win(self):
        self.TextBox["text"] = "You Lose"
        for x in self.Temp_obj_list:
            x.win()
        self.Temp_obj_list = []
        print("Win call")
        self.mv = 3
        self.board.after(1500, lambda: self.reset())

    def GUI2_draw(self):
        self.TextBox["text"] = "Draw"
        for x in self.Temp_obj_list:
            x.draw()
        self.Temp_obj_list = []
        print("Draw call")
        self.mv = 3
        self.board.after(1500, lambda: self.reset())

    def GUI2_loss(self):
        self.TextBox["text"] = "You Win"
        for x in self.Temp_obj_list:
            x.loss()
        self.Temp_obj_list = []
        print("Loss call")
        self.mv = 3
        self.board.after(1500, lambda: self.reset())

    def Has_Won(self):
        # Horizontal
        for x in range(0, 7, 3):
            if self.buttons[x]["text"] == self.buttons[x + 1]["text"] == self.buttons[x + 2]["text"] == "X":
                return "X"
            elif self.buttons[x]["text"] == self.buttons[x + 1]["text"] == self.buttons[x + 2]["text"] == "O":
                return "O"
        # Vertical
        for x in range(0, 3):
            if self.buttons[x]["text"] == self.buttons[x + 3]["text"] == self.buttons[x + 6]["text"] == "X":
                return "X"
            elif self.buttons[x]["text"] == self.buttons[x + 3]["text"] == self.buttons[x + 6]["text"] == "O":
                return "O"
        # Diagonal
        if self.buttons[0]["text"] == self.buttons[4]["text"] == self.buttons[8]["text"] == "X":
            return "X"
        elif self.buttons[0]["text"] == self.buttons[4]["text"] == self.buttons[8]["text"] == "O":
            return "O"
        elif self.buttons[2]["text"] == self.buttons[4]["text"] == self.buttons[6]["text"] == "X":
            return "X"
        elif self.buttons[2]["text"] == self.buttons[4]["text"] == self.buttons[6]["text"] == "O":
            return "O"
        # Draw
        inv = self.Invalid_Moves()
        invcheck = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        if invcheck == inv:
            return "Draw"
        return "Continue"

    def Destroy(self):
        with open('dictO.pkl', 'wb') as file:
            pickle.dump(self.Menace_obj_list, file)
        self.board.destroy()

#Store all the gamestates and its probabilities
class MENACE2:
    def __init__(self, prob, mv_no):
        self.buffer = 100
        self.mv = mv_no
        if mv_no == 2:
            self.l1 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3,
                       4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7,
                       8, 8, 8, 8, 8, 8, 8, 8]
        elif mv_no == 4:
            self.l1 = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7,
                       8, 8, 8, 8]
        elif mv_no == 6:
            self.l1 = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8]
        elif mv_no == 8:
            self.l1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        else:
            self.l1 = [0,1,2,3,4,5,6,7,8]
            print(mv_no,"Fail")
        try:
            self.probab = [x for x in self.l1 if x not in prob]
        except:
            print(mv_no, "_________________________________________________")

    def __repr__(self):
        k = '['
        for x in self.l1:
            k = k + str(x) + ", "
        k = k[:len(k) - 2]
        k = k + ']'
        return k

    def r_select(self):
        try:
            new_cell = random.choice(self.probab)
            self.buffer = new_cell
            #print(self.probab)
            return new_cell
        except:
            model = [0,1,2,3,4,5,6,7,8]
            if self.mv < 8:
                k = [x for x in model if x not in self.prob]
                print("Random Invoked")
                self.buffer = random.choice(k)
                return self.buffer
            return -1

    def loss(self):
        try:
            self.probab.remove(self.buffer)
        except:
            pass

    def win(self):
        for x in range(0, 3):
            self.probab.append(self.buffer)

    def draw(self):
        self.probab.append(self.buffer)

# pprint.pprint(Menace_obj_list, stream=None, indent=3, width=80, depth=None)
#W=GUI2()
