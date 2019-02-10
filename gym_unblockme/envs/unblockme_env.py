import gym
from gym import error, spaces, utils
from gym.utils import seeding

import numpy as np
from gym_unblockme.envs.unblockme_class import *
from gym_unblockme.envs.unblockme_render import *
from gym_unblockme.envs.unblockme_generate import *

class UnblockMeEnv(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		self._seed = 0

		# Class initialization
		self.WIDTH = 6; self.HEIGHT = 6; self.DIFFICULT_LEVEL = 3
		self.reset()

		self.obs_shape = self.game_class.shape
		self.action_space = spaces.MultiDiscrete([self.WIDTH, self.HEIGHT, 2])
		self.observation_space = spaces.Box(low=0, high=1, shape=self.obs_shape, dtype=np.int)

	def step(self, action):

		# Do the action
		successful = self.game_class.act(action)

		# And collect the output data
		state    = self.game_class.internal_state
		done     = self.game_class.is_solved()
		add_info = None
		reward = 0

		## Reward engineering
		#	- if is an invalid move the reward is -0.5
		#	- if the game is solved the reward is 1 
		#	- for now, if the move is neutral the reward is 0
		if not successful:
			reward = -0.5
		if done:
			reward = +1

		return [state, reward, done, add_info]


	def reset(self):

		matrix, goal = generate(self.WIDTH,self.HEIGHT, difficulty = self.DIFFICULT_LEVEL)
		self.game_class = unblock_me(matrix, goal)
		return self.game_class.internal_state

	
	def render(self, mode='human', close=False):

		render_unblockme(self.game_class)
		if close:
			pygame.quit()


if __name__ == "__main__":
	import time

	env = UnblockMeEnv()
	_ = env.reset()

	for _ in range(0,200):
		_, _, done, _ = env.step(env.action_space.sample())
		env.render()

		if done:
			env.reset()

		time.sleep(0.1)