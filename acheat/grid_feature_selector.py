#coding=utf-8
#author=godpgf
import random


def grid_select(evl, sel_num, data_num, max_fail_time = 32):
    selection = []
    selection_des = []
    selection_set = set()
    for i in xrange(sel_num):
        selection.append(i)
        selection_des.append("%d"%i)
    best_evl = evl(selection)
    if sel_num == data_num:
        return selection, best_evl
    fail_time = 0
    selection_set.add(','.join(selection_des))

    last_replace_index = -1
    while fail_time < max_fail_time:
        cur_replace_index = random.randint(0, sel_num-1)
        while cur_replace_index == last_replace_index:
            cur_replace_index = random.randint(0, sel_num - 1)
        last_replace_index = cur_replace_index
        last_replace_value = selection[cur_replace_index]
        best_feature_index = -1
        for i in xrange(data_num):
            if i != last_replace_value and i not in selection:
                selection[cur_replace_index] = i

                #判断是否出现过
                sorted_sel = sorted(selection)
                for j in xrange(sel_num):
                    selection_des[j] = "%d"%sorted_sel[j]
                des = ','.join(selection_des)
                if des in selection_set:
                    continue
                selection_set.add(des)

                cur_evl = evl(selection)
                if cur_evl > best_evl:
                    best_feature_index = i
                    best_evl = cur_evl

        if best_feature_index != -1:
            fail_time = 0
            selection[cur_replace_index] = best_feature_index
        else:
            fail_time += 1
            selection[cur_replace_index] = last_replace_value

    return selection, best_evl