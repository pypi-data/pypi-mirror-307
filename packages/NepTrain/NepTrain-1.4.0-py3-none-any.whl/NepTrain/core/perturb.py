#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/25 18:12
# @Author  : 兵
# @email    : 1747193328@qq.com
import os

from ase import Atoms
from ase.io import write as ase_write

from NepTrain import utils
from ._hiphive import generate_mc_rattled_structures


@utils.iter_path_to_atoms(["*.vasp","*.xyz"],description="正在生成微扰结构" )
def perturb(atoms:Atoms,cell_pert_fraction=0.04,rattle_std=0.04,min_distance=0.1,num=50):





    structures_mc_rattle = generate_mc_rattled_structures(
        atoms,num,  cell_pert_fraction,rattle_std, min_distance, n_iter=20)

    for structure in structures_mc_rattle:
        structure.info['Config_type'] = f"hiphive mc perturb {cell_pert_fraction} {rattle_std} {min_distance}"
    return structures_mc_rattle
def run_perturb(argparse):

    result = perturb(argparse.model_path,
                     cell_pert_fraction=argparse.cell_pert_fraction,
                     min_distance=argparse.min_distance,
                     rattle_std=argparse.rattle_std,
                     num=argparse.num,
                     )
    path=os.path.dirname(argparse.out_file_path)

    if path and  not os.path.exists(path):
        os.makedirs(path)

    ase_write(argparse.out_file_path,[atom for _list in result for atom in _list],format="extxyz",append=argparse.append)
