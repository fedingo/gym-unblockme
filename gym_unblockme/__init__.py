from gym.envs.registration import register
import numpy as np
 
register(id='UnblockMe-v0', 
    entry_point='gym_unblockme.envs:UnblockMeEnv', 
)

matrix_input = np.array([[0, 2, 2, 0],
                        [1, 1, 0, 3],
                        [0, 0, 0, 3],
                        [2, 2, 0, 0]])
target_input = [1,3]

register(id='UnblockMeFixedMap-v0',
         entry_point='gym_unblockme.envs:UnblockMeEnv',
         kwargs={'fix_map': True,
                 'matrix' : matrix_input,
                 'goal'   : target_input})