# Basic Implementation for the UnblockMe game

Implementation for the Unblock Me game using the OpenAI Gym Library

The game presents interesting challenges from a Reinforcement Learning prospective. The game requires reasoning to develop the right set of moves that the game

<img src="https://camo.githubusercontent.com/edd7f5405c3f9e58560d1e926bd1bf1909c1754b/687474703a2f2f6c6f676f6e7562756c2e636f6d2f696d616765732f756e626c6f636b2d6d652e706e67" width="256" title="Game example" alt ="Game example">

## How to install

Clone this repository, then move in the folder and use:

    pip install -e .

## Use gym-unblockme

After installation, you can use this environment as any other from OpenAI gym. To make an environment make sure to `import gym_unblockme`

This is a snippet example on how to run the envirnoment:

```python
	import gym
	import gym_unblockme

	env = gym.make('UnblockMe-v0')
	_ = env.reset()

	for _ in range(200):
		_, _, done, _ = env.step(env.action_space.sample())
		env.render()

		if done:
			_ = env.reset()
```

You can find a testing script in `env_test.py`

## Unblock Me implementation

This implementation uses a couple of semplification on the actual game. First, we only use blocks of length 2. This as made the implementation easier, and the complexity of the game was almost the same. The second assumption is that the Red Block (the target) is always horizontal.
The goal for the game is been modified to move the Red Block to the edge of the exit.

The `render()` function uses PyGame to provide a basic visualization of the game.

![Grid Example](https://raw.githubusercontent.com/fedingo/gym-unblockme/master/img/grid_example.png)

### Grid Generation
Every time the environment is reset a new grid is generated. The generation function is using 3 parameters, the `WIDTH`, `HEIGHT` and `DIFFICULTY_LEVEL`. You can change the default values of this parameters and call the `reset()` function.
The generation tries to insert `DIFFICULTY_LEVEL` blocks, drawing random positions. If the choosen position is not occupied, the block is inserted. We try to insert the same amount of vertical and horizontal blocks.
The generated grid is not necessarily solvable. To make it more likely, the insertion of horizontal blocks will avoid the row of the red block. This is the most likely cause that make the generated boards unsolvable. If the `DIFFICULTY_LEVEL` is low enough the grid is most likely solvable.

### Action Space
The Action Space is 3-Dimensional. The first 2 dimensions are the coordinates in the game grid, starting the (0,0) from the top left corner. The third one is instead a [0,1], that indicates the direction where to move the selected block. The 0 is for the (up, left) direction, and the 1 is for the (down, right) direction.

### Observation Space
The Observation Space is a matrix ( `WIDTH` x `HEIGHT` x 4 ) of binary values [0,1]. The layered maps describe the position of the following objects:
- Layer 0: Target Position for the Red Block
- Layer 1: Red Block
- Layer 2: Horizontal Blocks
- Layer 3: Vertical Blocks 

### Reward Function
The Rewards are computed with the following logic:
- If the action is not valid (meaning that it don't produce any meaningful movement), the reward is -0.5
- If the action moves a block but don't solves the grid, the reward is 0
- If the action solves the grid, the reward is 1