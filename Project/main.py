from simulation.network_topology import NetworkTopology
from simulation.traffic_simulation import TrafficSimulation
from simulation.bottleneck_simulation import BottleneckSimulation


def main():
    # Step 1: Create the network topology
    print("Creating network topology...")
    topology = NetworkTopology()
    topology.create_topology()
    topology.visualize_topology()

    # Step 2: Simulate normal traffic
    print("Simulating normal traffic...")
    traffic_sim = TrafficSimulation(topology.network)
    normal_traffic = traffic_sim.generate_traffic(num_packets=50)
    print("Normal Traffic:\n", normal_traffic.head())
    traffic_sim.save_traffic_logs(normal_traffic, file_name="results/normal_traffic_logs.csv")

    # Step 3: Introduce bottlenecks
    print("Introducing bottlenecks...")
    bottleneck_sim = BottleneckSimulation(topology.network)
    for _ in range(3):  # Introduce 3 bottlenecks
        bottleneck_sim.introduce_bottleneck()
    bottleneck_sim.save_bottleneck_logs(file_name="results/bottleneck_logs.csv")

    # Step 4: Simulate traffic after bottlenecks
    print("Simulating traffic after bottlenecks...")
    post_bottleneck_traffic = traffic_sim.generate_traffic(num_packets=50)
    print("Post-Bottleneck Traffic:\n", post_bottleneck_traffic.head())
    traffic_sim.save_traffic_logs(post_bottleneck_traffic, file_name="results/post_bottleneck_traffic_logs.csv")

    print("Simulation complete. Check the 'results' directory for logs.")


if __name__ == "__main__":
    main()
