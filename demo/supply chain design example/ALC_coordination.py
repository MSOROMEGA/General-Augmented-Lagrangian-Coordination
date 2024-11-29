# -*- coding: utf-8 -*-
#制作不易，转载请注明出处
#出处：黄海南(Hainan Huang), hhn0113@outlook.com
import sys
sys.path.append('GeneralALC')
import numpy as np
import node_0, node_1, node_2 
import alc_methods as amt

def run_alc(node_list, node_sequnce, Algorithm, outerloop_num, inner_loop_num, inner_loop_threshold, outer_loop_threshold, outer_loop_consisitency_threshold, beta, w0=1,v0=0,cpl0=0,c_old=[], obj_old=10000000000, inner_loop_count=0):    
    print('初始化中...')
    amt.alc_init(node_list,w0,v0,cpl0)
    print('初始化完成！')
    for o in range(outerloop_num):
        for i in range(inner_loop_num):
            obj_now = amt.inner_loop_coordination(node_list,node_sequnce)
            inner_loop_count+=1
            # 收敛判断
            print('  obj:',obj_now)
            if np.abs(obj_now - obj_old) / (np.abs(obj_now) + 1) <= inner_loop_threshold:
                print('🟢🟢🌛🌛内循环收敛,迭代次数为：{}🌛🌛🟢🟢'.format(i + 1), end='')
                break
            elif i==inner_loop_num-1:
                print('🔴🔴🌛🌛最大迭代{}次后，内循环任未收敛🌛🌛🔴🔴'.format(i + 1), end='')
                break
            obj_old = obj_now
        c_alllist,c_old_alllist,c_old = Algorithm.algorithm(node_list,o,beta,c_old)   
        # 收敛判断
        fseable_convergence = np.linalg.norm(c_alllist)
        alm_convergence = np.linalg.norm(c_alllist - c_old_alllist)
        print("    外环次数：",o,"  内环次数：",inner_loop_count,"  obj：",obj_now ,"  外环收敛1：",alm_convergence, "  外环收敛2：", fseable_convergence, '\n')
        if alm_convergence <= outer_loop_threshold:
            if fseable_convergence<=outer_loop_consisitency_threshold:
                print('🟢🟢☀️☀️外循环收敛,迭代次数为：{}☀️☀️🟢🟢'.format(o+1))
                break
        if o==outerloop_num-1:
            print('🔴🔴☀️☀️最大迭代{}次后，外循环任未收敛☀️☀️🔴🔴'.format(o+1))
            break
            

# 导入模型
node_0,node_1,node_2 = node_0.node_0(),node_1.node_1(),node_2.node_2()
node_sequnce = [2,1,0]
node_list = [eval('node_{}'.format(i)) for i in node_sequnce]

# 运行ALC
run_alc(node_list, 
        node_sequnce, 
        Algorithm = amt.ALC_ORGIN(), 
        outerloop_num = 300, 
        inner_loop_num = 10, 
        inner_loop_threshold = 0.0001, 
        outer_loop_threshold = 0.0001, 
        outer_loop_consisitency_threshold = 0.001, 
        beta = 1, 
        w0 = 0.0005,
        v0 = 0,
        cpl0 = 0,
        )
