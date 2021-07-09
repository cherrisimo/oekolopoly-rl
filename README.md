# oekolopoly-rl
A repository aimed at performing different RL-Algorithms on the custom environment [Oekolopoly](https://github.com/cherrisimo/oekolopoly) using [RL-Baselines3-Zoo](https://github.com/DLR-RM/rl-baselines3-zoo) Framework.

## Requirements

* [Visual Studio](https://visualstudio.microsoft.com/downloads/) must be installed in order to use modules like PyBullet. Community version relied.
* To build wheels for pytype download [SWIG](https://sourceforge.net/projects/swig/) and unzip it to `rl_baselines3-zoo`
  * Set Environment `PATH` Variables as follows:
 
## Installing

Install tensorflow in a new environment as follows:

```shell
conda create -n tf tensorflow
```

or in an existing one:

```shell
conda install -c anaconda tensorflow
```

Activate environment using:

```shell
conda activate tf
```

Install git:
```shell
conda install git
```

Clone respective repository:
```shell
git clone --recursive https://github.com/DLR-RM/rl-baselines3-zoo
```

In the repository folder execute following command:

```shell
cd rl-baselines3-zoo
pip install -r requirements.txt
```

Configure hyperparameters in rl-baselines3-zoo/hyperparams/ppo.yml as shown:

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

Oekolopoly-v0:
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


## Usage

Train an agent:
```shell
python enjoy.py --algo ppo --env OekolopolyBox-v0 --gym-packages=oekolopoly -f logs
```
* `--algo`: specifies the algorithm to be executed
* `--env`: name of environment
* `--gym-packages`: used to correctly point path to the environment class
* `-f`: save agent to the wished folder, if not defined logs is used as the default

Train a certain agent more:

```shell
python train.py --algo ppo --env OekolopolyBox-v0 --gym-packages=oekolopoly -i logs/ppo/OekolopolyBox-v0_1/OekolopolyBox-v0.zip
```
* `-i`: path to the particular agent

See trained agent in action using:

```shell
python enjoy.py --algo ppo --env OekolopolyBox-v0 --gym-packages=oekolopoly -f logs --exp-id 9
```
* `--exp-id 9`: enjoy a particular agent. If not defined, the last trained agent is the default

See benchmarks:
Evaluates highest performance (not quantative) 

```shell
python -m utils.benchmark

```

Generate benchmark for all agents used on custom environment:
```shell

```
