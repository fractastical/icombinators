#!/usr/bin/env python3
"""
Lambda Calculus to Chemlambda Compiler
Converts lambda calculus terms to chemlambda graphs
"""

import sys
import os
import re

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chemlambda import Graph, NodeType
from typing import Optional, Dict, List


class LambdaTerm:
    """Represents a lambda calculus term"""
    
    def __init__(self, term_type: str, **kwargs):
        self.term_type = term_type  # 'var', 'abs', 'app'
        self.value = kwargs.get('value')
        self.var = kwargs.get('var')
        self.body = kwargs.get('body')
        self.func = kwargs.get('func')
        self.arg = kwargs.get('arg')
    
    def __repr__(self):
        if self.term_type == 'var':
            return self.value
        elif self.term_type == 'abs':
            return f"λ{self.var}.{self.body}"
        elif self.term_type == 'app':
            return f"({self.func} {self.arg})"
        return str(self.value)


def parse_lambda_term(term: str) -> LambdaTerm:
    """
    Parse a lambda calculus term string.
    
    Supports:
    - Variables: x, y, z, etc.
    - Abstractions: λx.M or \\x.M
    - Applications: M N or (M N)
    
    Args:
        term: Lambda calculus term as string
    
    Returns:
        Parsed LambdaTerm object
    """
    term = term.strip()
    
    # Remove outer parentheses if present
    while term.startswith('(') and term.endswith(')'):
        # Check if parentheses are balanced
        count = 0
        balanced = True
        for i, char in enumerate(term):
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
                if count == 0 and i < len(term) - 1:
                    balanced = False
                    break
        if balanced:
            term = term[1:-1].strip()
        else:
            break
    
    # Try to parse abstraction: λx.M or \x.M
    # Use raw string and escape backslash properly
    abs_match = re.match(r'[λ\\]([a-zA-Z_][a-zA-Z0-9_]*)\.(.+)', term)
    if abs_match:
        var = abs_match.group(1)
        body_str = abs_match.group(2)
        body = parse_lambda_term(body_str)
        return LambdaTerm('abs', var=var, body=body)
    
    # Try to parse application: M N
    # Find the rightmost space that's not inside parentheses
    paren_count = 0
    split_pos = -1
    for i in range(len(term) - 1, -1, -1):
        if term[i] == ')':
            paren_count += 1
        elif term[i] == '(':
            paren_count -= 1
        elif term[i] == ' ' and paren_count == 0:
            split_pos = i
            break
    
    if split_pos > 0:
        func_str = term[:split_pos].strip()
        arg_str = term[split_pos+1:].strip()
        func = parse_lambda_term(func_str)
        arg = parse_lambda_term(arg_str)
        return LambdaTerm('app', func=func, arg=arg)
    
    # Otherwise, it's a variable
    if term:
        return LambdaTerm('var', value=term)
    
    raise ValueError(f"Could not parse lambda term: {term}")


