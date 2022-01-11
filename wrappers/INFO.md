# Overview

### Box Action Wrapper
*Class Name: OekoBoxActionWrapper, `Action Wrapper`, `Box`*

Transforms the action space into a continuous one. Sets the upper und lower bounds of each dimension of the vector between the values of {0..1} except for the second and last whichi could be {-1..1}. The sum of all dimensions must not exceed 1. The function `distribute1 ()` generates the discrete action from the continuous one to pass it to the original environment. 

Number of actions: theoretically infinite

### **Simple Action Wrapper**
*Class Name: OekoSimpleActionWrapper – `Action Wrapper`, `MultiDiscrete`*

Splits the available points in three groups which are to be distributed among all regions in the game. The wrapper uses a list of legal actions represented as strings and at each round chooses a random element (index). For example the string '210001' gives 2/3 of the points to the first region Sanierung whilst the rest belongs to the Produktion. The last character indicates that the points assigned to the second region must be subtracted (0 - add, 1 - subtract). 

Number of actions: 847 total actions

### **Simple Observation Wrapper** 
*Class Name: OekoSimpleObsWrapper – `Observation Wrapper`, `MultiDiscrete`*

Splits the values of the regions into the three categories low-medium-high corresponding to the numbers 0, 1, 2. The newly generated observation is given at the end of each step. The variables `obs_count` and `obs_split` denote the number of regions and the number of categories to be split in. 

Number of observations : 6561 total observations


### **OekolopolyBoxReward** 
*Class Name: OekoRewardWrapper – `Reward Wrapper`*

Adds a reward at each round. See table of rewards in main README.md file.

## Usage
Directly replace the original `wrappers.py` with the available file here.
