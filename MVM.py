import pickle
import random
import tkinter as tk
from tkinter import font
import pprint
from collections import Counter

Xrflag = False    #Turns Player number 1 to a random player
Orflag = False    #Turns Player number 2 to a random player
NumOfGames = 50000   #Define the Number of games to be played
MaxProbab = 70    #Higher number means higher persistance of moves
Drawprobab = 30   #0 indicates no reward for draws

class GUI3:
    def __init__(self):
        self.move_no = 1
        self.rescall=0
        self.obj_names = []
        self.Temp_obj_list1 = []
        self.Temp_obj_list2 = []
        try:
            with open('dictX.pkl', 'rb') as file:
                self.Menace_obj_list1 = pickle.load(file)
            print('x_open')
        except:
            self.Menace_obj_list1 = {}
            print("Cannot find x")
        try:
            with open('dictO.pkl', 'rb') as file1:
                self.Menace_obj_list2 = pickle.load(file1)
            print('o_open')
        except:
            self.Menace_obj_list2 = {}
            print("Cannot find o")

        kz = input()

        self.mv = 1
        self.board = tk.Tk()
        self.board.title("Tic-Tac-Toe")
        self.buttons = []
        self.font1 = font.Font(size=36)
        for x in range(0, 3):
            for y in range(0, 3):
                b = tk.Button(self.board, height=2, width=6, text='', font=self.font1)
                b.config(command=lambda widget=b: self.Menace_click2(widget))
                b.grid(row=x, column=y)
                b.position = (x, y)
                self.buttons.append(b)

        self.b1 = tk.Button(self.board, height=1, width=6, text='Exit', font=self.font1)
        self.b1.config(command=lambda: self.Destroy())
        self.b1.grid(row=3, column=0)
        self.Runprog()
        self.board.mainloop()

    def Invalid_Moves(self):
        invalid_m = []
        for x in range(0, 9):
            if self.buttons[x]["text"] == "X" or self.buttons[x]["text"] == "O":
                invalid_m.append(x)
        return invalid_m

    def Menace_click1(self, Menace_obj):
        click = Menace_obj.r_select()
        if click == -1:
            self.GUI3_loss()
        else:
            invalid_m = self.Invalid_Moves()
            if click not in invalid_m and self.mv % 2 != 0:
                self.buttons[click]["text"] = "X"
                self.mv = 2
                self.obj_names.append(str(click))
                self.move_no += 1
            Check_if_Won = self.Has_Won()
            if Check_if_Won == "Continue":
                return
            if Check_if_Won == "O":
                #print(Check_if_Won,"11")
                self.GUI3_loss()
            elif Check_if_Won == "X":
                #print(Check_if_Won,"12")
                self.GUI3_win()
            elif Check_if_Won == "Draw":
                #print(Check_if_Won,"13")
                self.GUI3_draw()
    def Menace_click2(self, Menace_obj):
        click = Menace_obj.r_select()
        if click == -1:
            self.GUI3_win()
        else:
            invalid_m = self.Invalid_Moves()
            if click not in invalid_m and self.mv % 2 != 1:
                self.buttons[click]["text"] = "O"
                self.mv = 1
                self.obj_names.append(str(click))
                self.move_no += 1
            Check_if_Won = self.Has_Won()

            if Check_if_Won == "Continue":
                return
            if Check_if_Won=="X":
                #print(Check_if_Won,"21")
                self.GUI3_win()
            elif Check_if_Won=="O":
                #print(Check_if_Won,"22")
                self.GUI3_loss()
            elif Check_if_Won=="Draw":
                #print(Check_if_Won,"23")
                self.GUI3_draw()

    def Runprog(self):
        global NumOfGames
        while self.rescall<NumOfGames:
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
            #print(name)
            if self.mv % 2 != 0:
                if name not in self.Menace_obj_list1:
                    # print(self.move_no)
                    M_obj = MENACE1(listAll, self.move_no)
                    self.Menace_obj_list1[name] = M_obj
                    self.Temp_obj_list1.append(M_obj)
                    self.Menace_click1(self.Menace_obj_list1[name])
                    continue
                else:
                    self.Temp_obj_list1.append(self.Menace_obj_list1[name])
                    self.Menace_click1(self.Menace_obj_list1[name])
                    continue
            else:
                if name not in self.Menace_obj_list2:
                    # print(self.move_no)
                    M_obj = MENACE2(listAll, self.move_no)
                    self.Menace_obj_list2[name] = M_obj
                    self.Temp_obj_list2.append(M_obj)
                    self.Menace_click2(self.Menace_obj_list2[name])
                    continue

                else:
                    self.Temp_obj_list2.append(self.Menace_obj_list2[name])
                    self.Menace_click2(self.Menace_obj_list2[name])

    def reset(self):
        for x in range(0, 9):
            self.buttons[x]["text"] = ''
        self.obj_names = []
        self.move_no = 1
        self.mv = 1
        self.rescall+=1

    # With respect to player 1
    def GUI3_win(self):
        self.move_no = 1
        self.mv = 1
        for x in self.Temp_obj_list1:
            x.win()
        for y in self.Temp_obj_list2:
            y.loss()
        self.Temp_obj_list2 = []
        self.Temp_obj_list1 = []
        print("P1 Win call")
        self.mv = 3
        self.reset()
        #self.board.after(1000, lambda: self.reset())

    def GUI3_draw(self):
        self.move_no = 1
        self.mv = 1
        for x in self.Temp_obj_list1:
            x.draw()
        for y in self.Temp_obj_list2:
            y.draw()
        self.Temp_obj_list2 = []
        self.Temp_obj_list1 = []
        print("Draw call")
        self.mv = 3
        self.reset()
        #self.board.after(1000, lambda: self.reset())

    def GUI3_loss(self):
        self.move_no = 1
        self.mv = 1
        for x in self.Temp_obj_list1:
            x.loss()
        for y in self.Temp_obj_list2:
            y.win()
        self.Temp_obj_list2 = []
        self.Temp_obj_list1 = []
        print("P1 Loss call")
        self.mv = 3
        self.reset()
        #self.board.after(1000, lambda: self.reset())

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
        global Orflag
        global Xrflag
        if Xrflag != True:
            with open('dictX.pkl', 'wb') as file:
                pickle.dump(self.Menace_obj_list1, file)
        if Orflag != True:
            with open('dictO.pkl', 'wb') as file1:
                pickle.dump(self.Menace_obj_list2, file1)
        self.board.destroy()