def compile_to_graph(term: LambdaTerm, var_map: Optional[Dict[str, int]] = None) -> Graph:
    """
    Compile a lambda term to a chemlambda graph.
    
    Args:
        term: Parsed lambda term
        var_map: Mapping of variable names to node IDs (for variable references)
    
    Returns:
        Chemlambda graph representing the term
    """
    if var_map is None:
        var_map = {}
    
    graph = Graph()
    
    if term.term_type == 'var':
        # Variable reference
        # Look up in var_map to find the node it refers to
        if term.value in var_map:
            # Variable is bound - create connection to bound variable
            # For now, create a placeholder node
            node_id = graph.add_node(NodeType.ARROW)
            # In full implementation, would connect to the bound variable
            return graph
        else:
            # Free variable - create a node for it
            node_id = graph.add_node(NodeType.FRIN)
            return graph
    
    elif term.term_type == 'abs':
        # Lambda abstraction: λx.M
        # Create L node
        l_id = graph.add_node(NodeType.L)
        l_node = graph.nodes[l_id]
        
        # Compile body with x added to var_map
        body_graph = compile_to_graph(term.body, {**var_map, term.var: l_id})
        
        # Merge body graph into main graph
        body_start_id = graph.next_node_id
        body_node_map = {}
        for node_id, node in body_graph.nodes.items():
            new_id = graph.add_node(node.node_type)
            body_node_map[node_id] = new_id
        
        # Copy edges from body graph
        for port1, port2 in body_graph.edges.items():
            if port1.node_id in body_node_map and port2.node_id in body_node_map:
                new_port1 = graph.nodes[body_node_map[port1.node_id]].ports[port1.port_type]
                new_port2 = graph.nodes[body_node_map[port2.node_id]].ports[port2.port_type]
                graph.connect(new_port1, new_port2)
        
        # Connect lambda body to compiled body
        # The body's output should connect to lambda's left port
        # Find output port of body (free output or application result)
        # For now, connect lambda's left to body's entry point
        
        # Connect lambda's right port (bound variable) to body
        # This is simplified - full implementation would properly handle variable binding
        
        return graph
    
    elif term.term_type == 'app':
        # Application: M N
        # Create A node
        a_id = graph.add_node(NodeType.A)
        a_node = graph.nodes[a_id]
        
        # Compile function and argument
        func_graph = compile_to_graph(term.func, var_map)
        arg_graph = compile_to_graph(term.arg, var_map)
        
        # Merge function graph
        func_start_id = graph.next_node_id
        func_node_map = {}
        for node_id, node in func_graph.nodes.items():
            new_id = graph.add_node(node.node_type)
            func_node_map[node_id] = new_id
        
        for port1, port2 in func_graph.edges.items():
            if port1.node_id in func_node_map and port2.node_id in func_node_map:
                new_port1 = graph.nodes[func_node_map[port1.node_id]].ports[port1.port_type]
                new_port2 = graph.nodes[func_node_map[port2.node_id]].ports[port2.port_type]
                graph.connect(new_port1, new_port2)
        
        # Merge argument graph
        arg_start_id = graph.next_node_id
        arg_node_map = {}
        for node_id, node in arg_graph.nodes.items():
            new_id = graph.add_node(node.node_type)
            arg_node_map[node_id] = new_id
        
        for port1, port2 in arg_graph.edges.items():
            if port1.node_id in arg_node_map and port2.node_id in arg_node_map:
                new_port1 = graph.nodes[arg_node_map[port1.node_id]].ports[port1.port_type]
                new_port2 = graph.nodes[arg_node_map[port2.node_id]].ports[port2.port_type]
                graph.connect(new_port1, new_port2)
        
        # Connect function output to application's left input
        # Connect argument to application's right input
        # This is simplified - full implementation would find proper output ports
        
        return graph
    
    return graph


def compile_lambda_string(term_str: str) -> Graph:
    """
    Convenience function to compile a lambda term string directly.
    
    Args:
        term_str: Lambda calculus term as string
    
    Returns:
        Chemlambda graph
    """
    term = parse_lambda_term(term_str)
    return compile_to_graph(term)


def main():
    """Test lambda compiler"""
    print("=" * 60)
    print("Lambda Calculus to Chemlambda Compiler")
    print("=" * 60)
    print()
    
    test_terms = [
        "x",
        "λx.x",
        "λx.λy.x",
        "(λx.x) y",
        "λf.λx.f x",
        "λm.λn.m n",
    ]
    
    for term_str in test_terms:
        print(f"\nTerm: {term_str}")
        try:
            term = parse_lambda_term(term_str)
            print(f"  Parsed: {term}")
            
            graph = compile_to_graph(term)
            print(f"  Graph: {graph} ({len(graph.nodes)} nodes, {len(graph.edges)//2} edges)")
            
            # Show node types
            node_types = {}
            for node in graph.nodes.values():
                node_type = node.node_type.value
                node_types[node_type] = node_types.get(node_type, 0) + 1
            print(f"  Node types: {node_types}")
        
        except Exception as e:
            print(f"  Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Note: This is a simplified compiler.")
    print("Full implementation would properly handle variable binding")
    print("and graph connections for beta reduction.")
    print("=" * 60)


if __name__ == "__main__":
    main()

