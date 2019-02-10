from gym.envs.registration import register
 
register(id='UnblockMe-v0', 
    entry_point='gym_unblockme.envs:UnblockMeEnv', 
)