class MENACE1:
    def __init__(self, prob, mv_no):
        self.buffer = 100
        self.mv = mv_no
        self.prob = prob
        if mv_no == 1:
            self.l1 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3,
                       4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7,
                       8, 8, 8, 8, 8, 8, 8, 8]

        elif mv_no == 3:
            self.l1 = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7,
                       8, 8, 8, 8]
        elif mv_no == 5:
            self.l1 = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8]
        elif mv_no == 7:
            self.l1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        elif mv_no == 9:
            self.l1 = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6,
                       6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8]
        try:
            self.probab = [x for x in self.l1 if x not in prob]
        except:
            print(mv_no)

    def __repr__(self):
        k = '['
        for x in self.probab:
            k = k + str(x) + ", "
        k = k[:len(k) - 2]
        k = k + ']'
        return k

    def r_select(self):
        global Xrflag
        if Xrflag == True:

            C = [0,1,2,3,4,5,6,7,8]
            k = [x for x in C if x not in self.prob]
            return random.choice(k)

        else:
            try:
                new_cell = random.choice(self.probab)
                self.buffer = new_cell
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
        global MaxProbab
        C = Counter(self.probab)
        if C[self.buffer] < MaxProbab:
            for x in range(0, 3):
                self.probab.append(self.buffer)
        else:
            pass

    def draw(self):
        global Drawprobab
        C = Counter(self.probab)
        if C[self.buffer] < Drawprobab:
            self.probab.append(self.buffer)
        else:
            pass


class MENACE2:
    def __init__(self, prob, mv_no):
        self.buffer = 100
        self.mv = mv_no
        self.prob = prob
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
        self.probab = [x for x in self.l1 if x not in prob]

    def __repr__(self):
        k = '['
        for x in self.probab:
            k = k + str(x) + ", "
        k = k[:len(k) - 2]
        k = k + ']'
        return k

    def r_select(self):
        global Orflag
        if Orflag == True:
            
            C = [0,1,2,3,4,5,6,7,8]
            k = [x for x in C if x not in self.prob]
            return random.choice(k)
        else:        
            try:
                new_cell = random.choice(self.probab)
                self.buffer = new_cell
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
        global MaxProbab
        C = Counter(self.probab)
        if C[self.buffer] < MaxProbab:
            for x in range(0, 3):
                self.probab.append(self.buffer)
        else:
            pass

    def draw(self):
        global Drawprobab
        C = Counter(self.probab)
        if C[self.buffer] < Drawprobab:
            self.probab.append(self.buffer)
        else:
            pass


# pprint.pprint(Menace_obj_list1, stream=None, indent=3, width=80, depth=None)
W = GUI3()
