#!/usr/bin/env python3
"""
Complex Chemlambda Examples
Demonstrates loops, cycles, chemical reaction networks, and quine-like structures
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chemlambda import Simulator
from chemlambda.examples import (
    create_loop_example,
    create_fixed_point_combinator,
    create_quine_like_structure,
    create_ackermann_structure,
    create_self_replicating_pattern,
    create_chemical_reaction_network,
    create_ouroboros_like,
    create_metabolism_example,
)


def run_example(name, graph_creator, max_steps=50):
    """Run an example and display results"""
    print("=" * 70)
    print(f"Example: {name}")
    print("=" * 70)
    print()
    
    # Create graph
    graph = graph_creator()
    print(f"Initial graph: {graph}")
    print(f"Nodes: {len(graph.nodes)}, Edges: {len(graph.edges) // 2}")
    print()
    
    print("Initial structure (.mol format):")
    print(graph.to_mol_format())
    print()
    
    # Run simulation
    simulator = Simulator(graph)
    print("Running simulation...")
    print("-" * 70)
    
    steps = 0
    while steps < max_steps:
        applied = simulator.step(random_order=True)
        if not applied:
            print("No more reactions can be applied.")
            break
        
        steps += 1
        if steps <= 10 or steps % 10 == 0:  # Show first 10 and every 10th
            step, reaction_name, _ = simulator.reaction_history[-1]
            print(f"Step {step}: Applied {reaction_name}")
    
    print("-" * 70)
    print()
    
    # Final state
    print("Final structure:")
    print(simulator.graph.to_mol_format())
    print()
    
    # Statistics
    stats = simulator.get_stats()
    print("Statistics:")
    print(f"  Total steps: {stats['total_steps']}")
    print(f"  Reaction counts: {stats['reaction_counts']}")
    print(f"  Final nodes: {stats['final_nodes']}")
    print(f"  Final edges: {stats['final_edges']}")
    print()
    print()


def main():
    print("\n" + "=" * 70)
    print("Complex Chemlambda Examples")
    print("Demonstrating loops, cycles, chemical reactions, and quine structures")
    print("=" * 70)
    print()
    
    examples = [
        ("Loop Example", create_loop_example),
        ("Fixed Point Combinator (Y)", create_fixed_point_combinator),
        ("Quine-like Structure", create_quine_like_structure),
        ("Ackermann Structure", create_ackermann_structure),
        ("Self-Replicating Pattern", create_self_replicating_pattern),
        ("Chemical Reaction Network", create_chemical_reaction_network),
        ("Ouroboros-like (Snake Eating Tail)", create_ouroboros_like),
        ("Metabolism Example", create_metabolism_example),
    ]
    
    for name, creator in examples:
        try:
            run_example(name, creator, max_steps=30)
        except Exception as e:
            print(f"Error in {name}: {e}")
            print()
            import traceback
            traceback.print_exc()
            print()


if __name__ == "__main__":
    main()

