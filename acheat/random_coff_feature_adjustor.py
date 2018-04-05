#coding=utf-8
#author=godpgf
import random
import sys
import math
from .random_feature_selector import random_select

class ActionTree(object):
    def __init__(self):
        self.nodes = []

    def __getitem__(self, index):
        return self.nodes[index]

    def create_node(self, act_id = -1):
        self.nodes.append(ActionNode(act_id))
        return len(self.nodes-1)

    def get_child_num(self, node_id):
        child_id = self.nodes[node_id].first_child_id
        child_num = 0
        while child_id >= 0:
            child_num += 1
            child_id = self.nodes[child_id].next_brother_id
        return child_num

    def get_child(self, node_id, child_index):
        child_id = self.nodes[node_id].first_child_id
        while child_index > 0:
            child_index -= 1
            child_id = self.nodes[child_id].next_brother_id
        return child_id

    def add_child(self, node_id, child_id):
        self[child_id].pre_id = node_id
        if self[node_id].first_child_id == -1:
            self[node_id].first_child_id = child_id
        else:
            pre_child_id = self[node_id].first_child_id
            while self[pre_child_id].next_brother_id != -1:
                pre_child_id = self[pre_child_id].next_brother_id
            self[pre_child_id].next_brother_id = child_id
            self[child_id].pre_brother_id = pre_child_id

    def random_choose_act(self, node_id, max_act_num, exploration_rate):
        child_num = self.get_child_num(node_id)

        sum_r = 0
        sqr_sum_r = 0
        min_r = sys.float_info.max

        for child_index in xrange(child_num):
            r = self[self.get_child(node_id, child_index)].expect_return
            sum_r += r
            sqr_sum_r += r * r
            min_r = min(min_r, r)

        avg_r = 0 if child_num == 0 else sum_r / child_num
        std_r = 0 if child_num == 0 else math.sqrt(sqr_sum_r / child_num - avg_r * avg_r)
        min_weight = 1 if child_num == 0 else std_r * exploration_rate

        choose_weight = [min_weight] * max_act_num
        all_weight = min_weight * max_act_num
        for child_index in  xrange(child_num):
            child_id = self.get_child(node_id, child_index)
            delta_r = self[child_id].expect_return - min_r
            choose_weight[self[child_id].act_id] += delta_r
            all_weight += delta_r

        all_weight *= random.random()
        for id, weight in enumerate(choose_weight):
            all_weight -= weight
            if all_weight <= 0:
                return id
        return len(choose_weight) - 1

    def act_2_child(self, node_id, act_id):
        for i in xrange(self.get_child_num(node_id)):
            if self[i].act_id == act_id:
                return self.get_child(node_id, i)
        return None

class ActionNode(object):
    def __init__(self, act_id):
        self.act_id = act_id
        self.expect_return = 0
        self.pre_id = -1
        self.first_child_id = -1
        self.pre_brother_id = -1
        self.next_brother_id = -1


def random_coff_feature_adj(evl, coff_num_list, feature_num_list, scores, relation_table,  max_fail_time, fail_continue_percent, epoch_num = 1024, lr = 0.1, step = 0.8, tired_coff = 0.016, exploration_rate = 0.1):
    tree = ActionTree()
    root_id = tree.create_node()

    max_reward = 0
    best_choose_list = None
    best_selection = None

    while epoch_num > 0:
        cur_id = root_id
        choose_list = []

        for coff_num in coff_num_list:
            act_id = tree.random_choose_act(cur_id, coff_num, exploration_rate)
            child_id = tree.act_2_child(cur_id, act_id)
            if child_id:
                cur_id = child_id
            else:
                child_id = tree.create_node(act_id)
                tree.add_child(cur_id, child_id)
                cur_id = child_id
            choose_list.append(act_id)

        act_id = tree.random_choose_act(cur_id, len(feature_num_list), exploration_rate)
        child_id = tree.act_2_child(cur_id, act_id)
        if child_id:
            cur_id = child_id
        else:
            child_id = tree.create_node(act_id)
            tree.add_child(cur_id, child_id)
            cur_id = child_id

            sel_num = feature_num_list[act_id]

            def sel_evl(sel):
                return evl(choose_list, sel)

            selection, tree[cur_id].expect_return = random_select(sel_evl, sel_num, scores, relation_table, max_fail_time, fail_continue_percent)

            if tree[cur_id].expect_return > max_reward:
                max_reward = tree[cur_id].expect_return
                best_choose_list = choose_list
                best_selection = selection

        pre_id = tree[cur_id].pre_id
        cur_leaf_id = cur_id
        while pre_id != -1:
            child_num = tree.get_child_num(pre_id)
            r = 0
            next_r = -sys.float_info.max
            for child_index in xrange(child_num):
                next_r = max(next_r, tree[tree.get_child(pre_id, child_index)].expect_return)
            tree[pre_id].expect_return += lr * (r + step * next_r  - tree[pre_id].expect_return)
            cur_leaf_id = pre_id
            pre_id = tree[cur_leaf_id].pre_id
        tree[cur_leaf_id].expect_return -= tired_coff
        epoch_num -= 1
    return best_choose_list, best_selection, max_reward