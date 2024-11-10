#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/29 19:52
# @Author  : 兵
# @email    : 1747193328@qq.com
import os

import numpy as np
from ase.io import read as ase_read
from calorine.nep import get_descriptors
from matplotlib import pyplot as plt

from scipy.spatial.distance import cdist



# 从pynep复制的最远点采样 就使用这一个函数 因为安装不方便
def select(new_data, now_data=[], min_distance=None, min_select=1, max_select=None):
    """Select those data fartheset from given data

    Args:
        new_data (2d list or array): A series of points to be selected
        now_data (2d list or array): Points already in the dataset.
            Defaults to []. (No existed data)
        min_distance (float, optional):
            If distance between two points exceeded the minimum distance, stop the selection.
            Defaults to None (use the self.min_distance)
        min_select (int, optional): Minimal numbers of points to be selected. This may cause
            some distance between points less than given min_distance.
            Defaults to 1.
        max_select (int, optional): Maximum numbers of points to be selected.
            Defaults to None. (No limitation)

    Returns:
        A list of int: index of selected points
    """
    metric = 'euclidean'
    metric_para = {}
    min_distance = min_distance
    max_select = max_select or len(new_data)
    to_add = []
    if len(new_data) == 0:
        return to_add
    if len(now_data) == 0:
        to_add.append(0)
        now_data.append(new_data[0])
    distances = np.min(cdist(new_data, now_data, metric=metric, **metric_para), axis=1)

    while np.max(distances) > min_distance or len(to_add) < min_select:
        i = np.argmax(distances)
        to_add.append(i)
        if len(to_add) >= max_select:
            break
        distances = np.minimum(distances, cdist([new_data[i]], new_data, metric=metric)[0])
    return to_add




def select_structures(train, new_atoms ,nep_path, max_selected=20, min_distance=0.01 ):
    # 首先去掉跑崩溃的结构


    train_des = np.array([np.mean(get_descriptors(i, nep_path), axis=0) for i in train])


    new_des = np.array([np.mean(get_descriptors(i, nep_path), axis=0) for i in new_atoms])

    selected_i = select(np.vstack([train_des, new_des]), train_des, min_distance=min_distance, max_select=max_selected,
                        min_select=0)



    return [new_atoms[i - train_des.shape[0]] for i in selected_i]

# 加速计算每对元素的最小键长
def compute_min_bond_lengths(atoms ):
    # 获取原子符号
    dist_matrix = atoms.get_all_distances()

    symbols = atoms.get_chemical_symbols()

    # 提取上三角矩阵（排除对角线）
    i, j = np.triu_indices(len(atoms), k=1)

    # 用字典来存储每种元素对的最小键长
    bond_lengths = {}

    # 遍历所有原子对，计算每一对元素的最小键长
    for idx in range(len(i)):
        atom_i, atom_j = symbols[i[idx]], symbols[j[idx]]
        # if atom_i==atom_j:
        #     continue
        # 获取当前键长
        bond_length = dist_matrix[i[idx], j[idx]]
        # if bond_length>5:
        #     continue
        # 确保元素对按字母顺序排列，避免 Cs-Ag 和 Ag-Cs 视为不同
        element_pair = tuple(sorted([atom_i, atom_j]))

        # 如果该元素对尚未存在于字典中，初始化其最小键长
        if element_pair not in bond_lengths:
            bond_lengths[element_pair] = bond_length
        else:
            # 更新最小键长
            bond_lengths[element_pair] = min(bond_lengths[element_pair], bond_length)

    return bond_lengths



def process_trajectory(trajectory):
    # 读取轨迹文件（假设为 xyz 格式）


    # 存储所有帧的结果
    all_bond_lengths = []

    # 遍历轨迹中的每一帧
    for atoms in trajectory:
        # 获取当前帧的距离矩阵

        # 计算当前帧的最小键长
        bond_lengths = compute_min_bond_lengths(atoms )
        all_bond_lengths.append(bond_lengths)

    return all_bond_lengths

def filter_by_bonds(trajectory,model):
    good_structure=[]
    bad_structure=[]
    base_bond=compute_min_bond_lengths(model )
    bonds=process_trajectory(trajectory)
    for index,bond in enumerate(bonds):
        # print(bond)
        # condition = [utils.radius_table[a]+utils.radius_table[b] > a_b for (a,b),a_b in bond.items()]

        condition = [base_bond.get(key,0)*0.6 > a_b for key,a_b in bond.items()]
        # print(condition)
        if any(condition):
            bad_structure.append(trajectory[index])
        else:
            good_structure.append(trajectory[index])
    return good_structure, bad_structure