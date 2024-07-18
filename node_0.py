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
    def __init__(self):
        # 初始化
        self.mutipler_list = []
        self.penalty_list = []
        self.receive_list = []
        self.node_id = 0
    
    def compute_distance(self,loc1, loc2):
        dx = loc1[0] - loc2[0]
        dy = loc1[1] - loc2[1]
        return sqrt(dx*dx + dy*dy)
    
    def decision_model(self):
        # 参数设置
        np.random.seed(0)
        cn = 5
        fn = 5
        customers = np.random.rand(cn,2).tolist()
        facilities = np.random.rand(fn,2).tolist()
        num_facilities = len(facilities)
        num_customers = len(customers)
        cartesian_prod = list(product(range(num_customers), range(num_facilities)))
        
        # 实例化模型
        m = gp.Model('facility_location')
        
        # 变量设置
        assign = m.addVars(cartesian_prod, ub=1, vtype=GRB.CONTINUOUS, name='Assign')

        # 约束设置
        # 无约束

        # 目标设置
        assign_list = np.array(list(assign.values()))
        coupling_send_list = np.array([np.array([],dtype=object),
                                  np.array([assign_list],dtype=object),
                                  np.array([assign_list],dtype=object)],
                                 dtype=object) 
        coupling_receive_list = np.array([np.array([],dtype=object),
                                  np.array([assign_list],dtype=object),
                                  np.array([assign_list],dtype=object)],
                                 dtype=object) 
        obj_augmented_penalty,self.receive_list,self.mutipler_list,self.penalty_list = nmt.penalty_function(coupling_receive_list,self.receive_list,self.mutipler_list,self.penalty_list,self.node_id)
        m.setObjective(obj_augmented_penalty, GRB.MINIMIZE)
        
        # 求解器设置
        m.setParam('OutputFlag', False)
        m.optimize()
        
        # 结果设置，假的(过时的)不一致性，仅用来监测当前的不一致性程度
        self.objVal = m.objVal
        self.pure_objVal = m.objVal - obj_augmented_penalty.getValue()
        self.sending_list,self.consistency_list,self.coupling_receive_list_value = nmt.return_penalty_result(coupling_receive_list, self.receive_list, coupling_send_list,self.node_id)
        
        
if __name__ == '__main__':
    Node_0 = node_0()
    Node_0.decision_model()
  
        
        
