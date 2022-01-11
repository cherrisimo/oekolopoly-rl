# Overview

### Box Action Wrapper
*Klassenname: OekoBoxActionWrapper, `Action Wrapper`, `Box`*

Transforms the action space into a continuous one. Sets the upper und lower bounds of each dimension of the vector between the values of {0..1} except for the second and last whichi could be {-1..1}. The sum of all dimensions must not exceed 1. The function `distribute1 ()` generates the discrete action from the continuous one to pass it to the original environment. Theoretically infinite many.

### **Simple Action Wrapper**
*Klassenname: OekoSimpleActionWrapper – `Action Wrapper`, `MultiDiscrete`*

Splits the available points in three groups which are to be distributed among all regions in the game. The wrapper uses a list of legal actions represented as strings and at each round chooses a random element (index). For example the string '210001' gives 2/3 of the points to the first region Sanierung whilst the rest belongs to the Produktion. The last character indicates that the points assigned to the second region must be subtracted (0 - add, 1 - subtract). 847 total actions

### **Simple Observation Wrapper** 
*Klassenname: OekoSimpleObsWrapper – `Observation Wrapper`, `MultiDiscrete`*

Splits the values of the regions into the three categories low-medium-high corresponding to the numbers 0, 1, 2. The newly generated observation is given at the end of each step. The variables `obs_count` and `obs_split` denote the number of regions and the number of categories to be split in. 6654 total observations


### **OekolopolyBoxReward** 
*Klassenname: OekoRewardWrapper – `Reward Wrapper`*

Der Wrapper fügt einen Hilfsreward zum Environment hinzu. Die Belohnung hat zum Ziel, die Bereiche Produktion und Bevölkerung in mittleren Werten zu halten.

## Usage
Die Datei `wrappers.py` enthält die Wrappers für die Umgebung Ökolopoly und die Environments von RL Baselines Zoo3. ~~Sie kann direkt anstelle der originalen im Ordner `utils` gesetzt werden. Instruktionen wie Wrappers zur Umgebung hinzugefügt werden können, sind im Haupt-[README](https://github.com/cherrisimo/oekolopoly-rl#usage) unter Punkt 2a enthalten.~~ [!MUST BE TESTED]
