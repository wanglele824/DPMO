import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Normal
from config import Config as C

class ActorNetwork(nn.Module):
    def __init__(self, obs_dim, action_dim):
        super(ActorNetwork, self).__init__()
        self.action_dim = action_dim
        layers = []
        input_dim = obs_dim
        for _ in range(C.NUM_HIDDEN_LAYERS):
            layers.append(nn.Linear(input_dim, C.HIDDEN_DIM))
            layers.append(nn.ReLU())
            input_dim = C.HIDDEN_DIM
        self.feature_net = nn.Sequential(*layers)
        self.mean_head = nn.Linear(C.HIDDEN_DIM, action_dim)
        self.log_std_head = nn.Linear(C.HIDDEN_DIM, action_dim)

    def forward(self, obs):
        features = self.feature_net(obs)
        mean = torch.sigmoid(self.mean_head(features))
        log_std = self.log_std_head(features)
        log_std = torch.clamp(log_std, -5, 0)
        return mean, torch.exp(log_std)

    def get_action(self, obs, deterministic=False):
        mean, std = self.forward(obs)
        if deterministic:
            return mean, torch.zeros(1)
        dist = Normal(mean, std)
        action = torch.clamp(dist.sample(), 0, 1)
        return action, dist.log_prob(action).sum(dim=-1)

    def evaluate_action(self, obs, action):
        mean, std = self.forward(obs)
        dist = Normal(mean, std)
        return dist.log_prob(action).sum(dim=-1), dist.entropy().sum(dim=-1)

class CriticNetwork(nn.Module):
    def __init__(self, global_state_dim):
        super(CriticNetwork, self).__init__()
        layers = []
        input_dim = global_state_dim
        for _ in range(C.NUM_HIDDEN_LAYERS):
            layers.append(nn.Linear(input_dim, C.HIDDEN_DIM))
            layers.append(nn.ReLU())
            input_dim = C.HIDDEN_DIM
        layers.append(nn.Linear(C.HIDDEN_DIM, 1))
        self.net = nn.Sequential(*layers)

    def forward(self, global_state):
        return self.net(global_state).squeeze(-1)

class ExperienceBuffer:
    def __init__(self):
        self.clear()

    def clear(self):
        self.observations, self.actions, self.log_probs = [], [], []
        self.rewards, self.global_states, self.dones, self.values = [], [], [], []

    def store(self, obs, actions, log_probs, rewards, global_state, done, value):
        self.observations.append(obs)
        self.actions.append(actions)
        self.log_probs.append(log_probs)
        self.rewards.append(rewards)
        self.global_states.append(global_state)
        self.dones.append(done)
        self.values.append(value)

    def get_batch(self):
        pass

    @property
    def size(self):
        return len(self.rewards)

class MAPPOTrainer:
    def __init__(self, obs_dim, action_dim, num_agents, global_state_dim):
        self.num_agents = num_agents
        self.obs_dim = obs_dim
        self.action_dim = action_dim
        self.actor = ActorNetwork(obs_dim, action_dim)
        self.critic = CriticNetwork(global_state_dim)
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=C.ACTOR_LR)
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=C.CRITIC_LR)
        self.buffer = ExperienceBuffer()

    def select_actions(self, observations, global_state, deterministic=False):
        pass

    def compute_gae(self, rewards, values, dones):
        raise NotImplementedError("GAE logic is withheld.")

    def update(self):
        raise NotImplementedError("Network update mechanism is withheld.")

    def save_model(self, path):
        pass

    def load_model(self, path):
        pass