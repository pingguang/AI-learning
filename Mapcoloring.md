# AI-learning
# 约束满足求解地图着色问题
回溯法：在搜索树中，每一层的所有节点表示某种变量；某个节点的所有分支表示该变量的所有可能取值。回溯法从树的根节点开始，每次选择一个分支执行，即选取该变量的某个具体取值 (此操作被称为“实例化变量”)。然后，算法检测新变量的取值与已有变量的取值是否满足约束：如果满足，表明新变量实例化成功，继续往下执行，到达下一层 (即选取另一个新变量)；否则，新变量实例化失败，需要回溯，重新实例化一个新值。上述过程，递归进行：

• 如果所有变量都有合法值或满足约束的值，则找到问题的解；

• 如果当前变量的所有实例化回溯失败，则执行变量回溯，即回溯至上一个变量的某个取值；直至找到一个解或所有解，或者已经遍历所有的变量取值组合，没有找到解，算法停止。     从回溯法的算法描述可以看出，回溯法使用约束函数来消除无效子树的搜索，相当于对解搜索树进行了剪枝处理，因而大大提高了效率。
但是，回溯法本质上还是解空间上的深度优先搜索，对大多数问题而言，其时间复杂度仍然是指数级的。回溯法也是一种完备的搜索算法，这意味着，如果问题有解的话，它一定能够找到解。

# 关于程序伪代码：
1.Mapcoloring.py : 回溯算法找出一个满足所有约束条件的解

  def Consistent(Xi,v(i)):     //判断是否相容 
  
      for each (Xj,v(j))∈ Solution:      
      
      if Rij ∈ R and (v(i), v(j)) /∈ Rij :  
      
         return False         
         
  return True


  def Backtracking(Vars):
  
      Select a variable Xi ∈ Vars 
      
      for each value v(i) ∈ Di:
      
          if Consistent(Xi, v(i)):
          
             Solution ← Solution + (Xi, v(i))
             
             if Xi is the only variable in Vars:
             
                return True
                
             else:
             
                if Backtracking(Vars\{Xi}):
                
                   return True
                   
                else:
                
             Solution ← Solution − (Xi, v(i))
             
       return False


   def CSP-BT():
   
       Solution ← ∅



2.Mapcoloring2.py: 回溯算法找出所有满足所有约束条件的解

  def Consistent(Xi,v(i)):    //判断是否相容
  
      for each (Xj,v(j))∈ Solution:
      
      if Rij ∈ R and (v(i), v(j)) /∈ Rij :
      
        return False
        
      return True

  def Backtracking(V ars):
  
      Select a variable Xi ∈ Vars
      
      for each value v(i) ∈ Di
      
      if Consistent(Xi, v(i)):
      
         Solution ← Solution + (Xi, v(i))
         
         if Xi is the only variable in Vars:
         
            Solutions ← Solutions + Solution
            
         else:
         
            Backtracking(Vars\{Xi})
            
         Solution ← Solution − (Xi, v(i))
         

  def CSP-BT():
  
      Solutions ← ∅
      
      Solution ← ∅
      
  return Backtracking(X)
