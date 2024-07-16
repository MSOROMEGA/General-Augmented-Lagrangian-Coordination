# -*- coding: utf-8 -*-
#制作不易，转载请注明出处
#出处：黄海南(Hainan Huang), hhn0113@outlook.com
import sys
sys.path.append('GeneralALC')
import numpy as np
import gurobipy as gp
from gurobipy import GRB
from itertools import product
from math import sqrt
import node_methods as nmt

class node_0(): 
# 非自定义的模块1_start
    def __init__(self):
        # 初始化
        self.mutipler_list = []
        self.penalty_list = []
        self.receive_list = []
# 非自定义的模块1_end
    
# 自定义的模块2_start
    def compute_distance(self,loc1, loc2):
        dx = loc1[0] - loc2[0]
        dy = loc1[1] - loc2[1]
        return sqrt(dx*dx + dy*dy)
# 自定义的模块2_end
    
# 非自定义的模块3_start
    def decision_model(self):
# 非自定义的模块3_end
    
# 自定义的模块4_start
        # Parameters
        np.random.seed(0)
        cn = 20
        fn = 20
        customers = np.random.rand(cn,2).tolist()
        facilities = np.random.rand(fn,2).tolist()
        
        # Compute key parameters of MIP model formulation
        num_facilities = len(facilities)
        num_customers = len(customers)
        cartesian_prod = list(product(range(num_customers), range(num_facilities)))
        
        # MIP  model formulation
        m = gp.Model('facility_location')
        # 设置变量
        assign = m.addVars(cartesian_prod, ub=1, vtype=GRB.CONTINUOUS, name='Assign')
    
        # coupling_list
        # 将字典转化为列表，创建耦合列表, 所有元素都转为np.array
        assign_list = np.array(list(assign.values()))
        coupling_send_list = np.array([np.array([],dtype=object),
                                  np.array([assign_list],dtype=object),
                                  np.array([assign_list],dtype=object)],
                                 dtype=object) 
        coupling_receive_list = np.array([np.array([],dtype=object),
                                  np.array([assign_list],dtype=object),
                                  np.array([assign_list],dtype=object)],
                                 dtype=object) 
# 自定义的模块4_end
        
# 非自定义的模块5_start
        #不一致性惩罚计算
        obj_augmented_penalty,self.receive_list,self.mutipler_list,self.penalty_list = nmt.penalty_function(coupling_receive_list,self.receive_list,self.mutipler_list,self.penalty_list)
# 非自定义的模块5_end
          
# 自定义的模块6_start
        #自身目标+不一致性惩罚
        m.setObjective(obj_augmented_penalty, GRB.MINIMIZE)
        
        # 求解器参数设置和求解
        m.setParam('OutputFlag', False)
        m.optimize()
# 自定义的模块6_end
        
# 非自定义的模块7_start
        #不一致性结果
        self.objVal = m.objVal
        self.pure_objVal = m.objVal - obj_augmented_penalty.getValue()
        self.sending_list,self.consistency_list = nmt.return_penalty_result(coupling_receive_list, self.receive_list, coupling_send_list)
        return self.sending_list,self.consistency_list
# 非自定义的模块7_end
        
        
if __name__ == '__main__':
    Node_0 = node_0() # 实例化问题的参数
    Node_0.decision_model() # 求解问题
  
        
        
