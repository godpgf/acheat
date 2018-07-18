#coding=utf-8
#author=godpgf
import random


def grid_select(evl, data_num_list, max_fail_time = 32):
    selection = []
    selection_des = []
    selection_set = set()
    all_data_cnt = 1
    for i in range(len(data_num_list)):
        all_data_cnt *= data_num_list[i]
        selection.append(0)
        selection_des.append("%d"%0)
    best_evl = evl(selection, -1, -1)
    if all_data_cnt == 1:
        return selection, best_evl
    fail_time = 0
    selection_set.add(','.join(selection_des))

    last_replace_index = -1
    while fail_time < max_fail_time:
        cur_replace_index = random.randint(0, len(data_num_list)-1)
        while cur_replace_index == last_replace_index:
            cur_replace_index = random.randint(0, len(data_num_list) - 1)
        last_replace_index = cur_replace_index
        last_replace_value = selection[cur_replace_index]
        best_feature_index = -1
        data_num = data_num_list[cur_replace_index]
        for i in range(data_num):
            if i != last_replace_value and i not in selection:
                selection[cur_replace_index] = i

                #判断是否出现过
                # sorted_sel = sorted(selection)
                for j in range(len(data_num_list)):
                    selection_des[j] = "%d"%selection[j]
                des = ','.join(selection_des)
                if des in selection_set:
                    continue
                selection_set.add(des)

                cur_evl = evl(selection, cur_replace_index, best_evl)
                if cur_evl > best_evl:
                    best_feature_index = i
                    best_evl = cur_evl

        if best_feature_index != -1:
            fail_time = 0
            selection[cur_replace_index] = best_feature_index
        else:
            fail_time += 1
            selection[cur_replace_index] = last_replace_value
    evl(selection, -1, best_evl)

    return selection, best_evl