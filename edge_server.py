import numpy as np
from config import Config as C
from task_model import Task, ComputationModel, CommunicationModel

class EdgeServer:
    def __init__(self, ms_id, position, cpu_freq):
        self.ms_id = ms_id
        self.position = position
        self.cpu_freq = cpu_freq
        self.CQ = []
        self.PQ = None
        self.PQ_remaining_time = 0.0
        self.SQ = None
        self.SQ_remaining_time = 0.0

    @property
    def queue_length(self):
        count = len(self.CQ)
        if self.PQ is not None:
            count += 1
        if self.SQ is not None:
            count += 1
        return count

    def is_queue_full(self):
        return self.queue_length >= C.MS_QUEUE_MAX

    def admit_task(self, task):
        if not self.is_queue_full():
            task.assigned_ms = self.ms_id
            self.CQ.append(task)
            return True
        return False

    def compute_priority(self, task, current_slot):
        raise NotImplementedError("Dynamic priority computation is withheld.")

    def update_all_priorities(self, current_slot):
        pass

    def get_task_remaining_time(self, task, current_slot):
        pass

    def get_task_proc_time(self, task):
        pass

    def get_task_recovery_time(self, task):
        pass

    def compute_base_wait(self, current_slot):
        pass

    def compute_wait_time_no_preempt(self, task_index, current_slot):
        pass

    def compute_delay_margin(self, task, task_index, current_slot):
        pass

    def compute_preemption_cost(self, preempt_tasks, current_slot):
        pass

    def compute_affected_task_margin(self, affected_task, preempt_tasks, current_slot):
        pass

    def preemption_evaluation(self, current_slot):
        raise NotImplementedError("Preemption evaluation and execution logic is withheld.")

    def _transfer_to_cloud(self, task):
        pass

    def _execute_preemption(self, preempt_tasks, current_slot):
        pass

    def step(self, current_slot):
        self.preemption_evaluation(current_slot)
        pass

    def get_queue_state(self):
        return {
            'queue_length': self.queue_length,
            'pq_remaining': self.PQ_remaining_time,
            'sq_remaining': self.SQ_remaining_time,
            'cq_size': len(self.CQ)
        }