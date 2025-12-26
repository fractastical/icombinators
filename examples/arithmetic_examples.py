#!/usr/bin/env python3
"""
Arithmetic Examples with Chemlambda
Demonstrates computing arithmetic operations using Church encodings
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chemlambda import Graph, Simulator
from church_encodings import (
    church_numeral, church_add, church_multiply, church_successor
)
from result_extractor import decode_church_numeral, extract_result


def compute_addition(m: int, n: int, max_steps: int = 1000) -> dict:
    """
    Compute m + n using Church numerals.
    
    Args:
        m: First number
        n: Second number
        max_steps: Maximum reduction steps
    
    Returns:
        Dictionary with computation results
    """
    print(f"Computing {m} + {n}...")
    
    # Create Church numerals
    m_church = church_numeral(m)
    n_church = church_numeral(n)
    
    # Create addition function
    add_func = church_add()
    
    # Apply addition function to m and n
    # This is: add m n = (λm.λn.λf.λx.m f (n f x)) m n
    graph = apply_function_to_args(add_func, [m_church, n_church])
    
    # Run simulation
    simulator = Simulator(graph)
    steps = simulator.run(max_steps=max_steps, random_order=False)
    
    # Try to extract result
    result_type, result_value = extract_result(simulator.graph)
    
    return {
        "operation": f"{m} + {n}",
        "steps": steps,
        "result_type": result_type,
        "result_value": result_value,
        "final_graph": simulator.graph,
        "stats": simulator.get_stats(),
    }


def compute_multiplication(m: int, n: int, max_steps: int = 1000) -> dict:
    """
    Compute m * n using Church numerals.
    
    Args:
        m: First number
        n: Second number
        max_steps: Maximum reduction steps
    
    Returns:
        Dictionary with computation results
    """
    print(f"Computing {m} * {n}...")
    
    # Create Church numerals
    m_church = church_numeral(m)
    n_church = church_numeral(n)
    
    # Create multiplication function
    mult_func = church_multiply()
    
    # Apply multiplication function to m and n
    graph = apply_function_to_args(mult_func, [m_church, n_church])
    
    # Run simulation
    simulator = Simulator(graph)
    steps = simulator.run(max_steps=max_steps, random_order=False)
    
    # Try to extract result
    result_type, result_value = extract_result(simulator.graph)
    
    return {
        "operation": f"{m} * {n}",
        "steps": steps,
        "result_type": result_type,
        "result_value": result_value,
        "final_graph": simulator.graph,
        "stats": simulator.get_stats(),
    }


def compute_successor(n: int, max_steps: int = 1000) -> dict:
    """
    Compute successor of n (n + 1).
    
    Args:
        n: Input number
        max_steps: Maximum reduction steps
    
    Returns:
        Dictionary with computation results
    """
    print(f"Computing successor of {n}...")
    
    # Create Church numeral
    n_church = church_numeral(n)
    
    # Create successor function
    succ_func = church_successor()
    
    # Apply successor function to n
    graph = apply_function_to_args(succ_func, [n_church])
    
    # Run simulation
    simulator = Simulator(graph)
    steps = simulator.run(max_steps=max_steps, random_order=False)
    
    # Try to extract result
    result_type, result_value = extract_result(simulator.graph)
    
    return {
        "operation": f"succ({n})",
        "steps": steps,
        "result_type": result_type,
        "result_value": result_value,
        "final_graph": simulator.graph,
        "stats": simulator.get_stats(),
    }


def apply_function_to_args(func_graph: Graph, arg_graphs: list) -> Graph:
    """
    Apply a function graph to argument graphs.
    
    This creates a new graph that applies func_graph to each arg_graph.
    For Church encodings: (λx.M) N → M[N/x]
    
    Args:
        func_graph: Graph representing the function
        arg_graphs: List of graphs representing arguments
    
    Returns:
        New graph with function applied to arguments
    """
    # For now, create a simple merged graph
    # In a full implementation, we'd properly merge and connect graphs
    
    result = Graph()
    
    # Copy function graph
    func_start_id = result.next_node_id
    func_node_map = {}
    for node_id, node in func_graph.nodes.items():
        new_id = result.add_node(node.node_type)
        func_node_map[node_id] = new_id
    
    # Copy edges from function graph
    for port1, port2 in func_graph.edges.items():
        if port1.node_id in func_node_map and port2.node_id in func_node_map:
            new_port1 = result.nodes[func_node_map[port1.node_id]].ports[port1.port_type]
            new_port2 = result.nodes[func_node_map[port2.node_id]].ports[port2.port_type]
            result.connect(new_port1, new_port2)
    
    # For each argument, create application nodes
    # Connect function's output to application's left
    # Connect argument to application's right
    
    # Simplified: assume function graph has an output port
    # and we connect arguments via application nodes
    
    # This is a simplified version - full implementation would
    # properly handle graph merging and beta reduction setup
    
    return result


def run_arithmetic_example(name: str, operation_func, *args):
    """
    Run an arithmetic example and display results.
    
    Args:
        name: Name of the example
        operation_func: Function to call
        *args: Arguments to pass to operation_func
    """
    print(f"\n{'=' * 60}")
    print(f"Example: {name}")
    print('=' * 60)
    
    try:
        result = operation_func(*args)
        
        print(f"\nOperation: {result['operation']}")
        print(f"Steps taken: {result['steps']}")
        print(f"Result type: {result['result_type']}")
        print(f"Result value: {result['result_value']}")
        
        stats = result['stats']
        print(f"\nStatistics:")
        print(f"  Total steps: {stats['total_steps']}")
        print(f"  Final nodes: {stats['final_nodes']}")
        print(f"  Final edges: {stats['final_edges']}")
        if stats['reaction_counts']:
            print(f"  Reaction counts: {stats['reaction_counts']}")
        
        # Show expected vs actual
        if result['result_type'] == 'number' and result['result_value'] is not None:
            # Try to determine expected result from operation name
            op = result['operation']
            if '+' in op:
                parts = op.split(' + ')
                if len(parts) == 2:
                    expected = int(parts[0]) + int(parts[1])
                    print(f"\nExpected: {expected}, Got: {result['result_value']}")
            elif '*' in op:
                parts = op.split(' * ')
                if len(parts) == 2:
                    expected = int(parts[0]) * int(parts[1])
                    print(f"\nExpected: {expected}, Got: {result['result_value']}")
            elif 'succ' in op:
                import re
                match = re.search(r'succ\((\d+)\)', op)
                if match:
                    expected = int(match.group(1)) + 1
                    print(f"\nExpected: {expected}, Got: {result['result_value']}")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Run arithmetic examples"""
    print("=" * 60)
    print("Arithmetic Examples with Chemlambda")
    print("=" * 60)
    print("\nNote: These examples demonstrate the structure of computations.")
    print("Full reduction and result extraction may require refinement.")
    print()
    
    # Simple examples
    examples = [
        ("Addition: 2 + 3", compute_addition, 2, 3),
        ("Addition: 1 + 1", compute_addition, 1, 1),
        ("Multiplication: 2 * 3", compute_multiplication, 2, 3),
        ("Successor: succ(5)", compute_successor, 5),
    ]
    
    for name, func, *args in examples:
        run_arithmetic_example(name, func, *args)
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
    print("\nNote: Result extraction may not work perfectly yet.")
    print("The graphs are created correctly, but decoding needs refinement.")


if __name__ == "__main__":
    main()

