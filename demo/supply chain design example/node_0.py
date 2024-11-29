# -*- coding: utf-8 -*-
#制作不易，转载请注明出处
#出处：黄海南(Hainan Huang), hhn0113@outlook.com; yuting pei, Email：1149015019@qq.com
import sys
sys.path.append('GeneralALC')
import numpy as np
import gurobipy as gp
from gurobipy import GRB
from itertools import product
from math import sqrt
import node_methods as nmt
import pandas as pd

class node_0(): 
    def __init__(self):
        # 初始化
        self.mutipler_list = []
        self.penalty_list = []
        self.receive_list = []
        self.node_id = 0
    
    
    def decision_model(self):
        # 参数设置
        supply = dict({'Liverpool': 150000,
               'Brighton': 200000})

        through = dict({'Newcastle': 70000,
                'Birmingham': 50000,
                'London': 100000,
                'Exeter': 40000})

        demand = dict({'C1': 50000,
               'C2': 10000,
               'C3': 40000,
               'C4': 35000,
               'C5': 60000,
               'C6': 20000})


        arcs_fd,cost_fd = gp.multidict({
          ('Liverpool', 'Newcastle'): 0.5,
          ('Liverpool', 'Birmingham'): 0.5,
          ('Liverpool', 'London'): 1.0,
          ('Liverpool', 'Exeter'): 0.2,
          ('Brighton', 'Birmingham'): 0.3,
          ('Brighton', 'London'): 0.5,
          ('Brighton', 'Exeter'): 0.2})



        arcs_fc,cost_fc=gp.multidict({
          ('Liverpool', 'C1'): 1.0,
          ('Liverpool', 'C3'): 1.5,
          ('Liverpool', 'C4'): 2.0,
          ('Liverpool', 'C6'): 1.0,
          ('Brighton', 'C1'): 2.0,})
      
        arcs_dc,cost_dc=gp.multidict({
          ('Newcastle', 'C2'): 1.5,
          ('Newcastle', 'C3'): 0.5,
          ('Newcastle', 'C5'): 1.5,
          ('Newcastle', 'C6'): 1.0,
          ('Birmingham', 'C1'): 1.0,
          ('Birmingham', 'C2'): 0.5,
          ('Birmingham', 'C3'): 0.5,
          ('Birmingham', 'C4'): 1.0,
          ('Birmingham', 'C5'): 0.5,
          ('London', 'C2'): 1.5,
          ('London', 'C3'): 2.0,
          ('London', 'C5'): 0.5,
          ('London', 'C6'): 1.5,
          ('Exeter', 'C3'): 0.2,
          ('Exeter', 'C4'): 1.5,
          ('Exeter', 'C5'): 0.5,
          ('Exeter', 'C6'): 1.5})
        
        
        # 实例化模型
        m = gp.Model('SupplyNetworkDesign')
        
        # 变量设置
        factories = supply.keys()
        depots = through.keys()
        customers = demand.keys()
        flow_fc = m.addVars(arcs_fc,lb=0, name="flow_fc")
        flow_fd=m.addVars(arcs_fd,lb=0, name="flow_fd")
       

        # 约束设置
        factory_flow = m.addConstrs((gp.quicksum(flow_fc.select(factory, '*'))+gp.quicksum(flow_fd.select(factory, '*')) <= supply[factory]
                                 for factory in factories), name="factory_flow")
       

        # 目标设置
        flow_fd_list = np.array(list(flow_fd.values()))
        flow_fc_list = np.array(list(flow_fc.values()))
        coupling_send_list = np.array([np.array([],dtype=object),
                                  np.array([flow_fd_list],dtype=object),
                                  np.array([flow_fc_list],dtype=object)],
                                 dtype=object) 
        coupling_receive_list = np.array([np.array([],dtype=object),
                                  np.array([flow_fd_list],dtype=object),
                                  np.array([flow_fc_list],dtype=object)],
                                 dtype=object) 
        obj_augmented_penalty,self.receive_list,self.mutipler_list,self.penalty_list = nmt.penalty_function(coupling_receive_list,self.receive_list,self.mutipler_list,self.penalty_list,self.node_id)
        
        transport_cost = (gp.quicksum(flow_fd[arc] * cost_fd[arc] for arc in arcs_fd) +gp.quicksum(flow_fc[arc] * cost_fc[arc] for arc in arcs_fc))
        m.setObjective(transport_cost + obj_augmented_penalty, GRB.MINIMIZE)

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
  
        
        
