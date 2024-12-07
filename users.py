# users.py
import random

class User:
    def __init__(self, user_id, qos_type, requested_bandwidth, priority=None):
        """
        Initializes a User object with dynamic properties.

        Parameters:
        - user_id (int): Unique identifier for the user.
        - qos_type (str): The QoS type ('High', 'Medium', 'Low') of the user.
        - requested_bandwidth (int): The amount of bandwidth the user requests.
        - priority (int, optional): The priority of the user (1-10). Used in priority-based scheduling.
        """
        self.user_id = user_id
        self.qos_type = qos_type
        self.requested_bandwidth = requested_bandwidth
        self.priority = priority  # Priority used in scheduling

def generate_users_with_dynamics(num_users, max_bandwidth_per_user, include_priority=False):
    """
    Generates a list of random users with dynamic properties such as QoS and priority.

    Parameters:
    - num_users (int): Number of users to generate.
    - max_bandwidth_per_user (int): Maximum bandwidth a user can request.
    - include_priority (bool): Whether to assign a priority value to each user.

    Returns:
    - list: A list of User objects.
    """
    qos_types = ['High', 'Medium', 'Low']
    users = []
    for user_id in range(1, num_users + 1):
        # Assign random QoS type and requested bandwidth
        qos_type = random.choice(qos_types)
        requested_bandwidth = random.randint(1, max_bandwidth_per_user)
        
        # Optionally assign random priority for priority-based scheduling
        if include_priority:
            priority = random.randint(1, 10)  # Random priority between 1 and 10
        else:
            priority = None
        
        users.append(User(user_id, qos_type, requested_bandwidth, priority))
    return users
