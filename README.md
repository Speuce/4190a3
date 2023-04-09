# Authors
Christopher Vattheuer
and
Matthew Kwiatkowski

# How to Run
`python reader.py grid.txt result.txt`

# Notes
We chose to display the grid instead of responding to queries in text for a specific cell we show the value for all cells. The grid should display in the console from which you run the program. If you are on macOS or Windows it should display in color as well.

When querying RL with `bestQValue` we print out all Q values. When querying with `bestPolicy` we print out the policy and the value at each state.

When querying MDP we display both the bestPolicy and the stateValue for all cells. 

Also please note when printing GridWorld, it can take up some space horizontal, so make sure you widen your terminal until you see a proper rectangle.  
Also we don't do any exploration or stuff like that and we always initialize to the same spot, so if you want to see decent policies please set a large eps value on Q-Learning in the query. 