#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/25 13:37
# @Author  : 兵
# @email    : 1747193328@qq.com
"""
自动训练的逻辑
"""
import os.path

from ase.io import read as ase_read
from ase.io import write as ase_write
from ruamel.yaml import YAML

from NepTrain import utils
from NepTrain.core.train.worker import LocalWorker, SlurmWorker
from NepTrain.core.utils import check_env


class Manager:
    def __init__(self, options):
        self.options = options
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.options):
            self.index = 0
        value = self.options[self.index]
        self.index += 1
        return value

    def set_next(self, option):
        index=self.options.index(option)
        # 设置当前索引，注意索引从0开始
        if 0 <= index < len(self.options):
            self.index = index
        else:
            raise IndexError("Index out of range.")


class PathManager:



    def __init__(self, root):
        self.root = root

    def __getattr__(self, item):
        return os.path.join(self.root, item)




class NepTrainWorker:
    pass
    def __init__(self):
        self.config={}
        self.manager=Manager(["vasp","nep","gpumd" ])

    def get_worker(self):
        queue = self.config.get("queue", "local")
        if queue == "local":
            return LocalWorker()
        else:
            return SlurmWorker(os.path.abspath("./sub_vasp.sh"),os.path.abspath("./sub_gpu.sh"))

    def __getattr__(self, item):

        if item.startswith("last_"):
            item=item.replace("last_","")
            generation_path=os.path.join(os.path.abspath(self.config.get("work_path")), f"Generation-{self.generation-1}")
        else:
            generation_path=os.path.join(os.path.abspath(self.config.get("work_path")), f"Generation-{self.generation}")

        if item=="generation_path":

            return generation_path

        items= item.split("_")
        if items[0] in ["vasp","nep","gpumd"]:
            job_path=os.path.join(generation_path, items.pop(0))
        else:
            job_path=generation_path
        fin_path=os.path.join(job_path, "_".join(items[:-1]) )
        if items[-1]=="path":
            pass
            utils.verify_path(fin_path)
        else:
            last_underscore_index = fin_path.rfind('_')
            if last_underscore_index != -1:
                # 替换最后一个下划线为点
                fin_path = fin_path[:last_underscore_index] + '.' + fin_path[last_underscore_index + 1:]
            else:
                fin_path = fin_path

            utils.verify_path(os.path.dirname(fin_path))


        return fin_path



    @property
    def generation(self):
        return self.config.get("generation")
    @generation.setter
    def generation(self,value):
        self.config["generation"] = value



    def split_vasp_job_xyz(self,xyz_file):
        addxyz = ase_read(xyz_file, ":", format="extxyz")

        split_addxyz_list = utils.split_list(addxyz, self.config["vasp_job"])

        for i, xyz in enumerate(split_addxyz_list):
            if xyz:
                ase_write(self.__getattr__(f"vasp_learn_add_{i + 1}_xyz_file"), xyz, format="extxyz")

    def check_env(self):


        if self.generation!=1 or self.config.get("restart") :
            utils.print("无需初始化检查")
            return

        if self.config["current_job"]=="vasp":

            self.generation=0
            utils.copy(self.config["init_train_xyz"], self.vasp_learn_add_xyz_file)

            if self.config["vasp_job"] != 1:


                self.split_vasp_job_xyz(self.config["init_train_xyz"])
        elif self.config["current_job"]=="nep":
           

            utils.copy(self.config["init_train_xyz"], self.last_all_learn_calculated_xyz_file)
            # utils.copy(self.config["init_train_xyz"], self.last_all_learn_calculated_xyz_file )
            #如果势函数有效  直接先复制过来
        elif self.config["current_job"]=="gpumd":

            utils.copy(self.config["init_train_xyz"],self.nep_train_xyz_file )

            if os.path.exists(self.config["init_nep_txt"]):
                utils.copy(self.config["init_nep_txt"],
                            self.nep_nep_txt_file )
            else:
                raise FileNotFoundError("开始任务为gpumd必须指定有效的势函数路径！")
        else:
            raise ValueError("current_job 只能是nep,gpumd,vasp其中一个")

    def read_config(self,config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"{config_path}文件不存在")
        with open(config_path,"r",encoding="utf8") as f:


            self.config=YAML().load(f )




    def build_nep_params(self  ):
        nep=self.config["nep"]
        params=[]
        params.append("NepTrain")
        params.append("nep")

        params.append("--directory")
        params.append(self.nep_path)

        params.append("--in")
        params.append(os.path.abspath(nep.get("nep_in_path")))

        params.append("--train")
        params.append(self.last_improved_train_xyz_file)



        params.append("--test")
        params.append(os.path.abspath(nep.get("test_xyz_path")))


        if self.config["nep"]["nep_restart"] and self.generation not in [1,len(self.config["gpumd"]["step_times"])+1]:
            #开启续跑
            #如果上一级的势函数路径有效  就传入一下续跑的参数

            if os.path.exists(self.last_nep_nep_restart_file):
                utils.print_tip("开启续跑模式！")
                params.append("--restart_file")
                params.append(self.last_nep_nep_restart_file)
                params.append("--continue_step")
                params.append(str(self.config["nep"]["nep_restart_step"]))

        return " ".join(params)
    def build_gpumd_params(self,n_job=1):
        gpumd=self.config["gpumd"]
        params=[]
        params.append("NepTrain")
        params.append("gpumd")

        params.append(os.path.abspath(gpumd.get("model_path")))

        params.append("--directory")

        params.append(self.gpumd_path)

        params.append("--in")
        params.append(os.path.abspath(gpumd.get("run_in_path")))
        params.append("--nep")
        params.append( self.nep_nep_txt_file)
        params.append("--time")
        params.append(str(gpumd.get("step_times")[self.generation-1]))

        params.append("--temperature")

        params.append(" ".join([str(i) for i in gpumd["temperature_every_step"]]))


        params.append("--train")
        params.append( self.nep_train_xyz_file )
        params.append("--max_selected")
        params.append(str(gpumd["max_selected"]))
        params.append("--min_distance")
        params.append(str(gpumd["min_distance"]))
        params.append("--out")
        params.append(self.__getattr__(f"gpumd_learn_{n_job}_xyz_file"))
        if self.config.get("limit",{}).get("filter_by_bonds",True):
            params.append("--filter")



        return " ".join(params)

    def build_vasp_params(self,n_job=1):
        vasp=self.config["vasp"]
        params=[]
        params.append("NepTrain")
        params.append("vasp")

        if self.config["vasp_job"] == 1:

            if not os.path.exists(self.vasp_learn_add_xyz_file):
                return None
            params.append(self.vasp_learn_add_xyz_file)
        else:
            path=self.__getattr__(f"vasp_learn_add_{n_job}_xyz_file")
            if not os.path.exists(path):
                return None
            params.append(path)

        params.append("--directory")

        params.append(self.__getattr__(f"vasp_cache{n_job}_path"))


        params.append("-np")
        params.append(str(vasp["cpu_core"]))
        if vasp["kpoints_use_gamma"]:
            params.append("--gamma")

        if vasp["incar_path"]:

            params.append("--incar")
            params.append(os.path.abspath(vasp["incar_path"]))
        if vasp["use_k_stype"]=="kpoints":
            if vasp.get("kpoints"):
                params.append("-ka")
                if isinstance(vasp["kpoints"],list):
                    params.append(",".join([str(i) for i in vasp["kpoints"]]))
                else:
                    params.append(str(vasp["kpoints"]))
        else:

            if vasp.get("kspacing") :
                params.append("--kspacing")
                params.append(str(vasp["kspacing"]))
        params.append("--out")
        params.append( self.__getattr__(f"vasp_learn_calculated_{n_job}_xyz_file"))


        return " ".join(params)



    def sub_vasp(self):
        utils.print_msg("开始执行VASP计算单点能")
        if not utils.is_file_empty(self.vasp_learn_add_xyz_file):
            for i in range(self.config["vasp_job"]):
                cmd = self.build_vasp_params(i + 1)
                if cmd is None:
                    continue
                self.worker.sub_job(cmd, self.vasp_path, job_type="vasp")

            self.worker.wait()

            utils.cat(self.__getattr__(f"vasp_learn_calculated_*_xyz_file"),
                      self.all_learn_calculated_xyz_file

                      )
            if self.config.get("limit",{}).get("force") and not utils.is_file_empty(self.all_learn_calculated_xyz_file):
                bad_structure = []
                good_structure = []
                structures=ase_read(self.all_learn_calculated_xyz_file,":")
                for structure in structures:

                    if structure.calc.results["forces"].max() <= self.config.get("limit",{}).get("force"):
                        good_structure.append(structure)
                    else:
                        bad_structure.append(structure)

                ase_write(self.all_learn_calculated_xyz_file,good_structure,append=False,format="extxyz")
                if bad_structure:
                    ase_write(self.remove_by_force_xyz_file, bad_structure, append=False, format="extxyz")

        else:
            utils.print_warning("检测到计算输入文件为空，直接进入下一步！")

            utils.cat(self.vasp_learn_add_xyz_file,
                      self.all_learn_calculated_xyz_file


                      )
        self.generation += 1

    def sub_nep(self):
        utils.print_msg("--" * 10, f"开始训练第{self.generation}代势函数", "--" * 10)

        if not utils.is_file_empty(self.last_all_learn_calculated_xyz_file):


            if os.path.exists(self.last_nep_train_xyz_file):
                utils.cat([self.last_nep_train_xyz_file,
                           self.last_all_learn_calculated_xyz_file
                           ],
                          self.last_improved_train_xyz_file

                          )
            else:
                utils.copy(self.last_all_learn_calculated_xyz_file,
                            self.last_improved_train_xyz_file)
            utils.print_msg(f"开始训练势函数")
            cmd = self.build_nep_params()
            self.worker.sub_job(cmd, self.nep_path, job_type="nep")
            self.worker.wait()
        else:
            utils.print_warning("数据集没有变化，直接复制上一次的势函数！")

            utils.copy_files(self.last_nep_path, self.nep_path)

    def sub_gpumd(self):
        utils.print_msg(f"开始主动学习")

        cmd = self.build_gpumd_params()

        self.worker.sub_job(cmd, self.gpumd_path, job_type="gpumd")
        self.worker.wait()

        utils.cat(self.__getattr__(f"gpumd_learn_*_xyz_file"),
                  self.vasp_learn_add_xyz_file
                  )

        if utils.is_file_empty(self.vasp_learn_add_xyz_file):
            # 文件为空

            utils.print_warning("本轮主动学习添加结构为0！")

            return

        # break
        if self.config["vasp_job"] != 1:
            # 这里分割下xyz 方便后面直接vasp计算
            self.split_vasp_job_xyz(self.vasp_learn_add_xyz_file)


    def start(self,config_path):
        utils.print_msg("欢迎使用NepTrain自动训练！")

        self.read_config(config_path)
        self.check_env()
        #首先创建一个总的路径
        #然后先
        self.worker=self.get_worker()

        self.manager.set_next(self.config.get("current_job"))

        while True:

            #开始循环
            job=next(self.manager)
            self.config["current_job"]=job
            self.save_restart()
            if job=="vasp":

                self.sub_vasp()

            elif job=="nep":

               self.sub_nep()
               if self.generation>len(self.config["gpumd"]["step_times"]):
                   utils.print_success("训练结束！")
                   break

            else:
                self.sub_gpumd()


    def save_restart(self):
        with open("./restart.yaml","w",encoding="utf-8") as f:
            self.config["restart"]=True

            YAML().dump(self.config,f)

def train_nep(argparse):
    """
    首先检查下当前的进度 看从哪开始
    :return:
    """
    check_env()

    worker = NepTrainWorker()
    # worker.start("..//core/train/job.json")
    worker.start(argparse.config_path)
if __name__ == '__main__':
    train =NepTrainWorker()
    train.generation=1
    train.config["work_path"]="./cache"
    print(train.nep_path)

    print(train.__getattr__(f"vasp_learn_calculated_*_xyz_file"))
