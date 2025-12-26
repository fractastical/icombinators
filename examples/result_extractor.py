#!/usr/bin/env python3
"""
Result Extraction from Chemlambda Graphs
Extracts values (Church numerals, booleans) from final graph structures
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chemlambda import Graph, NodeType
from typing import Optional, List, Tuple


def decode_church_numeral(graph: Graph) -> Optional[int]:
    """
    Decode a Church numeral from a graph.
    
    A Church numeral n has the structure: λf.λx.f^n(x)
    We need to identify this pattern and count the number of f applications.
    
    Args:
        graph: The graph to decode
    
    Returns:
        The decoded number, or None if not a valid Church numeral
    """
    # Look for pattern: L -> L -> ... (nested lambdas)
    # Outer lambda should bind f, inner lambda should bind x
    # Then count applications of f
    
    # Find all L nodes
    l_nodes = [node_id for node_id, node in graph.nodes.items() 
               if node.node_type == NodeType.L]
    
    if len(l_nodes) < 2:
        # Need at least 2 lambdas (outer and inner)
        return None
    
    # Try to find the Church numeral pattern
    # Look for: L (outer) -> L (inner) -> A (applications)
    
    # Find outer lambda (one that has another L connected to its left)
    outer_l_id = None
    inner_l_id = None
    
    for l_id in l_nodes:
        l_node = graph.nodes[l_id]
        left_port = l_node.ports.get("left")
        if left_port:
            connected = graph.get_connected(left_port)
            if connected:
                connected_node = graph.nodes.get(connected.node_id)
                if connected_node and connected_node.node_type == NodeType.L:
                    outer_l_id = connected.node_id
                    inner_l_id = l_id
                    break
    
    if outer_l_id is None or inner_l_id is None:
        # Try reverse: maybe inner is first
        for l_id in l_nodes:
            l_node = graph.nodes[l_id]
            middle_port = l_node.ports.get("middle")
            if middle_port:
                connected = graph.get_connected(middle_port)
                if connected:
                    connected_node = graph.nodes.get(connected.node_id)
                    if connected_node and connected_node.node_type == NodeType.L:
                        inner_l_id = connected.node_id
                        outer_l_id = l_id
                        break
    
    if outer_l_id is None or inner_l_id is None:
        # Couldn't find nested lambda structure
        # Maybe it's a simpler structure (like Church 0 or 1)
        return _try_simple_church_decode(graph)
    
    # Found nested lambdas, now count applications
    # Start from inner lambda's left port and trace applications
    inner_l = graph.nodes[inner_l_id]
    outer_l = graph.nodes[outer_l_id]
    
    # Check if this is Church 0: λf.λx.x (no applications)
    inner_left = inner_l.ports.get("left")
    inner_right = inner_l.ports.get("right")
    
    if inner_left and inner_right:
        connected_left = graph.get_connected(inner_left)
        connected_right = graph.get_connected(inner_right)
        
        # If left connects directly to right, it's Church 0
        if connected_left == inner_right or connected_right == inner_left:
            return 0
    
    # Count applications by traversing from inner lambda's left
    count = _count_applications(graph, inner_l, outer_l)
    
    return count


def _try_simple_church_decode(graph: Graph) -> Optional[int]:
    """Try to decode simpler Church numeral structures"""
    # Church 0: λf.λx.x - just returns x
    # Look for L -> L where inner L's left connects to its right
    
    l_nodes = [node_id for node_id, node in graph.nodes.items() 
               if node.node_type == NodeType.L]
    
    if len(l_nodes) == 2:
        # Check if it's Church 0
        for l_id in l_nodes:
            l_node = graph.nodes[l_id]
            left = l_node.ports.get("left")
            right = l_node.ports.get("right")
            if left and right:
                connected_left = graph.get_connected(left)
                if connected_left == right:
                    return 0
    
    return None


def _count_applications(graph: Graph, inner_l, outer_l) -> int:
    """
    Count the number of applications in a Church numeral.
    
    Traverses from inner lambda's left port, counting A nodes
    that form a chain.
    """
    inner_left = inner_l.ports.get("left")
    if not inner_left:
        return 0
    
    # Start traversal from inner lambda's left
    count = 0
    visited = set()
    current_port = inner_left
    
    while current_port:
        if current_port in visited:
            break
        visited.add(current_port)
        
        # Check if this port is connected to an application
        connected = graph.get_connected(current_port)
        if not connected:
            break
        
        connected_node = graph.nodes.get(connected.node_id)
        if not connected_node:
            break
        
        if connected_node.node_type == NodeType.A:
            count += 1
            # Move to application's middle (output)
            app_middle = connected_node.ports.get("middle")
            if app_middle:
                current_port = app_middle
            else:
                break
        elif connected_node.node_type == NodeType.ARROW:
            # Arrow node, continue traversal
            arrow_out = connected_node.ports.get("middle_out")
            if arrow_out:
                current_port = arrow_out
            else:
                break
        else:
            # Not an application, stop counting
            break
        
        # Limit to prevent infinite loops
        if count > 100:
            break
    
    return count


def decode_church_boolean(graph: Graph) -> Optional[bool]:
    """
    Decode a Church boolean from a graph.
    
    true = λx.λy.x  (selects first argument)
    false = λx.λy.y (selects second argument)
    
    Args:
        graph: The graph to decode
    
    Returns:
        The decoded boolean, or None if not a valid Church boolean
    """
    # Find nested lambdas: L -> L
    l_nodes = [node_id for node_id, node in graph.nodes.items() 
               if node.node_type == NodeType.L]
    
    if len(l_nodes) < 2:
        return None
    
    # Find outer and inner lambdas
    outer_l_id = None
    inner_l_id = None
    
    for l_id in l_nodes:
        l_node = graph.nodes[l_id]
        left_port = l_node.ports.get("left")
        if left_port:
            connected = graph.get_connected(left_port)
            if connected:
                connected_node = graph.nodes.get(connected.node_id)
                if connected_node and connected_node.node_type == NodeType.L:
                    outer_l_id = connected.node_id
                    inner_l_id = l_id
                    break
    
    if outer_l_id is None or inner_l_id is None:
        return None
    
    outer_l = graph.nodes[outer_l_id]
    inner_l = graph.nodes[inner_l_id]
    
    # Check inner lambda's left port
    # If it connects to outer_l's right (x), it's true
    # If it connects to inner_l's right (y), it's false
    
    inner_left = inner_l.ports.get("left")
    outer_right = outer_l.ports.get("right")
    inner_right = inner_l.ports.get("right")
    
    if not (inner_left and outer_right and inner_right):
        return None
    
    connected_to_inner_left = graph.get_connected(inner_left)
    
    if connected_to_inner_left == outer_right:
        return True  # true = λx.λy.x
    elif connected_to_inner_left == inner_right:
        return False  # false = λx.λy.y
    
    return None


def extract_result(graph: Graph) -> Tuple[Optional[str], Optional[any]]:
    """
    Try to extract a result from a graph.
    
    Attempts to decode as Church numeral first, then Church boolean.
    
    Args:
        graph: The graph to extract result from
    
    Returns:
        Tuple of (type, value) where type is "number", "boolean", or None
    """
    # Try Church numeral first
    num = decode_church_numeral(graph)
    if num is not None:
        return ("number", num)
    
    # Try Church boolean
    bool_val = decode_church_boolean(graph)
    if bool_val is not None:
        return ("boolean", bool_val)
    
    return (None, None)


def graph_structure_summary(graph: Graph) -> dict:
    """
    Get a summary of graph structure for debugging.
    
    Args:
        graph: The graph to analyze
    
    Returns:
        Dictionary with structure information
    """
    node_counts = {}
    for node in graph.nodes.values():
        node_type = node.node_type.value
        node_counts[node_type] = node_counts.get(node_type, 0) + 1
    
    # Count connections
    connection_count = len(graph.edges) // 2
    
    # Find lambda nodes
    l_nodes = [node_id for node_id, node in graph.nodes.items() 
               if node.node_type == NodeType.L]
    
    # Find application nodes
    a_nodes = [node_id for node_id, node in graph.nodes.items() 
               if node.node_type == NodeType.A]
    
    return {
        "total_nodes": len(graph.nodes),
        "total_edges": connection_count,
        "node_types": node_counts,
        "lambda_count": len(l_nodes),
        "application_count": len(a_nodes),
    }


def main():
    """Test result extraction"""
    print("=" * 60)
    print("Result Extraction Test")
    print("=" * 60)
    print()
    
    # Import church encodings
    from church_encodings import church_numeral, church_boolean
    
    # Test Church numeral decoding
    print("Testing Church Numeral Decoding:")
    for n in range(5):
        graph = church_numeral(n)
        decoded = decode_church_numeral(graph)
        summary = graph_structure_summary(graph)
        print(f"  Encoded {n}: {decoded} (nodes: {summary['total_nodes']}, "
              f"lambdas: {summary['lambda_count']}, apps: {summary['application_count']})")
    
    print()
    
    # Test Church boolean decoding
    print("Testing Church Boolean Decoding:")
    for val in [True, False]:
        graph = church_boolean(val)
        decoded = decode_church_boolean(graph)
        summary = graph_structure_summary(graph)
        print(f"  Encoded {val}: {decoded} (nodes: {summary['total_nodes']})")
    
    print()
    
    # Test general extraction
    print("Testing General Extraction:")
    test_graphs = [
        (church_numeral(3), "Church 3"),
        (church_boolean(True), "Church true"),
        (church_numeral(0), "Church 0"),
    ]
    
    for graph, name in test_graphs:
        result_type, result_value = extract_result(graph)
        print(f"  {name}: type={result_type}, value={result_value}")


if __name__ == "__main__":
    main()

