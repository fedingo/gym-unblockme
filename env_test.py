import time
import gym
import gym_unblockme

env = gym.make('UnblockMe-v0')

_ = env.reset()

for _ in range(200):
	_, _, done, _ = env.step(env.action_space.sample())
	env.render()
	time.sleep(0.1)

	if done:
		_ = env.reset()