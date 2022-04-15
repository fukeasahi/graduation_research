from random import random, randint, seed
from statistics import mean
from copy import deepcopy
from turtle import left

import numpy as np
import pandas as pd

df = pd.read_excel("/content/data.xlsx")


POP_SIZE        = 60   # 母集団の大きさ
MIN_DEPTH       = 2    # 初期ランダムツリーの深さの最小値
MAX_DEPTH       = 5    # 初期ランダムツリーの深さの最大値
GENERATIONS     = 250  # 進化を実行するための最大世代数
TOURNAMENT_SIZE = 5    # トーナメント選抜のためのトーナメントサイズ
XO_RATE         = 0.8  # クロスオーバー率 
PROB_MUTATION   = 0.2  # ノードごとの突然変異の確率 

def add(x, y): return x + y
def sub(x, y): return x - y
def mul(x, y): return x * y
FUNCTIONS = [add, sub, mul]
TERMINALS = ['x', -2, -1, 0, 1, 2] 

def generate_dataset(): # generate 101 data points from target_func
    dataset = []
    for i in range(len(np.array(df["平均気温(℃)"]))):
      dataset.append([np.array(df["最高気温(℃)"])[i], np.array(df["数量(t)"] * 1000 * df["円/kg"])[i]/10**12])
    return dataset

class GPTree:
    def __init__(self, data = None, left = None, right = None):
        self.data  = data
        self.left  = left
        self.right = right
        
    def node_label(self): # string label
        if (self.data in FUNCTIONS):
            return self.data.__name__
        else: 
            return str(self.data)
    
    def print_tree(self, prefix = ""): # textual printout
        print("%s%s" % (prefix, self.node_label()))        
        if self.left:  self.left.print_tree (prefix + "   ")
        if self.right: self.right.print_tree(prefix + "   ")

    def compute_tree(self, x): 
        # もし、dataが[add, sub, mul]の場合、左下と右下をcompute_tree()する
        if (self.data in FUNCTIONS): 
            return self.data(self.left.compute_tree(x), self.right.compute_tree(x))
        # もしdataが'x'の場合、xを返す
        elif self.data == 'x': return x
        # [-2, -1, 0, 1, 2]は、それを返す
        else: return self.data
            
    def random_tree(self, grow, max_depth, depth = 0): # create random tree using either grow or full method
        # もし深さが最小の深さよりも小さいか最大の深さよりは小さいが成長しない場合、+か-か*を追加する
        if depth < MIN_DEPTH or (depth < max_depth and not grow): 
            self.data = FUNCTIONS[randint(0, len(FUNCTIONS)-1)]
        # もし、深さが初期のランダムツリーの深さ以上ならば、['x', -2, -1, 0, 1, 2] から選択して、dataに格納する
        elif depth >= max_depth:   
            self.data = TERMINALS[randint(0, len(TERMINALS)-1)]
        else: # intermediate depth, grow
            # 1/2の確率で、、['x', -2, -1, 0, 1, 2] から選択して、dataに格納する
            if random () > 0.5: 
                self.data = TERMINALS[randint(0, len(TERMINALS)-1)]
            # 1/2の確率で、[add, sub, mul]から選択して、dataに格納する
            else:
                self.data = FUNCTIONS[randint(0, len(FUNCTIONS)-1)]
        # もし、[add, sub, mul]から選択された場合、左下と右下それぞれにGPTreeをもう一度実行する
        if self.data in FUNCTIONS:
            self.left = GPTree()          
            self.left.random_tree(grow, max_depth, depth = depth + 1)            
            self.right = GPTree()
            self.right.random_tree(grow, max_depth, depth = depth + 1)

    def mutation(self):
        # 20%の確率で、ノードごとの突然変異を起こす
        if random() < PROB_MUTATION: # mutate at this node
            self.random_tree(grow = True, max_depth = 2)
        # もしレフトに値があれば、mutation()を実行する
        elif self.left: self.left.mutation()
        # もしライトに値があれば、mutation()を実行する
        elif self.right: self.right.mutation() 

    def size(self): # tree size in nodes
        # もしself.dataが['x', -2, -1, 0, 1, 2]の時は1を返す
        if self.data in TERMINALS: return 1
        # もしleftに値が入っていれば、もう一度size()を実行する、なければ、0を返す
        l = self.left.size()  if self.left  else 0
        # もし、rightに、値があれば、もう一度、size()を実行する、なければ、0を返す
        r = self.right.size() if self.right else 0
        return 1 + l + r

    def build_subtree(self): # count is list in order to pass "by reference"
        # GPtreeのインスタンスを作成する
        t = GPTree()
        # インスタンスのデータをself.dataにする
        t.data = self.data
        # もしslf.leftをに値があれば、self.left.build_subtree()をt.leftに実行する
        if self.left:  t.left  = self.left.build_subtree()
        # もしslf.rightをに値があれば、self.right.build_subtree()をt.rightに実行する
        if self.right: t.right = self.right.build_subtree()
        return t
                        
    def scan_tree(self, count, second): # note: count is list, so it's passed "by reference"
        count[0] -= 1            
        if count[0] <= 1: 
            # もし、secondが無ければ、self.build_subtree()
            if not second: # return subtree rooted here
                return self.build_subtree()
            else: # glue subtree here
                self.data  = second.data
                self.left  = second.left
                self.right = second.right
        else:  
            ret = None              
            # もし、左下に値があり、count[0]が1以上の場合、左下をscan_tree()をする
            if self.left  and count[0] > 1: ret = self.left.scan_tree(count, second)  
            # もし、右下に値があり、count[0]が1以上の場合、右下をスキャンする
            if self.right and count[0] > 1: ret = self.right.scan_tree(count, second)  
            return ret

    def crossover(self, other): 
        # 80%の確率でクロスオーバーを行う
        if random() < XO_RATE:
            second = other.scan_tree([randint(1, other.size())], None) 
            self.scan_tree([randint(1, self.size())], second) 
                   
