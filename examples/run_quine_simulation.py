#!/usr/bin/env python3
"""
Example: Simulating Quine Graph Behavior
Demonstrates self-replication through parallel rewrites
"""

import sys
import os
import random

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chemlambda import Graph, NodeType, Simulator


def create_simple_quine_like() -> Graph:
    """
    Create a simple graph that can potentially replicate
    This is a simplified example - real quines are more complex
    """
    graph = Graph()
    
    # Create a structure that can potentially replicate
    # This is a minimal example - actual quines require specific patterns
    
    # Create nodes that can form replication patterns
    l1_id = graph.add_node(NodeType.L)
    l2_id = graph.add_node(NodeType.L)
    a1_id = graph.add_node(NodeType.A)
    a2_id = graph.add_node(NodeType.A)
    
    l1 = graph.nodes[l1_id]
    l2 = graph.nodes[l2_id]
    a1 = graph.nodes[a1_id]
    a2 = graph.nodes[a2_id]
    
    # Connect in a way that allows potential replication
    graph.connect(l1.ports["right"], a1.ports["left"])
    graph.connect(l2.ports["right"], a2.ports["left"])
    
    # Connect lambda bodies
    graph.connect(l1.ports["left"], a1.ports["middle"])
    graph.connect(l2.ports["left"], a2.ports["middle"])
    
    return graph


def check_isomorphism(graph1: Graph, graph2: Graph) -> bool:
    """
    Simple check if two graphs are isomorphic
    This is a simplified version - full isomorphism checking is more complex
    """
    if len(graph1.nodes) != len(graph2.nodes):
        return False
    
    if len(graph1.edges) != len(graph2.edges):
        return False
    
    # Check node type distribution
    types1 = {}
    types2 = {}
    
    for node in graph1.nodes.values():
        types1[node.node_type] = types1.get(node.node_type, 0) + 1
    
    for node in graph2.nodes.values():
        types2[node.node_type] = types2.get(node.node_type, 0) + 1
    
    return types1 == types2


def simulate_quine_replication(graph: Graph, max_steps: int = 50) -> dict:
    """
    Simulate quine replication behavior
    """
    simulator = Simulator(graph)
    
    initial_state = graph.clone()
    replication_events = []
    
    for step in range(max_steps):
        # Check for potential replication
        if step > 0 and step % 5 == 0:
            # Check if current graph is similar to initial (simplified check)
            if check_isomorphism(initial_state, simulator.graph):
                replication_events.append(step)
        
        # Apply reaction
        applied = simulator.step(random_order=True)
        if not applied:
            break
    
    return {
        "steps": simulator.step_count,
        "replication_events": replication_events,
        "final_graph": simulator.graph,
        "stats": simulator.get_stats(),
    }


def main():
    print("=" * 60)
    print("Quine Graph Replication Simulation")
    print("=" * 60)
    print()
    
    print("Creating quine-like graph...")
    graph = create_simple_quine_like()
    
    print(f"Initial graph: {graph}")
    print(f"Nodes: {len(graph.nodes)}")
    print(f"Edges: {len(graph.edges) // 2}")
    print()
    
    print("Running replication simulation...")
    print("-" * 60)
    
    result = simulate_quine_replication(graph, max_steps=30)
    
    print(f"Simulation completed after {result['steps']} steps")
    print(f"Replication events detected at steps: {result['replication_events']}")
    print()
    
    print("Final Statistics:")
    stats = result['stats']
    print(f"  Total steps: {stats['total_steps']}")
    print(f"  Reaction counts: {stats['reaction_counts']}")
    print(f"  Final nodes: {stats['final_nodes']}")
    print(f"  Final edges: {stats['final_edges']}")
    print()
    
    print("Note: This is a simplified simulation.")
    print("Real quine graphs require specific patterns that enable")
    print("true self-replication through parallel rewrites.")


if __name__ == "__main__":
    main()

