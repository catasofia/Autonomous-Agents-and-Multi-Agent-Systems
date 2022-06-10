from time import sleep
from agent import Agent
from greedy_with_roles_agent import GreedyRolesAgent
from greedy_agent import GreedyAgent
from random_agent import RandomAgent
from env import Environment
from utils import compare_results
import numpy as np

RANDOM = RandomAgent
GREEDY = GreedyAgent
GREEDY_COLAB = GreedyRolesAgent

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

                if (dead_agent != False): 
                    agents.remove(dead_agent)
                if game_over:
                    break

            #sleep(0.2)
            env.update_map_gui()
        results[episode] = steps

        env.update_map_gui()
        game_over = False
        dead_agent = False
        env = Environment(num_agents)
        if(agent_type == RANDOM):
            red_team, blue_team = random_vs_random_scenario(env)
        elif(agent_type == GREEDY):
            red_team, blue_team = greedy_vs_random_scenario(env)
        elif(agent_type == GREEDY_COLAB):
            red_team, blue_team = greedy_Roles_vs_random_scenario(env)
        agents = red_team + blue_team
    
    env.close()

    return results

def random_vs_random_scenario(env):
    red_team = team_initialization(num_agents // 2, RANDOM, Agent.RED, env)
    blue_team = team_initialization(num_agents // 2, RANDOM, Agent.BLUE, env)
    return red_team, blue_team

def greedy_vs_random_scenario(env):
    # 1 - Agent setup
    team_red = team_initialization(num_agents // 2, GREEDY, Agent.RED, env)
    team_blue = team_initialization(num_agents // 2, RANDOM, Agent.BLUE, env)
    return team_red, team_blue

def greedy_Roles_vs_random_scenario(env):
    # 1 - Agent setup
    team_red = team_initialization_collab(num_agents // 2, GREEDY_COLAB, Agent.RED, env)
    team_blue = team_initialization(num_agents // 2, RANDOM, Agent.BLUE, env)
    return team_red, team_blue

def team_initialization(num_agents, agent_type, team, env):
    team_lst = []
    for _ in range(num_agents):
        agent = agent_type(team)
        team_lst.append(agent)
        agent_pos_x, agent_pos_y = deploy_agent_on_env(agent, env)
        agent.set_position(agent_pos_x, agent_pos_y)
    return team_lst

def team_initialization_collab(num_agents, agent_type, team, env):
    team_lst = []
    for _ in range(num_agents // 2):
        agent_1 = agent_type(team, "P")
        agent_2 = agent_type(team, "E")
        team_lst.append(agent_1)
        team_lst.append(agent_2)
        agent_pos_x, agent_pos_y = deploy_agent_on_env(agent_1, env)
        agent_1.set_position(agent_pos_x, agent_pos_y)
        agent_pos_x, agent_pos_y = deploy_agent_on_env(agent_2, env)
        agent_2.set_position(agent_pos_x, agent_pos_y)
    return team_lst

def deploy_agent_on_env(agent, env):
        free_cells = env.get_free_cells()

        if(agent.get_team() == Agent.RED):
            free_cells = list(filter(lambda x: (x[1] <= Environment.WIDTH // 2 - 1), free_cells))
        elif(agent.get_team() == Agent.BLUE):
            free_cells = list(filter(lambda x: (x[1] >= Environment.WIDTH // 2), free_cells))
        
        x, y = free_cells[np.random.choice(len(free_cells))]
        #print(agent.get_team())
        env.set_cell_as_agent(x, y, agent)
        return (x,y)

if __name__ == "__main__":
    results = {}
    num_agents = 4

    # RANDOM VS RANDOM:
    # 1 - Setup Environment
    print("Running Random vs Random")

    if num_agents % 2 != 0:
        raise Exception("Total number of agents must be an even number!")
        
    env = Environment(num_agents)

    # 2 - Setup teams
    red_team, blue_team = random_vs_random_scenario(env)

    # 3 - Run
    agents = red_team + blue_team
    results["Random"] = run_agents(env, agents, 1000, RANDOM)
    
    # ## GREEDY VS RANDOM:
    # # 1 - Setup Environment

    print("Running Greedy vs Random!")
    env = Environment(num_agents)

    # # 2 - Setup teams
    team_red, team_blue = greedy_vs_random_scenario(env)
    
    # 3 - Run
    agents = team_red + team_blue
    results["Greedy"] = run_agents(env, agents, 1000, GREEDY)
 
    # ## GREEDY COLAB VS RANDOM:
    # # 1 - Setup Environment

    print("Running Greedy with Colaboration vs Random!")
    env = Environment(num_agents)

    # # 2 - Setup teams
    team_red, team_blue = greedy_Roles_vs_random_scenario(env)
    
    # 3 - Run
    agents = team_red + team_blue
    results["Greedy with Roles"] = run_agents(env, agents, 1000, GREEDY_COLAB)

    compare_results(
         results,
         title="Teams Comparison on Fish and Chips Environment",
         colors=["orange", "green", "blue"]
    )

    del results["Random"]
    compare_results(
         results,
         title="Teams Comparison on Fish and Chips Environment",
         colors=["green", "blue"]
    )


    