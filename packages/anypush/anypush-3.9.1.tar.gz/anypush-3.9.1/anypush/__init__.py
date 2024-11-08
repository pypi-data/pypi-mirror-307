from gym.envs.registration import register

register(
    id='anypush/AnyPush-v0',
    entry_point='anypush.envs:AnyPushEnv',
    max_episode_steps=300,
    kwargs={"obs_type": "state"}
)
