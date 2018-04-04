#coding=utf-8
#author=godpgf
import random


class ActionNode(object):
    def __init__(self, act_id):
        self.act_id = act_id
        self.expect_return = 0
        self.first_child_id = -1
        self.next_brother_id = -1


def random_coff_feature_adj(eval, coff_num_list, feature_num_list, feature_size, epoch_num = 1024, lr = 0.1, step = 0.8, tired_coff = 0.016, exploration_rate = 0.1):
    pass