def init_population(): 
    pop = []
    # こっちは、growがtrueの場合、、、mdを3、４、５でそれぞれ回していく
    for md in range(3, MAX_DEPTH + 1):
        # iを0,1,2,3,4,5,6,7,8,9でそれぞれ回していく
        for i in range(int(POP_SIZE/6)):
            t = GPTree()
            t.random_tree(grow = True, max_depth = md) 
            pop.append(t) 
        # こっちは、growがFlaseの場合、、、iを0,1,2,3,4,5,6,7,8,9でそれぞれ回していく
        for i in range(int(POP_SIZE/6)):
            t = GPTree()
            t.random_tree(grow = False, max_depth = md) 
            pop.append(t) 
    return pop

def fitness(individual, dataset): 
    diff = []
    for ds in dataset:
      diff.append(abs(individual.compute_tree(ds[0]) - ds[1]))
    return 1 / (1 + mean(diff))
                
def selection(population, fitnesses): 
    tournament = []
    # iを0,1,2,3,4で回す
    for i in range(TOURNAMENT_SIZE):
      # ランダムにモデルのindexを選択する
      tournament.append(randint(0, len(population)-1))

    tournament_fitnesses = []
    for i in range(TOURNAMENT_SIZE):
      tournament_fitnesses.append(fitnesses[tournament[i]])
  
    # 値が最も真に近いモデルを返す
    return deepcopy(population[tournament[tournament_fitnesses.index(max(tournament_fitnesses))]]) 
            
def main():      
    seed() 
    # データセットを作成
    dataset = generate_dataset() 

    # 初期のGPTreeを作成する
    # 複数のGPTreeが格納された配列が返ってくる
    population= init_population() 
    best_of_run = None
    best_of_run_f = 0
    best_of_run_gen = 0

    fitnesses = []
    for i in range(POP_SIZE):
      fitnesses.append(fitness(population[i], dataset))

    # 0代目から250代目まで
    for gen in range(GENERATIONS):        
        nextgen_population=[]
        # iを0から60まで繰り返す
        for i in range(POP_SIZE):
            parent1 = selection(population, fitnesses)
            parent2 = selection(population, fitnesses)
            
            parent1.crossover(parent2)
            # 突然変異を起こす
            parent1.mutation()
            nextgen_population.append(parent1)

        population = nextgen_population
    
        fitnesses = []
        for i in range(POP_SIZE):
          fitnesses.append(fitness(population[i], dataset))

        if max(fitnesses) > best_of_run_f:
            best_of_run_f = max(fitnesses)
            best_of_run_gen = gen
            best_of_run = deepcopy(population[fitnesses.index(max(fitnesses))])
            print("________________________")
            print("gen:", gen, ", best_of_run_f:", round(max(fitnesses),3), ", best_of_run:") 
            best_of_run.print_tree()
        if best_of_run_f == 1: break   
    
    print("\n\n_________________________________________________\nEND OF RUN\nbest_of_run attained at gen " + str(best_of_run_gen) +\
          " and has f=" + str(round(best_of_run_f,3)))
    best_of_run.print_tree()
    
if __name__== "__main__":
  main()







  