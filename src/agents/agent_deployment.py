from random import random
from time import sleep
from agent import Agent
from random_agent import RandomAgent 
from greedy_agent import GreedyAgent
from env import Environment
import numpy as np
from utils import compare_results

RANDOM = RandomAgent
GREEDY = GreedyAgent

def run_agents(env, agents, num_episodes, agent_type):

    results = np.zeros(num_episodes)

    num_agents = len(agents)
    game_over = False
    observations = env.get_map()

    for episode in range(num_episodes):
        steps = 0
        observations = env.get_map()

        while (not game_over):
            steps += 1
            for agent in agents:
                agent.see(observations)
                action = agent.action()
                observations, game_over, dead_agent = env.step(agent, action)
                if (dead_agent != False): agents.remove(dead_agent)
                if game_over:
                    break

            #sleep(0.3)
            env.update_map_gui()
        results[episode] = steps

        env.update_map_gui()
        game_over = False
        dead_agent = False
        env = Environment(num_agents)
        if(agent_type == RANDOM):
            team_red, team_blue = random_vs_random_scenario(env)
        elif(agent_type == GREEDY):
            team_red, team_blue = greedy_vs_random_scenario(env)
        agents = list(team_red.values()) + list(team_blue.values())
        env.team_blue = team_blue.copy()
        env.team_red = team_red.copy()
    
    env.close()

    return results
        


def team_initialization(agent_id_counter, num_agents, agent_type, team, env):
    team_dict = {}
    for _ in range(num_agents):
        if(agent_type == GREEDY):
            team_dict[agent_id_counter] = agent_type(agent_id_counter, team, env, num_agents)
        elif(agent_type == RANDOM):
            team_dict[agent_id_counter] = agent_type(agent_id_counter, team, env)
        agent_id_counter += 1
    return team_dict, agent_id_counter

def random_vs_random_scenario(env):
    # 1 - Agent setup
    agent_id_counter = env.FIRST_AGENT_ID
    team_red, agent_id_counter = team_initialization(agent_id_counter, num_agents // 2, RANDOM, Agent.RED, env)
    team_blue, agent_id_counter = team_initialization(agent_id_counter, num_agents // 2, RANDOM, Agent.BLUE, env)
    return team_red, team_blue

def greedy_vs_random_scenario(env):
    # 1 - Agent setup
    agent_id_counter = env.FIRST_AGENT_ID
    team_red, agent_id_counter = team_initialization(agent_id_counter, num_agents // 2, GREEDY, Agent.RED, env)
    team_blue, agent_id_counter = team_initialization(agent_id_counter, num_agents // 2, RANDOM, Agent.BLUE, env)
    return team_red, team_blue

if __name__ == "__main__":
    
    results = {}
    num_agents = 4

    ## RANDOM VS RANDOM:
    # 1 - Setup Environment

    print("Running Random vs Random!")


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
    results["Random"] = run_agents(env, agents, 20, RANDOM)
    
    ## GREEDY VS RANDOM:
    # 1 - Setup Environment

    print("Running Greedy vs Random!")
    env = Environment(num_agents)

    # 2 - Setup teams
    team_red, team_blue = greedy_vs_random_scenario(env)
    env.team_blue.update(team_blue.copy())
    env.team_red.update(team_red.copy())

    #env.set_teams(team_red, team_blue)
    
    # 3 - Run
    agents = list(team_red.values()) + list(team_blue.values())
    results["Greedy"] = run_agents(env, agents, 20, GREEDY)

    compare_results(
        results,
        title="Teams Comparison on Fish and Chips Environment",
        colors=["orange", "green", "blue"]
    )