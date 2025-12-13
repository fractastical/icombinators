#!/usr/bin/env python3
"""
Interactive Chemlambda Simulator
Allows step-by-step exploration of graph rewriting
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chemlambda import Graph, NodeType, Simulator, create_simple_application
from chemlambda.visualizer import GraphVisualizer


def interactive_simulation():
    """Run an interactive simulation"""
    print("=" * 60)
    print("Interactive Chemlambda Simulator")
    print("=" * 60)
    print()
    
    # Create graph
    print("Creating initial graph...")
    graph = create_simple_application()
    
    simulator = Simulator(graph)
    viz = GraphVisualizer(graph)
    
    print("Initial graph:")
    print(viz.visualize())
    print()
    
    print("Commands:")
    print("  's' or 'step' - Apply one reaction")
    print("  'r' or 'run' - Run until completion")
    print("  'q' or 'quit' - Quit")
    print("  'stats' - Show statistics")
    print()
    
    while True:
        try:
            command = input("> ").strip().lower()
            
            if command in ['q', 'quit']:
                print("Exiting...")
                break
            
            elif command in ['s', 'step']:
                applied = simulator.step(random_order=False)
                if applied:
                    step, reaction_name, _ = simulator.reaction_history[-1]
                    print(f"\nApplied {reaction_name} at step {step}")
                    viz = GraphVisualizer(simulator.graph)
                    print(viz.visualize())
                else:
                    print("No more reactions can be applied.")
            
            elif command in ['r', 'run']:
                steps = simulator.run(max_steps=100, random_order=False)
                print(f"\nRan {steps} steps")
                viz = GraphVisualizer(simulator.graph)
                print(viz.visualize())
            
            elif command == 'stats':
                stats = simulator.get_stats()
                print("\nStatistics:")
                print(f"  Total steps: {stats['total_steps']}")
                print(f"  Reaction counts: {stats['reaction_counts']}")
                print(f"  Final nodes: {stats['final_nodes']}")
                print(f"  Final edges: {stats['final_edges']}")
            
            else:
                print("Unknown command. Use 's', 'r', 'stats', or 'q'")
            
            print()
        
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except EOFError:
            print("\nExiting...")
            break


if __name__ == "__main__":
    interactive_simulation()

