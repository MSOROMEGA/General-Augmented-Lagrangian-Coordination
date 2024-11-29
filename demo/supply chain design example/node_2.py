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

class node_2(): 
    def __init__(self):
        # 初始化
        self.mutipler_list = []
        self.penalty_list = []
        self.receive_list = []
        self.node_id = 2


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
      
      # Create a dictionary to capture shipping costs.
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
    
      
      # 模型实例化
      m = gp.Model('SupplyNetworkDesign')
        
        # 变量设置
      depots = through.keys()
      customers = demand.keys()
      factories = supply.keys()
      flow_fc = m.addVars(arcs_fc, lb=0, name="flow_fc")
      flow_dc=m.addVars(arcs_dc, lb=0, name="flow_dc")


        # 约束设置
      customers = demand.keys()
      customer_flow = m.addConstrs(((gp.quicksum(flow_fc.select('*', customer)))+(gp.quicksum(flow_dc.select('*', customer))) == demand[customer]
                                  for customer in customers), name="customer_flow")

        # 目标设置
      flow_fc_list = np.array(list(flow_fc.values()))
      flow_dc_list = np.array(list(flow_dc.values()))
      coupling_send_list = np.array([np.array([flow_fc_list],dtype=object),
                                  np.array([flow_dc_list],dtype=object),
                                  np.array([],dtype=object)],
                                 dtype=object) 
      coupling_receive_list = np.array([np.array([flow_fc_list],dtype=object),
                                  np.array([flow_dc_list],dtype=object),
                                  np.array([],dtype=object)],
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
    Node_2 = node_2() 
    Node_2.decision_model() 

       
        
        
