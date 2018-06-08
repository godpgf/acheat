#coding=utf-8
#author=godpgf

import numpy as np
import random

def get_score_percent(scores):
    return 1.0 / (1.0 + np.exp(-scores))
def refresh_score_percent(scores,choose_index,last_index):
    --scores[last_index]
    ++scores[choose_index]
    return  get_score_percent(scores)

#累加所有没有选择的数据的概率,这个概率受到已经选择的元素影响(和已经选择的元素关联大的将概率小)
def sum_percent(relation_table, selection, sel_num, score_percent):
    s = set(selection)
    sum = 0.0
    relation_percent = []
    for i in range(len(score_percent)):
        relation_percent.append(1)
        if not i in s:
            for j in range(sel_num):
                relation_percent[i] *= (1 - relation_table[i][selection[j]])
            sum += relation_percent[i] * score_percent[i]
    return sum, relation_percent

#产生一个随机数,从没有选择的数据中选择一个
def select(cur_percent, score_percent, relation_percent, selection):
    s = set(selection)
    for i in range(len(score_percent)):
        if not i in s:
            cur_percent -= score_percent[i] * relation_percent[i]
            if cur_percent < 0:
                return i
    return -1

#随机选择一个已经选过的元素,把它放在末尾,再随机选择一个没选过的元素返回
def random_swap(selection,score_percent,relation_table):
    sel_num = len(selection)
    sel_index = random.randint(0,sel_num-1)
    if sel_index != sel_num-1 :
        selection[sel_index],selection[sel_num-1] = selection[sel_num-1], selection[sel_index]
    #s = set(selection)
    sp, rp = sum_percent(relation_table,selection,sel_num-1,score_percent)
    cur_percent = random.uniform(0,sp)
    return select(cur_percent, score_percent,rp,selection)

def search_best_select(evl, selection, cur_evl, scores, score_percent, relation_table, cur_depth, max_fail_time, fail_continue_percent):
    remain_time = max_fail_time[cur_depth]
    search_depth = len(max_fail_time)
    while remain_time > 0:
        remain_time = remain_time - 1
        choose_index = random_swap(selection, score_percent,relation_table)
        lase_index = selection[len(selection)-1]
        #尝试选择
        selection[len(selection)-1]=choose_index
        evl_value = evl(selection)
        if evl_value > cur_evl :#如果尝试的选择效果好
            #更新数据评分
            score_percent = refresh_score_percent(scores,choose_index,lase_index)
            #清空次数计数器，再测试
            cur_evl = evl_value
            remain_time = max_fail_time[cur_depth]
        else :#如果尝试的选择效果不好
            if cur_depth + 1 == search_depth:
                selection[len(selection) - 1] = lase_index
                continue
            #选择效果不好,有一定概率接着不好的选择继续尝试
            if random.uniform(0,1) < fail_continue_percent:
                scale = (search_depth - cur_depth - 1.0) / search_depth
                new_selection = selection[:]
                evl_value = search_best_select(evl, new_selection, cur_evl, scores, score_percent, relation_table, cur_depth+1, max_fail_time,fail_continue_percent*scale)
                if evl_value > cur_evl :#如果尝试的选择效果好
                    #更新数据评分
                    score_percent = refresh_score_percent(scores,choose_index,lase_index)
                    #清空次数计数器，再测试
                    cur_evl = evl_value
                    remain_time = max_fail_time[cur_depth]
                    #更新选择
                    for i in range(len(selection)):
                        selection[i] = new_selection[i]
                else:#如果效果还是不好,恢复之前选择,并更新评分
                    selection[len(selection)-1] = lase_index
                    score_percent = refresh_score_percent(scores,lase_index,choose_index)
            else:
                selection[len(selection)-1] = lase_index
                score_percent = refresh_score_percent(scores,lase_index,choose_index)
    return cur_evl

#随机选择一些参数,返回最大评估值和当前的选择
#evl:评估值
#score:每个数据的得分
#relation_table:数据相关联程度
#search_depth:错误方向上继续搜索的最大深度
#max_fail_time:最多失败次数
#fail_continue_percent:错误方向上继续尝试概率
def random_select(evl, sel_num, scores, relation_table,  max_fail_time, fail_continue_percent):
    selection = []
    if sel_num == len(scores):
        for i in range(sel_num):
            selection.append(i)
        return selection,evl(selection)

    #初始化
    score_percent = get_score_percent(scores)

    for i in range(sel_num):
        #s = set(selection)
        sp, rp = sum_percent(relation_table,selection,len(selection),score_percent)
        cur_percent = random.uniform(0,sp)
        cur_index = select(cur_percent, score_percent,rp,selection)
        selection.append(cur_index)

    cur_evl = evl(selection)
    evl_value = search_best_select(evl,selection,cur_evl,scores,score_percent,relation_table,0,max_fail_time,fail_continue_percent)

    return selection, evl_value