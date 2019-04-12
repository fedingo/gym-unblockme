from setuptools import setup

setup(name='gym_unblockme',
      version='0.1',
      url="https://github.com/fedingo/gym-unblockme",
      author="Federico Rossetto",
      license="MIT",
      packages=["gym_unblockme", "gym_unblockme.envs"],
      install_requires=['gym', 'numpy', 'pygame']
)