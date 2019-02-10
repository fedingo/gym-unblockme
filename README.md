# Basic Implementation for the UnblockMe game

Implementation for the Unblock Me game using the OpenAI Gym Library

The game presents interesting challenges from a Reinforcement Learning prospective. The game requires reasoning to develop the right set of moves that the game

![Game example](https://camo.githubusercontent.com/edd7f5405c3f9e58560d1e926bd1bf1909c1754b/687474703a2f2f6c6f676f6e7562756c2e636f6d2f696d616765732f756e626c6f636b2d6d652e706e67)


## How to install

clone this repository, then move in the folder and use:

    pip install -e .

## Use gym-unblockme

After installation, you can use this environment as any other from OpenAI gym. To make an environment make sure to `import gym_unblockme`

This is a snippet example of how to run the envirnoment:

	import gym
	import gym_unblockme

	env = gym.make('UnblockMe-v0')
	_ = env.reset()

	for _ in range(200):
		_, _, done, _ = env.step(env.action_space.sample())
		env.render()

		if done:
			_ = env.reset()

You can find a testing script in `env_test.py`

## Unblock Me implementation

