import copy 

class Node:
    def __init__(self, no):
        self.nodeNo = no   #节点的编号
        self.color = ""    #节点的颜色
        self.next = []     #也这个节点相连的节点
    
    def initNextNode(self, next):   #为节点门初始化相连节点
        for i in next:
            self.next.append(i) 







#自定义函数
'''
def Consistent(Xi,Solution):
    for Xj,vj in Solution:
        if(Xi == Xj or Xi.color == vj):
            return False
    return True
'''

def Consistent(Xi,vi):
    for Xj in Xi.next:
        if  vi == Xj.color:
            return False
    return True


def Backtracking(Vars,Solution):   #找出一个满足所有约束条件的解
     Xi,Vi = Vars[0]     #Xi存储的是第一个节点，Vi保存的是所有的颜色
     for vi in Vi:
         #print(Consistent(Xi,Solution))
         #if Consistent(Xi,Solution):   #判断是否相容,相容返回true,不相容返回false
         if Consistent(Xi,vi):   #判断是否相容,相容返回true,不相容返回false
            Solution.append((Xi,vi))
            Xi.color = vi
            if len(Vars) == 1:  #表示节点是最后一个节点
               return True
            else:   #若Xi不是最后一个变量
                VarsCopy = copy.deepcopy(Vars)  #对Vars进行深度拷贝,防止后面的操作修改Vars
                VarsCopy.pop(0)    #将第一个节点从VarsCopy中剔除，换成第二个节点
                if Backtracking(VarsCopy,Solution):
                   return True
                else:
                    Solution.pop()
     return False


def main():
     colors = []  #用于存放节点的颜色
     graph = []   #用于存放节点
   
     #将8个节点存放到graph中
     for i in range(8):      
          #print("i = ",i)    #其中i的变化范围是0~7
          graph.append(Node(i))


     #颜色初始化，因为最多用八种颜色    
     colors = ["Red", "Green", "Blue","Yellow","Black","White","Grey","Pink"]
     print("所有颜色：",colors)     #输出所有颜色，列表形式

     #为节点门初始化相连的节点
     graph[0].initNextNode([graph[1], graph[2],graph[3]])
     graph[1].initNextNode([graph[0], graph[2],graph[4]])
     graph[2].initNextNode([graph[0], graph[1], graph[3], graph[4],graph[5]])
     graph[3].initNextNode([graph[0], graph[2], graph[5], graph[6]])
     graph[4].initNextNode([graph[1], graph[2],graph[5]])
     graph[5].initNextNode([graph[2], graph[3],graph[4],graph[6]])
     graph[6].initNextNode([graph[3], graph[5]])
     graph[7].initNextNode([graph[6]])

     Vars = []
     for node in graph:
         Vars.append((node,colors))
     Solution = []
     Backtracking(Vars,Solution)
     
     colorAll = []
     colorCount = 1   #统计颜色的个数
     colorFlag = True

     for Xi,Vi in Solution:
         for color in colorAll:   
             if Vi == color:
                 colorFlag = False
         if colorFlag:
             colorCount += 1
             colorAll.append(Vi)
         print("节点： ",Xi.nodeNo, "\t颜色： ",Vi)
    
     print("只需要",colorCount,"种颜色即可！")


if __name__ == '__main__':
    main()