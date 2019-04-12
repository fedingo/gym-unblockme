from gym.envs.registration import register
import numpy as np
 
register(id='UnblockMe-v0', 
    entry_point='gym_unblockme.envs:UnblockMeEnv', 
)

register(id='UnblockMeListed-v0',
    entry_point='gym_unblockme.envs:UnblockMeEnvListed',
)

matrix_input = np.array([[0, 0, 2, 2],
                        [1, 1, 0, 3],
                        [0, 0, 0, 3],
                        [0, 0, 2, 2]])
target_input = [1,3]

register(id='UnblockMeFixedMap-v0',
         entry_point='gym_unblockme.envs:UnblockMeEnv',
         kwargs={'fix_map': True,
                 'matrix' : matrix_input,
                 'goal'   : target_input,
                 'max_steps': 100})

register(id='UnblockMeListedFixedMap-v0',
         entry_point='gym_unblockme.envs:UnblockMeEnvListed',
         kwargs={'fix_map': True,
                 'matrix' : matrix_input,
                 'goal'   : target_input,
                 'max_steps': 100})

register(id='UnblockMeCompactFixedMap-v0',
         entry_point='gym_unblockme.envs:UnblockMeEnvListed',
         kwargs={'fix_map': True,
                 'matrix' : matrix_input,
                 'goal'   : target_input,
                 'listing': False,
                 'max_steps': 100})

register(id='UnblockMeCompact-v0',
         entry_point='gym_unblockme.envs:UnblockMeEnvListed',
         kwargs={'listing': False})