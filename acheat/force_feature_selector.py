#coding=utf-8
#author=godpgf

#重data_num-1开始，产生长度是len(selection)-cur_sel_index的全排列，返回最好的结果
def search_select(evl, selection, data_num, cur_sel_index):
    best_choose = data_num-1
    best_evl = 0
    for i in range(len(selection)-cur_sel_index-1,data_num):
        selection[cur_sel_index] = i
        if cur_sel_index < len(selection) -  1:
            search_select(evl, selection, i, cur_sel_index+1)
        cur_evl = evl(selection)
        if cur_evl > best_evl :
            best_choose = i
            best_evl = cur_evl
    selection[cur_sel_index] = best_choose
    return best_evl

def force_select(evl, sel_num, data_num):
    selection = []
    for i in range(sel_num):
        selection.append(i)
    if sel_num == data_num:
        return selection,evl(selection)

    best_evl = search_select(evl, selection, data_num, 0)
    return selection, best_evl

