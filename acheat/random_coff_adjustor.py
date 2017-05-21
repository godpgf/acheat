#coding=utf-8
#author=godpgf
import random

#coff_num_list保存的是每个参数的长度
#max_loop_time表示随机随机测试多少次找不到最大值就停止
def random_adjust(evl, coff_num_list, max_loop_time = 32):
    last_adj_index = -1
    cur_adj_index = -1
    best_evl = 0
    adjust_list = [random.randint(0,len(coff_num_list[i])-1) for i in range(len(coff_num_list))]
    remain_loop_time = max_loop_time
    while remain_loop_time > 0:
        --remain_loop_time
        while cur_adj_index == last_adj_index:
            cur_adj_index = random.randint(0, len(coff_num_list)-1) if len(coff_num_list) > 1 else 0
        last_adj_index = cur_adj_index
        best_coff_id = adjust_list[cur_adj_index]
        cur_coff_id = best_coff_id
        for i in range(coff_num_list[cur_adj_index]):
            adjust_list[cur_adj_index] = i
            cur_evl = evl(adjust_list)
            if cur_evl > best_evl:
                best_evl = cur_evl
                best_coff_id = i
        if best_coff_id != cur_coff_id:
            adjust_list[cur_adj_index] = best_coff_id
            remain_loop_time = max_loop_time
    return adjust_list, best_evl
