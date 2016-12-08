#coding=utf-8
#author=godpgf


#cur_sel_index以后的元素已经是选得最优的，在cur_sel_index上尝试所有没有选过的元素，写入最好的
def search_select(evl, selection, data_num, cur_sel_index):
    s = set()
    for i in range(cur_sel_index+1,len(selection)):
        s.add(selection[i])
    best_choose = selection[cur_sel_index]
    best_evl = evl(selection)
    start_data = selection[cur_sel_index]+1
    for d in range(start_data,data_num):
        if not d in s:
            selection[cur_sel_index] = d
            cur_evl = evl(selection)
            if cur_evl > best_evl :
                best_evl = cur_evl
                best_choose = d
    selection[cur_sel_index] = best_choose
    return best_evl

def gready_select(evl, sel_num, data_num):
    selection = []
    for i in range(sel_num):
        selection.append(i)
    if sel_num == data_num:
        return selection,evl(selection)
    best_evl = 0.0
    for i in range(len(selection)-1,-1,-1):
        best_evl = search_select(evl, selection, data_num, i)
    return selection, best_evl
