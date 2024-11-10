 

<h4 align="center">

 
[![PyPI Downloads](https://img.shields.io/pypi/dm/NepTrain?logo=pypi&logoColor=white&color=blue&label=PyPI)](https://pypi.org/project/NepTrain)
[![Requires Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white)](https://python.org/downloads)
 
</h4>

 
[pull request]: https://github.com/aboys-cb/NepTrain/pulls
[github issue]: https://github.com/aboys-cb/NepTrain/issues
[github discussion]: https://github.com/aboys-cb/NepTrain/discussions

 
## 安装

Python包索引[PyPI]中的版本始终是相对无bug的最新稳定版本，可以通过`pip安装`:

[pypi]: https://pypi.org/project/NepTrain

```sh
pip install NepTrain
```

如果你想在主分支上使用最新未发布的更改，你可以直接从GitHub安装:

```sh
pip install -U git+https://github.com/aboys-cb/NepTrain
```
### 社区支持

- [点击加入VASPTool群聊](https://qm.qq.com/q/wPDQYHMhyg)
- 通过issue提出问题和讨论交流

## 软件架构

建议使用 Python 3.10 以上版本。旧版本可能会报错类型错误。
推荐使用GPUMD3.9.5以上的版本。

 
## 使用方式

修改`vim ~/.NepTrain` 修改赝势文件路径,
如果没有这个文件，请任意执行一次`NepTrain init`

### 1. 初始化
首先先初始化下 会在当前目录下创建提交脚本
```sh
NepTrain init
```
```shell
(mysci) aboy@aboy:/mnt/d/Desktop/1$ NepTrain init
[2024-11-05 13:20:57.264180]-- 对于已有的文件我们选择跳过，如果需要强行生成覆盖，请使用-f 或者--force。
[2024-11-05 13:20:57.270163]-- 创建./structure，请将需要跑md的扩包结构放到该文件夹！
[2024-11-05 13:20:57.285512]-- 请检查sub_vasp.sh中的队列信息以及环境设置！
[2024-11-05 13:20:57.289824]-- 请检查sub_gpu.sh中的队列信息以及环境设置！
[2024-11-05 13:20:57.294086]-- 您需要检查修改job.yaml的vasp_job以及vasp.cpu_core。
[2024-11-05 13:20:57.294713]-- 同样需要检查修改job.yaml的gpumd主动学习的设置！
[2024-11-05 13:20:57.472578]-- 创建run.in，您可修改系综设置！温度和时间程序会修改！
[2024-11-05 13:20:57.478132]-- 初始化完成，您在检查好文件后，运行NepTrain train job.yaml即可
```
### 2. 制作训练集（可选）
针对结构或者结构文件生成微扰训练集

0.03的晶格形变+0.1的原子扰动
```sh
NepTrain perturb ./structure/Cs16Ag8Bi8I48.vasp --num 200 --cell 0.03 -d 0.1 -o train.xyz
```
### 3. 提交任务
在修改提交脚本以及任务配置后，在登陆节点运行以下命令即可
```sh
NepTrain train job.yaml
```
如果是后台运行 配合nohup即可
```sh
nohup NepTrain train job.yaml &
```
如果中途出现异常停止了，目录下有一个restart.yaml 执行以下命令即可
```sh
NepTrain train restart.yaml
```
## 以下是单独使用部分功能的命令demo
- 很多参数都是默认的可通过-h查看  比如`NepTrain vasp -h`

### 计算VASP单点能

```sh
NepTrain vasp demo.xyz -np 64 -g --kpoints 20  
```
如果想修改执行目录 输出目录 以及指定incar 参考以下命令
```sh
NepTrain vasp demo.xyz -np 64 --directory ./cache -g --incar=./INCAR --kpoints 20 -o ./result/result.xyz
```
 
### 执行主动学习
对./structure的结构跑300k、500k 10ps的md
```sh
NepTrain gpumd ./structure  -t 10 -T 300 500
```
更多细节参数执行`NepTrain gpumd -h`