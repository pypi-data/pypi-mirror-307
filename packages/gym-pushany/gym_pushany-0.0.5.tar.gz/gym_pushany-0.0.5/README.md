## Install Anypush
```python
pip install anypush
```

## Example
```python
import gymnasium as gym
import gym_pushany

<<<<<<< HEAD
# OBJECT_NAME_LIST = [
#     't',
#     '0',
#     '1',
#     '2',
#     '3',
#     '4',
#     '5',
#     '6',
#     '7',
#     '8',
#     '9',
#     'ellipse',
#     'rectangle',
#     'reg3',
#     'reg4',
#     'reg5',
#     'reg6',
#     'reg7',
#     'reg8',
#     'reg9',
#     'reg10'
# ]

object_name = 'ellipse'  
use_obstacles = True     
env = gym.make("anypush/AnyPush-v0", object_name=object_name, use_obstacles=use_obstacles)
=======
object_name = 'ellipse'  # 예시로 'ellipse'를 사용
use_obstacles = True     # 예시로 True를 사용
env = gym.make("pushany/PushAny-v0", object_name=object_name, use_obstacles=use_obstacles)
>>>>>>> 6ff4299 (change name to gym-pushany)
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
