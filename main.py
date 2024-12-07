import pandas as pd
import matplotlib.pyplot as plt
import os
from scheduler import Scheduler
from users import generate_users_with_dynamics
import numpy as np

# Create output directory if it doesn't exist
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def plot_results(allocation_data, scheduler_name, image_counter):
    """
    Plots the bandwidth allocation for a given scheduling algorithm
    and saves the plot as an image in the output folder.
    """
    df = pd.DataFrame(allocation_data, columns=["User ID", "Allocated Bandwidth"])
    df = df.sort_values(by="User ID")

    # Plot the results
    plt.figure(figsize=(16, 10))
    ax = df.plot(kind="bar", x="User ID", y="Allocated Bandwidth", color='skyblue', width=0.7)
    plt.title(f'{scheduler_name} - Bandwidth Allocation', fontsize=18)
    plt.xlabel('User ID', fontsize=14)
    plt.ylabel('Allocated Bandwidth (Mbps)', fontsize=14)
    plt.grid(True)
    plt.xticks(rotation=90, fontsize=10)
    plt.tight_layout()

    # Save the plot as an image (PNG) in the output folder
    image_filename = f"{output_dir}/{scheduler_name.replace(' ', '_')}_{image_counter}.png"
    plt.savefig(image_filename)
    plt.close()

    print(f"Saved {scheduler_name} plot as: {image_filename}")

def plot_qos_distribution(users, image_counter):
    """
    Plots the distribution of QoS types (High, Medium, Low)
    and saves the plot as an image in the output folder.
    """
    qos_counts = {'High': 0, 'Medium': 0, 'Low': 0}
    for user in users:
        qos_counts[user.qos_type] += 1

    plt.bar(qos_counts.keys(), qos_counts.values(), color='skyblue')
    plt.title("QoS Distribution", fontsize=16)
    plt.xlabel("QoS Type", fontsize=12)
    plt.ylabel("Number of Users", fontsize=12)
    plt.grid(True)
    plt.tight_layout()

    # Save the plot as an image (PNG) in the output folder
    image_filename = f"{output_dir}/QoS_Distribution_{image_counter}.png"
    plt.savefig(image_filename)
    plt.close()

    print(f"Saved QoS distribution plot as: {image_filename}")

def calculate_fairness(allocation_data):
    """
    Calculates fairness using the variance of the bandwidth allocation.
    The lower the variance, the more fair the allocation.
    """
    allocations = [bandwidth for _, bandwidth in allocation_data]
    return np.var(allocations)

def run_simulation():
    """
    Runs the simulation, executes all scheduling algorithms, and compares their performance.
    The results are saved as images in the output folder, and comparison metrics are printed to a text file.
    """
    total_bandwidth = 100  # Total available bandwidth (in Mbps)
    max_bandwidth_per_user = 20  # Max bandwidth a user can request (in Mbps)
    num_users = 10  # Number of users

    # Generate random users with dynamic properties (including priority)
    users = generate_users_with_dynamics(num_users, max_bandwidth_per_user, include_priority=True)

    # Initialize the scheduler
    scheduler = Scheduler(total_bandwidth)
    for user in users:
        scheduler.add_user(user)

    # Image counter to differentiate between saved images
    image_counter = 1

    # Open the results text file for writing
    with open('simulation_results.txt', 'w') as file:
        file.write("5G RAN Scheduling Simulation Results\n")
        file.write(f"Total Bandwidth: {total_bandwidth} Mbps\n")
        file.write(f"Max Bandwidth per User: {max_bandwidth_per_user} Mbps\n")
        file.write(f"Number of Users: {num_users}\n\n")

        # Plot and save QoS Distribution to image
        plot_qos_distribution(users, image_counter)
        file.write("QoS Distribution:\n")
        for user in users:
            file.write(f"User {user.user_id}: QoS Type = {user.qos_type}\n")
        image_counter += 1

        # Run and plot each scheduling algorithm
        algorithms = [
            ("Round Robin Scheduling", scheduler.allocate_round_robin),
            ("Shortest Job First (SJF)", scheduler.allocate_shortest_job_first),
            ("Priority-based Scheduling", scheduler.allocate_priority_based),
            ("Weighted Proportional Fair", scheduler.allocate_weighted_proportional_fair),
            ("Earliest Deadline First (EDF)", scheduler.allocate_earliest_deadline_first),
            ("Maximal Scheduling with Interference Mitigation", scheduler.allocate_maximal_with_interference),
            ("Queue-based Scheduling", scheduler.allocate_queue_based)
        ]

        # Dictionary to hold the results for comparison
        comparison_results = {}

        for scheduler_name, allocation_func in algorithms:
            allocation_data = allocation_func()
            plot_results(allocation_data, scheduler_name, image_counter)
            image_counter += 1

            # Write allocation results to the file only once here
            file.write(f"\n{scheduler_name} Allocation:\n")
            for user_id, bandwidth in allocation_data:
                file.write(f"User {user_id} - Allocated Bandwidth: {bandwidth} Mbps\n")

            # Calculate fairness (variance of the allocation) for each algorithm
            fairness = calculate_fairness(allocation_data)
            comparison_results[scheduler_name] = fairness

        # Write comparison results to the file
        file.write("\nComparison of Scheduling Algorithms based on Fairness (Lower is Better):\n")
        for scheduler_name, fairness in comparison_results.items():
            file.write(f"{scheduler_name}: Fairness (Variance) = {fairness:.2f}\n")

    print("\nSimulation complete. All results have been saved as images in the 'output' folder and details have been written to 'simulation_results.txt'.")

if __name__ == "__main__":
    run_simulation()
