from itertools import cycle
from multiprocessing import Process, Queue
from tkinter.messagebox import showinfo
import tkinter 
import numpy as np

from Board import Board
from mcts import mcts
from tkinter import * 

class Game:

    def __init__(self):   
        self.size = 12    #棋盘的大小
        self.grid = 30    #棋盘每格的大小
        self.player = 0   #玩家，0表示还没开始，-1表示玩家，1表示电脑
        self.board = None #棋盘
        self.previous = [] #用于判断玩家是否可以悔棋
        self.is_start = False #游戏的状态    
        self.chess_radius = 10  #棋子的半径
        self.queue = Queue()

        self.tk = Tk()   #窗口设计
        self.tk.title("MCTS五子棋")
        self.tk_header = Frame(self.tk, highlightthickness=0)
        self.tk_header.pack(fill=BOTH)
        self.func_start = Button(self.tk_header, text="开始", command=self.start) #开始按钮
        self.func_restart = Button(self.tk_header, text="重玩", command=self.restart, state=DISABLED) #重新开始按钮
        self.info = Label(self.tk_header, text="游戏未开始")
        self.func_tishi = Label(self.tk_header,text = "棋盘大小：")
        self.gobangSize = StringVar()  #输入框
        self.gobangSize.set(12)  #设置默认值为12
        self.func_size = Entry(self.tk_header,textvariable=self.gobangSize,width=8)
        self.func_regret = Button(self.tk_header, text="悔棋", command=self.regret, state=DISABLED)  #悔棋按钮
        self.func_tishi.pack(side=LEFT)  #将按钮和编辑框放入容器当中
        self.func_size.pack(side=LEFT)
        self.func_start.pack(side=LEFT)
        self.func_restart.pack(side=LEFT)
        self.info.pack(side=LEFT, expand=YES, fill=BOTH, pady=5)
        self.func_regret.pack(side=RIGHT)
        #添加画布
        self.canvas = Canvas(self.tk, bg="grey",
                             width=(self.size + 1) * self.grid,
                             height=(self.size + 1) * self.grid,
                             highlightthickness=0)
        self.draw_board()
        self.canvas.pack()
        self.tk.mainloop()
        

    def draw_grid(self):  #绘制棋盘网格
        for i in range(self.size):
            self.canvas.create_line((i+1) * self.grid , self.grid, (i+1)* self.grid, self.size * self.grid)
            self.canvas.create_line(self.grid,(i+1) * self.grid, self.size * self.grid, (i+1) * self.grid)

    def draw_chess(self, x, y, color):  #绘制棋子
        center_x, center_y = self.grid * (x + 1), self.grid * (y + 1)
        self.qizi = self.canvas.create_oval(center_y - self.chess_radius,
                                center_x - self.chess_radius,
                                center_y + self.chess_radius,
                                center_x + self.chess_radius,
                                fill=color)

    def draw_board(self): #绘制棋盘
        self.canvas.destroy()
        self.canvas = Canvas(self.tk, bg="grey",
                width=(self.size + 1) * self.grid,
                height=(self.size + 1) * self.grid,
                highlightthickness=0)
        self.canvas.pack()      
        self.canvas.bind("<Button-1>", self.click)
        self.draw_grid()

    def start(self):
        self.size = int(self.gobangSize.get())  #修改棋盘的大小
        del (self.board)
        self.board = Board(self.size)
        self.func_start.config(state=DISABLED)  #改变按钮的状态
        self.func_restart.config(state=NORMAL)
        self.func_regret.config(state=NORMAL)
        self.is_start = True
        self.player = -1  #开始后玩家线下棋
        self.draw_board()
        self.info.config(text="黑方下棋")

    def restart(self):  #重新开始棋局
        self.start()

    def regretQiZi(self):  #悔棋，删除黑子
        self.canvas.delete(self.qizi)

    def regret(self):  #悔棋功能
        if not self.previous or len(self.previous) == 2:   #如果玩家还没下棋，或是白方已经下棋，就不能悔棋
            showinfo("提示", "您已没有机会悔棋")
            self.previous = []
            return
        x, y = self.previous[0]
        self.regretQiZi()
        self.board.chess[x, y] = 0   #悔棋后黑方所下棋的位置的数值改为0
        self.info.config(text="黑方下棋")
        self.previous = []   
        self.player = -1
    
    def waiting(self):
        if not self.previous:
            self.queue = Queue()
            return
        elif not self.queue.empty():
            pos = self.queue.get()
            self.draw_chess(*pos, "white")
            self.player = -1 
            self.board.move(pos, 1) #白方下棋
            print(f' {pos}')
            if self.player_win(*pos,1):  #判断白方是否获胜
                self.is_start = False
                self.func_start.config(state=NORMAL)  #改变按钮的状态
                self.func_restart.config(state=DISABLED)
                self.func_regret.config(state=DISABLED)
                self.info.config(text="白方胜，你输了！")
                return
            self.info.config(text="黑方下棋")
            self.previous.append(pos)  #将白方的棋存入previous中
            return
        self.info.config(text="白方下棋" )  #+ next(self.points)#
        self.tk.after(1000, self.waiting)

    def click(self, e):  #玩家点击屏幕下棋
        if self.player != -1: 
            return   #如果不归玩家下棋，点击棋盘不能下棋
        #轮到玩家下棋
        self.player = 1   #将身份改为白方
        x, y = int((e.y - self.grid/2) / self.grid), int((e.x - self.grid/2) / self.grid)  #获得玩家（黑方）棋子所下的位置,鼠标位置转化为画布棋子位置
        #防止棋子下出格
        if not ((0, ) * 2 <= (x, y) < (self.size, ) * 2):
            self.player = -1
            return
        center_x, center_y = self.grid * (x + 1), self.grid * (y + 1)
        distance = np.linalg.norm(np.array([center_x, center_y]) - np.array([e.y, e.x]))
        if not self.is_start or distance > self.grid/2 * 0.95 or self.board.chess[x, y] != 0:
            self.player = -1
            return

        self.draw_chess(x, y, "black")
        print(f'=> 黑方: {(x, y)}')
        self.board.move((x, y), -1)
        self.previous = [(x, y)]  #将黑子下的位置储存在previous当中
        if self.player_win(x, y, -1):    #判断玩家是否获胜
            self.is_start = False   #不能下棋
            self.func_start.config(state=NORMAL)  #改变按钮的状态
            self.func_restart.config(state=DISABLED)
            self.func_regret.config(state=DISABLED)
            self.info.config(text="你真棒，你赢了！")
            return
        self.info.config(text="白方下棋")
        print(f'=> 白方:', end='')
        self.queue.put(self.board)
        Process(target=mcts, args=(self.queue, 150)).start()   #执行进程
        self.tk.after(1000, self.waiting)

    def player_win(self, x, y, tag):
        four_direction = [ [self.board.chess[i][y] for i in range(self.size)] ]  #竖直方向上看是否连成五子
        four_direction.append([self.board.chess[x][j] for j in range(self.size)])  #水平方向上看是否连成五子
        four_direction.append(self.board.chess.diagonal(y - x))   #主对角线上看是否连成五子
        four_direction.append(np.fliplr(self.board.chess).diagonal(self.size - 1 - y - x))  #副主对角线上看是否连成五子

        for v_list in four_direction:  #遍历四个方向，看是否连成五子
            count = 0
            for v in v_list:   #统计该方向上是否连成五子
                if v == tag:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0
        return False

if __name__ == '__main__':
    game = Game()
