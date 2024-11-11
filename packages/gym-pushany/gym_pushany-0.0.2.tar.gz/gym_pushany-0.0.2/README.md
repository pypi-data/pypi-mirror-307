## Install Anypush
```python
pip install anypush
```

## Example
```python
import gymnasium as gym
import gym_pushany

object_name = 'ellipse'  # 예시로 'ellipse'를 사용
use_obstacles = True     # 예시로 True를 사용
env = gym.make("pushany/PushAny-v0", object_name=object_name, use_obstacles=use_obstacles)
observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    image = env.render()

    print(f'terminated: {terminated}, truncated: {truncated}')
    if terminated or truncated:
        observation, info = env.reset()

env.close()
```
