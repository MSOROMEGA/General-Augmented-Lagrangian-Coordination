# -*- coding: utf-8 -*-
#制作不易，转载请注明出处
#出处：黄海南(Hainan Huang), hhn0113@outlook.com
import sys
sys.path.append('GeneralALC')
import numpy as np
import node_0, node_1, node_2 
import alc_methods as amt

def run_alc(node_list, node_sequnce, Algorithm, outerloop_num, inner_loop_num, inner_loop_threshold, outer_loop_threshold, outer_loop_consisitency_threshold, beta, w0=1,v0=0,cpl0=0,c_old=[], obj_old=10000000000, inner_loop_count=0):    
    # 初始化运行
    print('初始化中...')
    amt.alc_init(node_list,w0,v0,cpl0)
    print('初始化完成！')
    # ALC迭代开始
    # 外循环
    for o in range(outerloop_num):
        # 内循环
        for i in range(inner_loop_num):
            # 单次内循环协调,返回当前网络(所有节点加总)的目标值
            obj_now = amt.inner_loop_coordination(node_list,node_sequnce)
            # 内循环数量计数
            inner_loop_count+=1
            #内循环收敛条件
            print('  obj:',obj_now)
            if np.abs(obj_now - obj_old) / (np.abs(obj_now) + 1) <= inner_loop_threshold:
                print('🟢🟢🌛🌛内循环收敛,迭代次数为：{}🌛🌛🟢🟢'.format(i + 1), end='')
                break
            elif i==inner_loop_num-1:
                print('🔴🔴🌛🌛最大迭代{}次后，内循环任未收敛🌛🌛🔴🔴'.format(i + 1), end='')
                break
            obj_old = obj_now
        # 更新乘子和惩罚因子
        c_alllist,c_old_alllist,c_old = Algorithm.algorithm(node_list,o,beta,c_old)   
        # 收敛判断
        fseable_convergence = np.linalg.norm(c_alllist)
        alm_convergence = np.linalg.norm(c_alllist - c_old_alllist)
        print("    外环次数：",o,"  内环次数：",inner_loop_count,"  obj：",obj_now ,"  外环收敛1：",alm_convergence, "  外环收敛2：", fseable_convergence, '\n')
        if alm_convergence <= outer_loop_threshold:#保证收敛；
            if fseable_convergence<=outer_loop_consisitency_threshold:#保证可行解
                print('🟢🟢☀️☀️外循环收敛,迭代次数为：{}☀️☀️🟢🟢'.format(o+1))
                break
        if o==outerloop_num-1:
            print('🔴🔴☀️☀️最大迭代{}次后，外循环任未收敛☀️☀️🔴🔴'.format(o+1))
            break
            

# 初始参数
outerloop_num = 300 # 外循环最大迭代次数
inner_loop_num = 10 # 内循环最大迭代次数
inner_loop_threshold = 0.0001 # 内循环两次迭代目标收敛阈值
outer_loop_threshold = 0.0001 # 外循环两次迭代目标收敛阈值
outer_loop_consisitency_threshold = 0.0001 #外循环一致性收敛阈值
beta=2 # 惩罚系数增量的初始值
w0=1 # 惩罚系数(增广)的初始值
v0=0 # 乘子的初始值
cpl0=0 # 耦合变量的初始值 
# 选择协调算法，最经典算法，Tosserams, S., Etman, L. F. P., & Rooda, J. E. (2008). Augmented Lagrangian coordination for distributed optimal design in MDO. International Journal for Numerical Methods in Engineering, 73(13), 1885–1910. https://doi.org/10.1002/nme.2158
Algorithm = amt.ALC_ORGIN()
# 节点实例化,导入模型
node_0,node_1,node_2 = node_0.node_0(),node_1.node_1(),node_2.node_2()
# 设置协调顺序，这里是先求解node_2，再求解node_1，最后求解node_0
node_sequnce = [2,1,0]
node_list = [eval('node_{}'.format(i)) for i in node_sequnce]

# 运行协调算法，如果没有特殊的需求的话，可以不用改变这里的参数
run_alc(node_list, node_sequnce, Algorithm, outerloop_num, inner_loop_num, inner_loop_threshold, outer_loop_threshold, outer_loop_consisitency_threshold, beta, w0,v0,cpl0)
