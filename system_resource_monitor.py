import time
import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Function to get CPU usage using psutil module
def get_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=0, percpu=True)  # Get CPU usage for all cores
    return sum(cpu_percent) / len(cpu_percent)

# Function to get memory usage (RAM and SSD)
def get_memory_usage():
    virtual_memory = psutil.virtual_memory()
    swap_memory = psutil.swap_memory()
    return virtual_memory.percent, swap_memory.percent

# Function to get network usage (bytes sent and received)
def get_network_usage():
    network_stats = psutil.net_io_counters()
    return network_stats.bytes_sent, network_stats.bytes_recv

# Initialize lists to store resource data
timestamps = []
cpu_usages = []
ram_usages = []
sent_values = []
received_values = []

# Create live resource utilization graphs
fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10, 6))  # Smaller figure size
fig.suptitle("System Resource Monitor")

ax[0].set_ylim(0, 100)
ax[1].set_ylim(0, 100)
ax[2].set_ylim(0, 1e7)  # Adjusted the limit for network bytes

resource_names = ["CPU Usage (%)", "RAM Usage (%)", "Network Usage (Bytes)"]

# Function to update the resource data and plots
def update(frame):
    timestamp = time.time()

    # Get resource usage data
    cpu_usage = get_cpu_usage()
    ram_usage, _ = get_memory_usage()
    sent, received = get_network_usage()

    # Append data to lists
    timestamps.append(timestamp)
    cpu_usages.append(cpu_usage)
    ram_usages.append(ram_usage)
    sent_values.append(sent)
    received_values.append(received)

    # Plot the data
    for i, a in enumerate(ax):
        a.clear()
        if i == 0:
            a.plot(timestamps, cpu_usages, label=f"CPU Usage: {cpu_usage:.2f}%")
        elif i == 1:
            a.plot(timestamps, ram_usages, label=f"RAM Usage: {ram_usage:.2f}%")
        else:
            a.plot(timestamps, sent_values, label=f"Bytes Sent: {sent}")
            a.plot(timestamps, received_values, label=f"Bytes Received: {received}")

        a.set_title(f"{resource_names[i]}")
        a.set_xlabel("Time (seconds)")
        a.set_ylabel("Value")
        a.legend()

    return ax  # Return the axes as artists

ani = FuncAnimation(fig, update, blit=False, interval=1000, cache_frame_data=False)

# Show the live resource utilization graphs
plt.tight_layout()
plt.show()