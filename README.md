# oekolopoly-rl  [![Python 3.8](https://upload.wikimedia.org/wikipedia/commons/a/a5/Blue_Python_3.8_Shield_Badge.svg)](https://upload.wikimedia.org/wikipedia/commons/a/a5/Blue_Python_3.8_Shield_Badge.svg)
A repository aimed at performing different RL-Algorithms on the custom environment [Oekolopoly](https://github.com/cherrisimo/oekolopoly) using [RL-Baselines3-Zoo](https://github.com/DLR-RM/rl-baselines3-zoo) Framework.

## Repo structure overview

* [oekolopoly](https://github.com/cherrisimo/oekolopoly-rl/tree/main/oekolopoly) contains the Oekolopoly environment with following differences:
  * The observation space no longer contains the flag valid_turn as it brings no information for the state of the environment and is better to be stored in a variable within the step function
  * Assertions have been added instead of some if-statements for consistency and better readability 
  * Multiply render functions have been added to showcase the gameplay of agents
* [oekolopoly_agents](https://github.com/cherrisimo/oekolopoly-rl/tree/main/oekolopoly_agents) carries zip folders with trained agents grouped by the algorithm they've been trained with.
 
## Installing

Python 3.8 is needed for the module [pytype](https://github.com/cherrisimo/pytype).

Create a new environment with tensorflow and the required Python version installed as followed:

```shell
conda create -n env_name tensorflow python=3.8
```

or install tensorflow in an existing one:

```shell
conda install -c anaconda tensorflow
```

Activate environment and install pytype, pybullet and box2dpy:

```shell
conda activate env_name
conda install -c forge pytype
conda install -c forge pybullet
conda install -c forge box2d-py
```

Install git:
```shell
conda install git
```

RL-Baselines3-Zoo contains in itself further repositories. One of them contains the over 100+ trained agents. The argument `--recursive` is used to clone them as well.

Clone respective repository with its sub-repos:
```shell
git clone --recursive https://github.com/DLR-RM/rl-baselines3-zoo
```

In the repository folder execute following command:

```shell
cd rl-baselines3-zoo
pip install -r requirements.txt
```

## Usage

Add custom environment to `utils/import_envs.py` using:

```python
try:
    import oekolopoly
except ImportError:
    oekolopoly = None
```

Configure hyperparameters in `rl-baselines3-zoo/hyperparams/ppo.yml` as shown below:

```python
OekolopolyBox-v0:
  n_envs: 8
  n_timesteps: 4000
  policy: 'MlpPolicy'
  n_steps: 32
  batch_size: 256
  gae_lambda: 0.8
  gamma: 0.98
  n_epochs: 20
  ent_coef: 0.0
  learning_rate: lin_0.001
  clip_range: lin_0.2
```

If custom environment is not yet installed, now it can be done:

```
pip install -e .
```

Optionally create a folder to store each trained agent. A further folder named after the used algorithm for the trained agent should reside in it as shown here:

```
├── oekolopoly_agents
│   └── ppo
│       ├── OekolopolyBox-v0_1
│       └── ...
└── logs
    └── benchmark
    └── ppo
    └── ...
```

Train an agent:

```shell
python train.py --algo ppo --env OekolopolyBox-v0 -f oekolopoly_agents
```
* `--algo`: specifies the algorithm to be executed
* `--env`: name of environment
* `-f`: save agent to the wished folder, if not defined logs is used as the default path

Train a certain agent more:

```shell
python train.py --algo ppo --env OekolopolyBox-v0 -i oekolopoly_agents/ppo/OekolopolyBox-v0_1/OekolopolyBox-v0.zip
```
* `-i`: path to the particular agent

See trained agent in action using:

```shell
python enjoy.py --algo ppo --env OekolopolyBox-v0 -f oekolopoly_agents --exp-id 9
```
* `--exp-id 9`: enjoy a particular agent. If not defined, the last trained agent is called per default


The table shown in `benchmark.md` includes only agents with highest performance (not quantatively evaluated). In order to see own trained agent amongst the ones from baselines, the folder of the wished agent should be pasted to the `rl-trained-agents` directory. For example the first agent trained with PPO should be displayed in the benchmark table, this requires the folder `OekolopolyBox-v0_1` to be included in the already said directory. Path: **oekolopoly_agents** -> **ppo** -> **OekolopolyBox-v0_1**

Now generate benchmark:

```shell
python -m utils.benchmark --log-dir rl-trained-agents

```

Generate benchmark for all agents used on custom environment:
```shell
python -m utils.benchmark --log-dir oekolopoly_agents
```
**Note 1**: Oftentimes it fails to generate the benchmark and the loading of the table is the command prompt "freezes". A solution as of now is moving own agents to the `rl-trained-agents` directory and deleting the rest in order to see only chosen agents in comparison.

**Note 2**: Generating benchmark for own agents from the `logs` directory is not possible because it clashes with the `benchmark` folder there - either loading "freezes" or it starts generating a benchmark for *ALL* trained agents which takes too long. 

Overview of commands and folders which are accessed by default with their respective implementations/files:
Command | Default Folder |
------------ | ------------- | -------------
train | logs | train.py
enjoy | rl-trained-agents | enjoy.py
benchmark | rl-trained-agents | in main branch or logs/benchmark/benchmark.md


## Optional requirements

This section is relevant in case there are further errors and therefore RL-Baselines3-Zoo could not be installed properly.

* A compiler may be needed for compiling modules like PyBullet. As such here is used [Visual Studio](https://visualstudio.microsoft.com/downloads/) Community version. No further settings are required.
* In case the building of wheels for pytype fails [SWIG](https://sourceforge.net/projects/swig/) must be downloaded and unzipped to any desired directory. Next up set Environment Variables as follows:
    
   1. Go to **Settings** -> **System** -> **About** -> **System info** -> **Advanced system settings** -> **Environment Variables...**  <sub> *[Tutorial with images](https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10)* </sub>

   2. In second half of the window under **System Variables** select `Path`
    
   3. Create a new path to the directory where the unzipped **swigwin** folder resides as shown in the second image below.
   
   <img src="images/sysvar.png" align="left" width="40%"/>
   <img src="images/envvar.png" align="center" width="40%"/>
