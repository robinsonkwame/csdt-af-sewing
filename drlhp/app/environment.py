from gym import Env
from action import (
    PARAMETERS_TO_SPACES, NUMBER_OF_BINS_FOR, 
    discretize_dict_space, convert_sample_to_a_dict_sample
)
from observation import PERCEPTUAL_P_AB_SCORE, stub_perceptual_score

class AutoTrace(Env):
    def __init__(self):
        super(AutoTrace, self).__init__()

        self.action_space = discretize_dict_space(
            PARAMETERS_TO_SPACES,
            NUMBER_OF_BINS_FOR
        )['MultiDiscretizedDictSpace']
        
        self.observation_space = PERCEPTUAL_P_AB_SCORE
        self.number_of_episodes_ran = 0
        self.the_current_action = None

    def reset(self):
        initial_observation = self._get_observation()
        return initial_observation

    def step(self, the_action):
        self.number_of_episodes_ran += 1

        self._register(the_action)

        reward = self._get_reward()

        # If the reward and observation have the same values, it means that the agent receives
        # the same information for both its observations and rewards. This scenario could
        # occur in certain simplified environments or toy problems where the observation 
        # itself is used as the reward signal.

        # Here the agent's objective would typically be to learn a policy that 
        # directly maximizes the observed values. It would select actions 
        # that lead to higher observed values because those actions are considered more 
        # desirable or beneficial.

        # In most realistic reinforcement learning scenarios, the reward and observation 
        # are distinct and serve different purposes. The reward provides a more explicit
        # feedback signal that guides the agent's learning process, while the observation 
        # provides information about the environment's state or features necessary for 
        # decision-making.
        the_next_observation = reward
        done = self._stub_done()
        # bug: https://github.com/hill-a/stable-baselines/issues/977
        info = {"episode_number": self.number_of_episodes_ran}

        return the_next_observation, reward, done, info

    def _register(self, the_action):        
        self.the_current_action = convert_sample_to_a_dict_sample(
            the_action,
            PARAMETERS_TO_SPACES,
            NUMBER_OF_BINS_FOR
        )

        print(
            self.the_current_action
        )

    def _get_observation(self):
        return self._get_reward()
    
    def _get_reward(self):
        if self.the_current_action is None:
            return self.observation_space.high

        return stub_perceptual_score(self.the_current_action)
    
    def _stub_done(self):
        done = False
        if self.number_of_episodes_ran > 50:
            done = True

        return 