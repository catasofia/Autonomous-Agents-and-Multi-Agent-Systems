from random import random
from time import sleep
from agent import Agent
from random_agent import RandomAgent 
from env import Environment

RANDOM = RandomAgent

def run_agents(env, agents, num_episodes):
    num_agents = len(agents)
    game_over = False
    observations = env.get_map()

    for _ in range(num_episodes):
        observations = env.get_map()

        while (not game_over):
            for agent in agents:
                agent.see(observations)
                action = agent.action()
                observations, game_over, dead_agent = env.step(agent, action)
                if (dead_agent != False): agents.remove(dead_agent)

            sleep(0.01)
            env.update_map_gui()
        
        env.update_map_gui()
        game_over = False
        dead_agent = False
        env = Environment(num_agents)
        team_red, team_blue = random_vs_random_scenario(env)
        agents = list(team_red.values()) + list(team_blue.values())
        env.team_blue = team_blue.copy()
        env.team_red = team_red.copy()
    env.close()
        


def team_initialization(agent_id_counter, num_agents, agent_type, team, env):
    team_dict = {}
    for _ in range(num_agents):
        team_dict[agent_id_counter] = agent_type(agent_id_counter, team, env)
        agent_id_counter += 1
    return team_dict, agent_id_counter

def random_vs_random_scenario(env):
    # 1 - Agent setup
    agent_id_counter = env.FIRST_AGENT_ID
    team_red, agent_id_counter = team_initialization(agent_id_counter, num_agents // 2, RANDOM, Agent.RED, env)
    team_blue, agent_id_counter = team_initialization(agent_id_counter, num_agents // 2, RANDOM, Agent.BLUE, env)
    return team_red, team_blue

if __name__ == "__main__":
    # 1 - Setup Environment
    num_agents = 4

    if num_agents % 2 != 0:
        raise Exception("Total number of agents must be an even number!")
        
    env = Environment(num_agents)

    # 2 - Setup teams
    team_red, team_blue = random_vs_random_scenario(env)
    env.team_blue.update(team_blue.copy())
    env.team_red.update(team_red.copy())

    #env.set_teams(team_red, team_blue)
    
    # 3 - Run
    agents = list(team_red.values()) + list(team_blue.values())
    run_agents(env, agents, 3)