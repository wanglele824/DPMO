import numpy as np
from config import Config as C
from task_model import Task, CommunicationModel, ComputationModel
from edge_server import EdgeServer

class MobileDevice:
    def __init__(self, md_id, position, cpu_freq, trajectory=None):
        self.md_id = md_id
        self.position = np.array(position, dtype=np.float64)
        self.cpu_freq = cpu_freq
        self.trajectory = trajectory
        self.is_local_busy = False
        self.local_remaining_time = 0.0
        self.connected_ms_ids = []
        self.current_task = None

    def update_position(self, slot):
        pass

    def generate_task(self, slot):
        pass

    def select_nearest_ms(self, ms_list):
        pass

    def execute_local(self, task, local_ratio):
        pass

    def local_step(self):
        pass

class MECEnvironment:
    def __init__(self, num_md=C.NUM_MD, num_ms=C.NUM_MS):
        self.num_md = num_md
        self.num_ms = num_ms
        self.current_slot = 0
        self.ms_list = self._init_edge_servers()
        self.md_list = self._init_mobile_devices()
        self.all_tasks = []
        self.finished_tasks = []
        self.failed_tasks = []

    def _init_edge_servers(self):
        pass

    def _init_mobile_devices(self):
        pass

    def reset(self):
        pass

    def _get_observation_for_md(self, md):
        raise NotImplementedError("State observation mechanism is withheld.")

    def _get_all_observations(self):
        pass

    def _get_global_state(self):
        pass

    def _apply_actions(self, actions):
        pass

    def _create_task_slice(self, original_task, ms_id, action_idx, ratio):
        pass

    def _compute_rewards(self):
        raise NotImplementedError("Reward formulation is withheld.")

    def step(self, actions):
        pass