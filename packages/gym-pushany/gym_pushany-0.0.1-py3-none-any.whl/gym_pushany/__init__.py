from gymnasium.envs.registration import register

register(
    id='pushany/PushAny-v0',
    entry_point='gym_pushany.envs:PushAnyEnv',
    max_episode_steps=300
)
