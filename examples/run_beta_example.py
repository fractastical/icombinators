#!/usr/bin/env python3
"""
Example: Running BETA reduction
Demonstrates the BETA move in action
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chemlambda import Graph, NodeType, Simulator, create_simple_application


def main():
    print("=" * 60)
    print("Chemlambda BETA Reduction Example")
    print("=" * 60)
    print()
    
    # Create graph for (λx.x) y
    print("Creating graph for (λx.x) y (identity function applied to y)")
    graph = create_simple_application()
    
    print(f"Initial graph: {graph}")
    print(f"Nodes: {len(graph.nodes)}")
    print(f"Edges: {len(graph.edges) // 2}")
    print()
    
    print("Initial graph structure:")
    print(graph.to_mol_format())
    print()
    
    # Create simulator
    simulator = Simulator(graph)
    
    # Run simulation
    print("Running simulation...")
    print("-" * 60)
    
    steps = 0
    max_steps = 10
    
    while steps < max_steps:
        applied = simulator.step(random_order=False)
        if not applied:
            print("No more reactions can be applied.")
            break
        
        steps += 1
        reaction_name = simulator.reaction_history[-1][1]
        print(f"Step {steps}: Applied {reaction_name}")
        print(f"  Graph: {simulator.graph}")
        print(f"  Nodes: {len(simulator.graph.nodes)}, "
              f"Edges: {len(simulator.graph.edges) // 2}")
    
    print("-" * 60)
    print()
    
    # Final state
    print("Final graph structure:")
    print(simulator.graph.to_mol_format())
    print()
    
    # Statistics
    stats = simulator.get_stats()
    print("Simulation Statistics:")
    print(f"  Total steps: {stats['total_steps']}")
    print(f"  Reaction counts: {stats['reaction_counts']}")
    print(f"  Final nodes: {stats['final_nodes']}")
    print(f"  Final edges: {stats['final_edges']}")


if __name__ == "__main__":
    main()

