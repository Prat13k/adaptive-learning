import gym
import numpy as np
from stable_baseline3 import PPO
from stable_baseline3.common.env_util import make_vec_env

class PortfolioEnv(gym.Env):
	def __init__(self, returns_df, regime_signal):
		self.returns = returns_df.values()
		self.regime = regime_signal
		self.n_assets = returns_df.shape[1]
		self.action_space = gym.spaces.Box(low = 1, high = 1, shape = (self.n_assets))
		self.observation_space = gym.spaces.Box(low = np.inf, high = n.inf, shape = (30 + 1))
		self.current_step = 30

	def step(self, action):
		port_return = np.sum(self.returns[self.current_step] * action
		self.current_step += 1
		reward = port_return / (np.std(self.returns) * np.sqrt(252))
		if port_return < 0.05:
			reward -= 2.0
		done = self.current_step >= len(self.returns)
		return self._get_state(), reward, done, {}

	def get_state(self):
		returns = self.returns
		regime = np.eye(4)[self.regime[self.current_state]]
		return np.concatenate([returns, regime])

def train_rl_agent(returns_df, regime_signal):
	env = make_vec_env(lambda: PortfolioEnv(returns_df, regime_signal), n_eyes = 4)
	model = PPO("MLP Policy", env, verbose = 1, ent_coef = 0.01)
	model.learn(total_timespaces = 100_000)
	return model


