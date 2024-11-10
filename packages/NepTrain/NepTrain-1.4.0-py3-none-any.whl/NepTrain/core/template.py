#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/25 18:12
# @Author  : 兵
# @email    : 1747193328@qq.com
import os.path

from ase.io import read as ase_read
from ruamel.yaml import YAML
from NepTrain import module_path, utils
from NepTrain.core.utils import check_env


def create_vasp(force):
    if   os.path.exists("./sub_vasp.sh") and not force:
        return
    utils.print_warning("请检查sub_vasp.sh中的队列信息以及环境设置！")

    sub_vasp="""#! /bin/bash
#SBATCH --job-name=NepTrain
#SBATCH --nodes=1
#SBATCH --partition=cpu
#SBATCH --ntasks-per-node=64
#这里可以放一些加载环境的命令

#例如conda activate NepTrain
#这里主要是为了直接传参
$@ 
#实际执行的脚本应该如下
#具体参数含义可以执行NepTrain vasp -h 查看
#NepTrain vasp demo.xyz -np 64 --directory ./cache -g --incar=./INCAR --kpoints 35 -o ./result/result.xyz 
"""

    with open("./sub_vasp.sh", "w",encoding="utf8") as f:
        f.write(sub_vasp)


def create_nep(force):
    if os.path.exists("./sub_gpu.sh") and not force:
        return
    utils.print_warning("请检查sub_gpu.sh中的队列信息以及环境设置！")

    sub_vasp = """#! /bin/bash
#SBATCH --job-name=NepTrain-gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=gpu-a800
#SBATCH --gres=gpu:1
#这里可以放一些加载环境的命令
 
$@ """
    with open("./sub_gpu.sh", "w", encoding="utf8") as f:
        f.write(sub_vasp)



def init_template(argparse):
    if not argparse.force:
        utils.print_tip("对于已有的文件我们选择跳过，如果需要强行生成覆盖，请使用-f 或者--force。")

    if not os.path.exists("./structure"):
        os.mkdir("./structure")
        utils.print_tip("创建./structure，请将需要跑md的扩包结构放到该文件夹！" )
    check_env()
    create_vasp(argparse.force)
    create_nep(argparse.force)
    if not os.path.exists("./job.yaml") or argparse.force:
        utils.print_tip("您需要检查修改job.yaml的vasp_job以及vasp.cpu_core。")
        utils.print_warning("同样需要检查修改job.yaml的gpumd主动学习的设置！")

        with open(os.path.join(module_path,"core/train/job.yaml"),"r",encoding="utf8") as f:

            config = YAML().load(f  )

        if os.path.exists("train.xyz"):
            #检查下第一个结构有没有计算
            atoms=ase_read("./train.xyz",0,format="extxyz")

            if not (atoms.calc and "energy"   in atoms.calc.results):
                config["current_job"]="vasp"
                utils.print_warning("检查train.xyz的第一个结构没有计算，将初始任务设置为vasp！")
        else:
            utils.print_warning("检测到当前目录下并没有train.xyz，请检查目录结构！")
            utils.print_tip("如果有训练集但文件名不叫train.xyz，请统一job.yaml")


        with open("./job.yaml","w",encoding="utf8") as f:
            YAML().dump(config,f  )
    else:

        #已经存在 如果执行init  更新下
        with open(os.path.join(module_path, "core/train/job.yaml"), "r", encoding="utf8") as f:

            base_config = YAML().load(f)
        with open("./job.yaml","r",encoding="utf8") as f:
            user_config = YAML().load(f)
        job=utils.merge_yaml(base_config,user_config)


        with open("./job.yaml","w",encoding="utf8") as f:
            YAML().dump(job,f  )


    if not os.path.exists("./run.in")  or argparse.force:
        utils.print_tip("创建run.in，您可修改系综设置！温度和时间程序会修改！")

        utils.copy(os.path.join(module_path,"core/gpumd/run.in"),"./run.in")

    utils.print_success("初始化完成，您在检查好文件后，运行NepTrain train job.yaml即可")
