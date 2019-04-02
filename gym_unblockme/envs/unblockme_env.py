import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pygame
import numpy as np
from gym_unblockme.envs.unblockme_class import *
from gym_unblockme.envs.unblockme_render import *
from gym_unblockme.envs.unblockme_generate import *

class UnblockMeEnv(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self, fix_map=False, difficulty=1, max_steps = 400, matrix = None, goal = None):
		self._seed = 0
		self.max_steps = max_steps

		# Class initialization
		self.WIDTH = 6; self.HEIGHT = 6; self.DIFFICULT_LEVEL = difficulty
		self.fix_map = fix_map

		if matrix is not None and goal is not None:
			self.matrix = matrix; self.goal = goal
			self.WIDTH, self.HEIGHT = self.matrix.shape
		elif self.fix_map:
			self.matrix, self.goal = generate(self.WIDTH, self.HEIGHT, difficulty=self.DIFFICULT_LEVEL)
		self.reset()

	def step(self, action):

		# Do the action
		successful = self.game_class.act(action)
		self.step_count += 1

		# And collect the output data
		state    = self.game_class.internal_state
		done     = self.game_class.is_solved()
		add_info = None
		reward = -0.1

		## Reward engineering
		#	- if is an invalid move the reward is -0.5
		#	- if the game is solved the reward is 1 
		#	- for now, if the move is neutral the reward is 0
		if not successful:
			reward = -1
		if done:
			reward = +50

		done = done or self.step_count >= self.max_steps
		return [state, reward, done, add_info]


	def reset(self):

		if not self.fix_map:
			self.matrix, self.goal = generate(self.WIDTH,self.HEIGHT, difficulty = self.DIFFICULT_LEVEL)
		self.game_class = unblock_me(self.matrix, self.goal)
		self.step_count = 0

		self.obs_shape = self.game_class.shape
		self.action_space = spaces.MultiDiscrete([self.WIDTH, self.HEIGHT, 2])
		self.observation_space = spaces.Box(low=0, high=1, shape=self.obs_shape, dtype=np.int)
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