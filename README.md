# oekolopoly-rl  [![Python 3.8](https://upload.wikimedia.org/wikipedia/commons/a/a5/Blue_Python_3.8_Shield_Badge.svg)](https://upload.wikimedia.org/wikipedia/commons/a/a5/Blue_Python_3.8_Shield_Badge.svg)
A repository aimed at performing different RL-Algorithms on the custom environment [Oekolopoly](https://github.com/cherrisimo/oekolopoly) using the [RL-Baselines3-Zoo](https://github.com/DLR-RM/rl-baselines3-zoo) Framework. 

## Repo structure overview

* [oekolopoly](https://github.com/cherrisimo/oekolopoly-rl/tree/main/oekolopoly) contains the Oekolopoly environment with following differences to its [original version](https://github.com/cherrisimo/oekolopoly):
  * The observation space no longer contains the flag valid_turn as it brings no information about the state of the environment and is better to be stored in a variable within the step function. 
  * Assertions have been added instead of some if-statements for consistency and better readability.
  * Added reward, which is focused on keeping the Life Areas *Produktion* and *Bevoelkerung* in their middle values.
  * Multiply render functions have been added to showcase each round of the agents' actions.
  * Registered reward environments
* [oekolopoly_agents](https://github.com/cherrisimo/oekolopoly-rl/tree/main/oekolopoly_agents) carries .zip-Files with some well-trained agents grouped by the wrapper and algorithm they've been trained with. 
* [wrappers.py](https://github.com/cherrisimo/oekolopoly-rl/blob/main/wrappers/wrappers.py) contains implemented wrappers.
* [eval](https://github.com/cherrisimo/oekolopoly-rl/blob/main/eval) enables user to see a trained agent's game strategy a.k.a turns.

## Motivation
RL-Baselines3-Zoo provides a nice start base to train own agents in a unified manner. A segregated directory is automatically created for every agent where all necessary informations are stored - such as training data and used hyperparameters. Furthermore, the results of a trained agent can be plotted using Tensorboard which shows different scalars and metrics for easier analysis on the agent´s performance. The framework uses a reliable set of state-of-the-art algorithms which are implemented by [Stable Baselines3](https://stable-baselines3.readthedocs.io/en/master/guide/rl_zoo.html). Other than that the agent's performance can also be visualised if suitable render-Functions are provided. The Framework supports all environments from [OpenAI Gym](https://gym.openai.com/) which means that is is a suitable choice for the Oekolopoly Environment. Most importantly it provides tuned hyperparameters which alleviates the training process because there is no need to tune them. Even then RL Baseliesn3 Zoo gives the opportunity to do so with already implemented scripts which use [Optuna](https://optuna.org/).

All aforementioned features are prebuild/alreadz implemented and require only basis knowledge in RL to be incorporated in one's own project. Because of this the framework is beginner-friendly and a really good start point to create RL-agents.

## Installing

Note: **Python 3.8** is the required for this project because of the module [pytype](https://github.com/cherrisimo/pytype). Also please use the [environment](https://github.com/cherrisimo/oekolopoly-rl/tree/main/oekolopoly) provided in **this repository** as it is the latest code version of the game Oekolopoly.

Note: Download the files provided in this repository beforehand to easily copy-paste them to their respective folders once RL-Baselines3-Zoo is installed.

### Let's get started: 
Please use the command prompt for the instructions below:

1. Create a new environment with **tensorflow** and the required Python version installed as followed:

```shell
conda create -n env_name tensorflow python=3.8
```

or install **tensorflow** in an existing one:

```shell
conda install -c anaconda tensorflow
```

2. Activate environment and install **pytype**, **pybullet** and **box2dpy**:

```shell
conda activate env_name
```
```shell
conda install -c conda-forge pytype pybullet box2d-py
```

3. Install git:
```shell
conda install git
```

4. Install pyglet for the rendering functions in the environment and PyQt for the GUIs:

```shell
pip install pyglet PyQt5
```

RL-Baselines3-Zoo contains further repositories, where over 100 pretrained agents reside. The argument `--recursive` is used to clone them as well. It is, however, **optional** and can be left out so that the size of the cloned repository remains at about 350 MB. The pretrained agents can be found in folder `rl-trained-agents` in the directory of the cloned repository `rl-baselines3-zoo` and can take up to 1.5 GB of space.

5. Clone respective repository with its sub-repos in a new directory:
```shell
cd mydir
```
```shell
git clone --recursive https://github.com/DLR-RM/rl-baselines3-zoo
```

6. In the repository folder execute following to install required packages:

```shell
cd rl-baselines3-zoo
```
```shell
pip install -r requirements.txt
```
## Usage

1. Add custom environment to `utils/import_envs.py` by pasting the following lines:

```python
try:
    import oekolopoly
except ImportError:
    oekolopoly = None
```
2. All wrappers are to be found under `utils/wrappers.py`. The implementation of each wrapper can be found in [wrappers.py](https://github.com/cherrisimo/oekolopoly-rl/blob/main/wrappers/wrappers.py) in this repository. 
To use the wrappers implemented exclusively for the Oekolopoly environment either replace the original `utils/wrappers.py` with the [wrappers.py](https://github.com/cherrisimo/oekolopoly-rl/blob/main/wrappers/wrappers.py) provided in this repository or copy and paste the section with the wished wrappers into the original file.
    
3. Configure hyperparameters in `rl-baselines3-zoo/hyperparams/ppo.yml` for the **PPO** algorithm as shown below:

```python
Oekolopoly-v0:
  env_wrapper:
  - utils.wrappers.OekoBoxActionWrapper
#  - utils.wrappers.OekoSimpleActionWrapper
#  - utils.wrappers.OekoSimpleObsWrapper
  n_envs: 8
  n_timesteps: !!float 1e5
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
The aforementioned hyperparameters are tuned and have been sampled from the CartPole-v1 environment. According to them the agent must train for 1e5 = 100 000 timesteps. Adding each wrapper as argument in the hyperparamter list does not require registering it as new environment. Alternatively, change name of environment to OekolopolyRew2-v0 or OekolopolyRew3-v0 or OekolopolyRew4-v0, to use different reward system. Issue with Reward-Wrapper described [here](https://github.com/DLR-RM/stable-baselines3/issues/146).

#### Rewards overview:
Environment name      | Type of Reward    
--------------------- | -------------
Oekolopoly-v0         | <img src="https://latex.codecogs.com/gif.latex?B=\frac{10(P&plus;3d)}{(r&plus;3)}" title="B=\frac{10(P+3d)}{(r+3)}" />               
OekolopolyRew2-v0     | The agent gets the simple reward 1 for each round.  
OekolopolyRew3-v0     | The agent gets an auxiliary reward for each turn, in order to keep Production and Population in the middle.
OekolopolyRew4-v0     | The agent gets the sum of the auxiliary reward and balance number at the end of each round.

4. If custom environment is not yet installed, now it can be done. Copy and paste the **folder** [oekolopoly](https://github.com/cherrisimo/oekolopoly-rl/tree/main/oekolopoly) in `rl-baselines3-zoo` (only a recommendation. Practically it can reside anywhere in PC since it's not dependent on rl-baselines3-zoo). Now navigate to the respective folder of the environment where `setup.py` is visible and execute the command:

```shell
pip install -e .
```

To use the environments GUI and play the game yourself navigate to the [oekolopoly-gui](https://github.com/cherrisimo/oekolopoly-rl/tree/main/oekolopoly/oekolopoly-gui)-Folder using the command prompt and execute:

```shell
python oeko_gui.py
```
*Regarding training of agents*
Optionally, create a folder to store each trained agent. A further folder named after the used algorithm for the trained agent should reside in it as shown below:

```
├── oekolopoly_agents
│   └── ppo
│       ├── Oekolopoly-v0_10
│       └── ...
└── logs
    └── benchmark
    └── ppo
    └── ...
```
If not done, `logs` stores the newly trained agents per default.

***Following commands should always be executed while being in the repo folder `rl-baselines3-zoo`.***
### Train an agent:

```shell
python train.py --algo ppo --env Oekolopoly-v0 -f oekolopoly_agents -n 5000 --tensorboard-log tensorboard-log
```
* `--algo`: specifies the algorithm to be executed
* `--env`: name of environment
* `-f`: save agent to desired folder. If not defined, `logs` is used as the default path, therefore it's an optional paramater.
* `-n`: set number of timesteps. Optional parameter.
* `--tensorboard-log tensorboard-log`: save data about training to later generate a graph. [See this section.](https://github.com/cherrisimo/oekolopoly-rl#generate-graphs)

Note: Stopping the training sooner than it has reached its given timesteps can be done using CTRL + c but then the informations about the agent (the .zip-File used for the evaluation programm here) may not be saved properly. Best practice is to set the wished number of timesteps in the hyperparameters file or using the `-n` parameter.

### Train a certain agent more:

```shell
python train.py --algo ppo --env Oekolopoly-v0 -i oekolopoly_agents/ppo/Oekolopoly-v0_10/Oekolopoly-v0.zip
```
* `-i`: path to the particular agent

### See trained agent in action:
To use the agents provided in [oekolopoly_agents](https://github.com/cherrisimo/oekolopoly-rl/tree/main/oekolopoly_agents) extract the contents (a.k.a Oekolopoly-v0_...) of the .zip-Files directly in the folder with trained agents: `logs` (default) or `oekolopoly_agents` (user defined) and with respect to which algorithm they were trained with. For example all agents trained with PPO should reside in the ppo folder.

```shell
python enjoy.py --algo ppo --env Oekolopoly-v0 -f oekolopoly_agents --timesteps 22 --exp-id 9
```
* `--timesteps`: the animation runs for the given amount of timesteps and terminates itself automatically.
* `--exp-id 9`: enjoy a particular agent. If not defined, the last trained agent is called per default, therefore it's an optional paramater.
* `-f`: assigning the folder is optional. Per default it would use the `logs` folder.

## Analyse and compare agents

### Benchmarks

The table in `benchmark.md` displays only agents with the highest performance (not quantatively evaluated as stated by RL Baselines3 Zoo). In order to see own trained agent in comparison with the ones from baselines, the folder of the wished agent should be pasted to the `rl-trained-agents` directory. For example the first agent trained with PPO is to be displayed in the benchmark table, thus requiring the folder of the agent `Oekolopoly-v0_10` to be moved to `rl-trained-agents`. 

Path to agent's folder: **oekolopoly_agents** -> **ppo** -> **Oekolopoly-v0_10**

Now generate benchmark:

```shell
python -m utils.benchmark --log-dir rl-trained-agents
```
* `--log-dir`: specify folder with agents

Generate benchmark for all agents used on own custom environment:

```shell
python -m utils.benchmark --log-dir oekolopoly_agents
```

Note: Often, the generating of the benchmark fails and the loading of the table in the command prompt "freezes". A solution for now is moving own agents to the `rl-trained-agents` directory and deleting the rest in order to see only chosen agents in comparison.

Note: Generating benchmark for own agents from the `logs` directory is not possible because it clashes with the `benchmark` folder there - either loading "freezes" or it starts generating a benchmark for *ALL* trained agents which takes all too long. 

### Tensorboard

Following command leads to a localhost webpage where performance of different agents is showcased via graphs:

```shell
tensorboard --logdir tensorboard-log
```

## Overview of commands and folders

Following table lists folders which are accessed per default by the respective command and which file is being invoked/altered as a result.

Command      | Default Folder    | Path to File/Implementation
------------ | -------------     | -------------
train        | logs              | rl-baselines3-zoo/train.py
enjoy        | rl-trained-agents | rl-baselines3-zoo/enjoy.py
benchmark    | rl-trained-agents | rl-baselines3-zoo/benchmark.md or logs/benchmark/benchmark.md

## Manual evaluation of agents

The contents of folder [eval](https://github.com/cherrisimo/oekolopoly-rl/blob/main/eval) must be copied to the the `rl-baselines3-zoo` directory. In the command prompt navigate to the `rl-baselines3-zoo` directory and start the evaluation program using:
```shell
python play.py
```
- Choose an agent using **Open Model** by selecting a valid .zip-File following the path: `oekolopoly_agents/ppo/Oekolopoly-v0_10/Oekolopoly-v0.zip`. The .zip contains all the necessary informations about the agent in order to show what his learnt strategy during training is. 

- The button **Play** shows how he plays a full game based on the given observations in left. 

- **Step** makes one game turn based on the given observations left. 

- You can delete the contents of the table by clicking **Clear**. The chosen agent remains loaded. To choose a new one simply load another .zip-File of a different agent.

## Class overview 

A compact overview of the environments in folder [envs](https://github.com/cherrisimo/oekolopoly-rl/tree/main/oekolopoly/oekolopoly/envs)

Class name         |  Description    
------------       | -------------     
OekoEnv            | Original Environment    
OekoEnvRew2        | Adds reward 1 in each step
OekoEnvRew3        | Adds auxiliary reward in each step
OekoEnvRew4        | Adds auxiliary reward + balance in each step
OekoEnvRandom      | Adds a new initial set of values
OekoEnvRandomRew2  | Combines reward 1 with new set of values

## Optional steps

This section is relevant in case there are further errors and therefore RL-Baselines3-Zoo could not be installed properly.

* A compiler may be needed for compiling modules like PyBullet. As such here is used [Visual Studio](https://visualstudio.microsoft.com/downloads/) Community version. No further settings are required.
* In case the building of wheels for pytype fails [SWIG](https://sourceforge.net/projects/swig/) must be downloaded and unzipped to any desired directory. Next up set Environment Variables as follows:
    
   1. Go to **Settings** -> **System** -> **About** -> **System info** -> **Advanced system settings** -> **Environment Variables...**  <sub> *[Tutorial with images](https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10)* </sub>

   2. In second half of the window under **System Variables** select `Path`
    
   3. Create a new path to the directory where the unzipped **swigwin** folder resides as shown in the second image below.
   
   <img src="images/sysvar.png" align="left" width="40%"/>
   <img src="images/envvar.png" align="center" width="40%"/>
   
   ## TO DO
   -  [x] Develop further Wrapper to split the observation space in low-medium-high
   -  [x] Develop another Wrapper to split action in three sectors which are to be distributed among the 5 Life Areas
   -  [x] Test and compare different rewards on PPO, A2C, DDPG, TD3, SAC with wrappers
   
   ## Resources
   * [Stable Baselines3](https://stable-baselines3.readthedocs.io/en/master/guide/rl_zoo.html)
   * [RL-Baselines3-Zoo](https://github.com/DLR-RM/rl-baselines3-zoo)
