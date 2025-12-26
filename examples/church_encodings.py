#!/usr/bin/env python3
"""
Church Encodings for Chemlambda
Implements Church numerals, booleans, and basic operations
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chemlambda import Graph, NodeType


def church_numeral(n: int) -> Graph:
    """
    Create a Church numeral encoding of n.
    
    Church numeral n = λf.λx.f^n(x)
    - n = 0: λf.λx.x (return x unchanged)
    - n = 1: λf.λx.f(x)
    - n = 2: λf.λx.f(f(x))
    - etc.
    
    Args:
        n: The natural number to encode (must be >= 0)
    
    Returns:
        Graph representing the Church numeral
    """
    if n < 0:
        raise ValueError("Church numerals must be non-negative")
    
    graph = Graph()
    
    # Outer lambda: λf (binds f)
    outer_l_id = graph.add_node(NodeType.L)
    outer_l = graph.nodes[outer_l_id]
    
    # Inner lambda: λx (binds x)
    inner_l_id = graph.add_node(NodeType.L)
    inner_l = graph.nodes[inner_l_id]
    
    # Connect outer lambda body to inner lambda (outer returns inner)
    graph.connect(outer_l.ports["left"], inner_l.ports["middle"])
    
    if n == 0:
        # λf.λx.x - return x unchanged
        # Connect inner lambda body (left.out) directly to x (right.out)
        graph.connect(inner_l.ports["left"], inner_l.ports["right"])
        # f is unused, connect to termination
        t_id = graph.add_node(NodeType.T)
        t = graph.nodes[t_id]
        graph.connect(outer_l.ports["right"], t.ports["middle"])
    else:
        # Build chain: f(f(...f(x)...)) with n applications
        # We need to apply f n times to x
        
        # Track the chain: start with x
        prev_output = inner_l.ports["right"]  # x
        
        # Create n application nodes
        app_ids = []
        for i in range(n):
            app_id = graph.add_node(NodeType.A)
            app_ids.append(app_id)
            app = graph.nodes[app_id]
            
            # Connect f to left input of application
            # f needs to be duplicated for each application
            # Use fan-out to duplicate f
            if i == 0:
                # First app: connect f directly
                graph.connect(outer_l.ports["right"], app.ports["left"])
            else:
                # Need to duplicate f - create fan-out
                fo_id = graph.add_node(NodeType.FO)
                fo = graph.nodes[fo_id]
                graph.connect(outer_l.ports["right"], fo.ports["middle"])
                # Connect one output to this app
                graph.connect(fo.ports["left"], app.ports["left"])
                # Connect other output to previous app (if needed)
                if i < n - 1:
                    # We'll need more fan-outs, but for now connect
                    pass
            
            # Connect previous output to right input
            graph.connect(prev_output, app.ports["right"])
            
            # This app's output becomes input for next
            prev_output = app.ports["middle"]
        
        # Connect final result to inner lambda body
        graph.connect(inner_l.ports["left"], prev_output)
    
    return graph


def church_boolean(value: bool) -> Graph:
    """
    Create a Church boolean encoding.
    
    true = λx.λy.x  (selects first argument)
    false = λx.λy.y (selects second argument)
    
    Args:
        value: True or False
    
    Returns:
        Graph representing the Church boolean
    """
    graph = Graph()
    
    # Outer lambda: λx
    outer_l_id = graph.add_node(NodeType.L)
    outer_l = graph.nodes[outer_l_id]
    
    # Inner lambda: λy
    inner_l_id = graph.add_node(NodeType.L)
    inner_l = graph.nodes[inner_l_id]
    
    # Connect outer lambda body to inner lambda
    graph.connect(outer_l.ports["left"], inner_l.ports["middle"])
    
    if value:  # true = λx.λy.x
        # Return x (first argument)
        graph.connect(inner_l.ports["left"], outer_l.ports["right"])
        # y is unused, connect to termination
        t_id = graph.add_node(NodeType.T)
        t = graph.nodes[t_id]
        graph.connect(inner_l.ports["right"], t.ports["middle"])
    else:  # false = λx.λy.y
        # Return y (second argument)
        graph.connect(inner_l.ports["left"], inner_l.ports["right"])
        # x is unused, connect to termination
        t_id = graph.add_node(NodeType.T)
        t = graph.nodes[t_id]
        graph.connect(outer_l.ports["right"], t.ports["middle"])
    
    return graph


def church_successor() -> Graph:
    """
    Create successor function: succ = λn.λf.λx.f(n f x)
    
    Successor adds one more application of f.
    
    Returns:
        Graph representing the successor function
    """
    graph = Graph()
    
    # Outer lambda: λn
    outer_l_id = graph.add_node(NodeType.L)
    outer_l = graph.nodes[outer_l_id]
    
    # Middle lambda: λf
    middle_l_id = graph.add_node(NodeType.L)
    middle_l = graph.nodes[middle_l_id]
    
    # Inner lambda: λx
    inner_l_id = graph.add_node(NodeType.L)
    inner_l = graph.nodes[inner_l_id]
    
    # Connect lambdas: outer -> middle -> inner
    graph.connect(outer_l.ports["left"], middle_l.ports["middle"])
    graph.connect(middle_l.ports["left"], inner_l.ports["middle"])
    
    # Build: f(n f x)
    # First apply n to f: (n f)
    app1_id = graph.add_node(NodeType.A)
    app1 = graph.nodes[app1_id]
    graph.connect(outer_l.ports["right"], app1.ports["left"])  # n
    graph.connect(middle_l.ports["right"], app1.ports["right"])  # f
    
    # Then apply f to result: f((n f) x)
    app2_id = graph.add_node(NodeType.A)
    app2 = graph.nodes[app2_id]
    graph.connect(middle_l.ports["right"], app2.ports["left"])  # f
    graph.connect(app1.ports["middle"], app2.ports["right"])  # (n f)
    
    # Apply (n f) to x: (n f) x
    app3_id = graph.add_node(NodeType.A)
    app3 = graph.nodes[app3_id]
    graph.connect(app1.ports["middle"], app3.ports["left"])  # (n f)
    graph.connect(inner_l.ports["right"], app3.ports["right"])  # x
    
    # Finally apply f to result: f((n f) x)
    graph.connect(app2.ports["middle"], app3.ports["middle"])
    graph.connect(inner_l.ports["left"], app2.ports["middle"])
    
    return graph


def church_add() -> Graph:
    """
    Create addition function: add = λm.λn.λf.λx.m f (n f x)
    
    Addition is applying m times, then n times.
    
    Returns:
        Graph representing the addition function
    """
    graph = Graph()
    
    # Outer lambda: λm
    outer_l_id = graph.add_node(NodeType.L)
    outer_l = graph.nodes[outer_l_id]
    
    # Second lambda: λn
    second_l_id = graph.add_node(NodeType.L)
    second_l = graph.nodes[second_l_id]
    
    # Third lambda: λf
    third_l_id = graph.add_node(NodeType.L)
    third_l = graph.nodes[third_l_id]
    
    # Inner lambda: λx
    inner_l_id = graph.add_node(NodeType.L)
    inner_l = graph.nodes[inner_l_id]
    
    # Connect lambdas
    graph.connect(outer_l.ports["left"], second_l.ports["middle"])
    graph.connect(second_l.ports["left"], third_l.ports["middle"])
    graph.connect(third_l.ports["left"], inner_l.ports["middle"])
    
    # Build: m f (n f x)
    # First: n f x
    app1_id = graph.add_node(NodeType.A)
    app1 = graph.nodes[app1_id]
    graph.connect(second_l.ports["right"], app1.ports["left"])  # n
    graph.connect(third_l.ports["right"], app1.ports["right"])  # f
    
    app2_id = graph.add_node(NodeType.A)
    app2 = graph.nodes[app2_id]
    graph.connect(app1.ports["middle"], app2.ports["left"])  # (n f)
    graph.connect(inner_l.ports["right"], app2.ports["right"])  # x
    
    # Then: m f (n f x)
    app3_id = graph.add_node(NodeType.A)
    app3 = graph.nodes[app3_id]
    graph.connect(outer_l.ports["right"], app3.ports["left"])  # m
    graph.connect(third_l.ports["right"], app3.ports["right"])  # f
    
    app4_id = graph.add_node(NodeType.A)
    app4 = graph.nodes[app4_id]
    graph.connect(app3.ports["middle"], app4.ports["left"])  # (m f)
    graph.connect(app2.ports["middle"], app4.ports["right"])  # (n f x)
    
    # Connect result
    graph.connect(inner_l.ports["left"], app4.ports["middle"])
    
    return graph


def church_multiply() -> Graph:
    """
    Create multiplication function: mult = λm.λn.λf.m (n f)
    
    Multiplication is composing m and n.
    
    Returns:
        Graph representing the multiplication function
    """
    graph = Graph()
    
    # Outer lambda: λm
    outer_l_id = graph.add_node(NodeType.L)
    outer_l = graph.nodes[outer_l_id]
    
    # Second lambda: λn
    second_l_id = graph.add_node(NodeType.L)
    second_l = graph.nodes[second_l_id]
    
    # Third lambda: λf
    third_l_id = graph.add_node(NodeType.L)
    third_l = graph.nodes[third_l_id]
    
    # Connect lambdas
    graph.connect(outer_l.ports["left"], second_l.ports["middle"])
    graph.connect(second_l.ports["left"], third_l.ports["middle"])
    
    # Build: m (n f)
    # First: n f
    app1_id = graph.add_node(NodeType.A)
    app1 = graph.nodes[app1_id]
    graph.connect(second_l.ports["right"], app1.ports["left"])  # n
    graph.connect(third_l.ports["right"], app1.ports["right"])  # f
    
    # Then: m (n f)
    app2_id = graph.add_node(NodeType.A)
    app2 = graph.nodes[app2_id]
    graph.connect(outer_l.ports["right"], app2.ports["left"])  # m
    graph.connect(app1.ports["middle"], app2.ports["right"])  # (n f)
    
    # Connect result
    graph.connect(third_l.ports["left"], app2.ports["middle"])
    
    return graph


def apply_church_function(func_graph: Graph, arg_graph: Graph) -> Graph:
    """
    Apply a Church-encoded function to an argument.
    
    Creates a new graph that applies func_graph to arg_graph.
    
    Args:
        func_graph: Graph representing the function
        arg_graph: Graph representing the argument
    
    Returns:
        New graph with the application
    """
    # Clone both graphs
    func = func_graph.clone()
    arg = arg_graph.clone()
    
    # Merge graphs (need to handle node ID conflicts)
    # Find the output port of func (right port of outer lambda)
    # Find a suitable input port of arg
    
    # For now, create a simple application node
    result = Graph()
    
    # Add all nodes from func
    func_start_id = result.next_node_id
    for node_id, node in func.nodes.items():
        new_id = result.add_node(node.node_type)
        # Note: node IDs will be different, need to remap connections
    
    # This is complex - let's use a simpler approach
    # Create an application node connecting func to arg
    app_id = result.add_node(NodeType.A)
    app = result.nodes[app_id]
    
    # We need to connect func's output to app's left
    # and arg to app's right
    # But we need to properly merge the graphs first
    
    # Simplified: assume func and arg are already complete graphs
    # and we just need to connect them via an application
    
    # For now, return a placeholder
    # TODO: Implement proper graph merging and connection
    return result


def main():
    """Demonstrate Church encodings"""
    print("=" * 60)
    print("Church Encodings Demonstration")
    print("=" * 60)
    print()
    
    # Test Church numerals
    print("Church Numerals:")
    for n in range(5):
        graph = church_numeral(n)
        print(f"  {n}: {graph} ({len(graph.nodes)} nodes)")
    
    print()
    
    # Test Church booleans
    print("Church Booleans:")
    true_graph = church_boolean(True)
    false_graph = church_boolean(False)
    print(f"  true: {true_graph} ({len(true_graph.nodes)} nodes)")
    print(f"  false: {false_graph} ({len(false_graph.nodes)} nodes)")
    
    print()
    
    # Test operations
    print("Church Operations:")
    succ_graph = church_successor()
    add_graph = church_add()
    mult_graph = church_multiply()
    print(f"  successor: {succ_graph} ({len(succ_graph.nodes)} nodes)")
    print(f"  add: {add_graph} ({len(add_graph.nodes)} nodes)")
    print(f"  multiply: {mult_graph} ({len(mult_graph.nodes)} nodes)")


if __name__ == "__main__":
    main()

