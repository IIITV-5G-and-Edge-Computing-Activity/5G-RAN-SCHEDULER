# scheduler.py
from users import User
import random

class Scheduler:
    def __init__(self, total_bandwidth):
        """
        Initializes the Scheduler object with a total bandwidth to allocate.

        Parameters:
        - total_bandwidth (int): The total available bandwidth to be allocated across users.
        """
        self.total_bandwidth = total_bandwidth
        self.users = []

    def add_user(self, user):
        """
        Adds a user to the scheduler's list.

        Parameters:
        - user (User): A User object representing a user in the system.
        """
        self.users.append(user)

    def allocate_weighted_proportional_fair(self):
        """
        Allocates bandwidth using the Weighted Proportional Fair (WPFS) algorithm.
        This algorithm allocates bandwidth based on the ratio of requested bandwidth to the total requested bandwidth.

        Returns:
        - list: A list of user IDs and their allocated bandwidth.
        """
        allocation = []
        total_weight = sum(user.requested_bandwidth for user in self.users)
        for user in self.users:
            weight = user.requested_bandwidth / total_weight
            allocated_bandwidth = weight * self.total_bandwidth
            allocation.append([user.user_id, allocated_bandwidth])
        return allocation

    def allocate_earliest_deadline_first(self):
        """
        Allocates bandwidth based on the Earliest Deadline First (EDF) algorithm.
        For simplicity, this implementation assigns random bandwidth to users.

        Returns:
        - list: A list of user IDs and their allocated bandwidth.
        """
        allocation = sorted(self.users, key=lambda x: random.random())  # Random allocation for EDF
        total_bandwidth = self.total_bandwidth / len(self.users)
        return [[user.user_id, total_bandwidth] for user in allocation]

    def allocate_maximal_with_interference(self):
        """
        Allocates bandwidth using a maximal scheduling approach with interference mitigation.
        Here, random bandwidth values are assigned to simulate this approach.

        Returns:
        - list: A list of user IDs and their allocated bandwidth.
        """
        allocation = []
        for user in self.users:
            allocated_bandwidth = random.randint(1, self.total_bandwidth // len(self.users))
            allocation.append([user.user_id, allocated_bandwidth])
        return allocation

    def allocate_queue_based(self):
        """
        Allocates bandwidth based on queue lengths, here simulated by random allocation.

        Returns:
        - list: A list of user IDs and their allocated bandwidth.
        """
        allocation = []
        for user in self.users:
            allocated_bandwidth = random.randint(1, self.total_bandwidth // len(self.users))
            allocation.append([user.user_id, allocated_bandwidth])
        return allocation

    # Advanced Scheduling Algorithms

    def allocate_round_robin(self):
        """
        Allocates bandwidth to users in a round-robin fashion, where each user gets an equal share of the total bandwidth.

        Returns:
        - list: A list of user IDs and their allocated bandwidth.
        """
        allocation = []
        num_users = len(self.users)
        bandwidth_per_user = self.total_bandwidth / num_users
        for i, user in enumerate(self.users):
            allocation.append([user.user_id, bandwidth_per_user])
        return allocation

    def allocate_shortest_job_first(self):
        """
        Allocates bandwidth based on the Shortest Job First (SJF) scheduling algorithm.
        The user with the smallest requested bandwidth gets allocated first.

        Returns:
        - list: A list of user IDs and their allocated bandwidth.
        """
        allocation = []
        sorted_users = sorted(self.users, key=lambda x: x.requested_bandwidth)
        for user in sorted_users:
            allocation.append([user.user_id, user.requested_bandwidth])
        return allocation

    def allocate_priority_based(self):
        """
        Allocates bandwidth based on QoS priority. High-priority users get more bandwidth.
        High QoS -> 40% of the total bandwidth, Medium QoS -> 30%, Low QoS -> 20%.

        Returns:
        - list: A list of user IDs and their allocated bandwidth.
        """
        allocation = []
        for user in self.users:
            if user.qos_type == 'High':
                allocated_bandwidth = self.total_bandwidth * 0.4
            elif user.qos_type == 'Medium':
                allocated_bandwidth = self.total_bandwidth * 0.3
            else:
                allocated_bandwidth = self.total_bandwidth * 0.2
            allocation.append([user.user_id, allocated_bandwidth])
        return allocation
