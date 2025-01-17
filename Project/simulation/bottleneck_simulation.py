import random
import pandas as pd
import pickle 

class BottleneckSimulation:
    def __init__(self, network):
        self.network = network
        self.bottleneck_logs = []

    def introduce_bottleneck(self):

        edge = random.choice(list(self.network.edges))
        u, v = edge

        if u not in self.network.nodes or v not in self.network.nodes:
            print(f"Invalid edge: {u} -> {v}. Skipping.")
            return

        original_bandwidth = self.network[u][v]["bandwidth"]
        self.network[u][v]["bandwidth"] = max(1, original_bandwidth // 2)  
        self.network[u][v]["latency"] += 10  

        self.bottleneck_logs.append({
            "source": u,
            "destination": v,
            "original_bandwidth": original_bandwidth,
            "reduced_bandwidth": self.network[u][v]["bandwidth"],
            "original_latency": self.network[u][v]["latency"] - 10,
            "increased_latency": self.network[u][v]["latency"],
        })

        print(f"Bottleneck introduced on edge: {u} -> {v} (Bandwidth: {original_bandwidth} -> {self.network[u][v]['bandwidth']})")

    def save_bottleneck_logs(self, file_name="results/bottleneck_logs.csv"):

        bottleneck_df = pd.DataFrame(self.bottleneck_logs)
        bottleneck_df.to_csv(file_name, index=False)
        print(f"Bottleneck logs saved to {file_name}")

    def save_network(self, file_name="results/bottlenecked_network.pkl"):

        with open(file_name, "wb") as f:
            pickle.dump(self.network, f)
        print(f"Bottlenecked network saved to {file_name}")

if __name__ == "__main__":
    from network_topology import NetworkTopology

    topology = NetworkTopology()
    topology.create_topology()

    bottleneck_sim = BottleneckSimulation(topology.network)

    for _ in range(3): 
        bottleneck_sim.introduce_bottleneck()

    bottleneck_sim.save_bottleneck_logs()
    bottleneck_sim.save_network()
