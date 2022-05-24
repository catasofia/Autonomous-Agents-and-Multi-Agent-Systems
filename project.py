from pettingzoo.magent import battlefield_v5

env = battlefield_v5.env()
env.reset()
for agent in env.agent_iter():
    observation, reward, done, info = env.last()
    action = env.action_space(agent)
    print(action)
    env.step(action)

   