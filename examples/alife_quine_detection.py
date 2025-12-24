#!/usr/bin/env python3
"""
Example: Quine Detection for Artificial Life
Demonstrates detecting and analyzing quine graphs
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chemlambda import Graph, NodeType, Simulator
from chemlambda.examples import create_quine_like_structure, create_ouroboros_like

# Import ALife module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.alife.quine_detector import QuineAnalyzer, detect_quine, measure_replication_rate


def test_quine_detection():
    """Test quine detection on example graphs"""
    
    print("=" * 70)
    print("Quine Detection Test")
    print("=" * 70)
    print()
    
    # Test 1: Quine-like structure
    print("Test 1: Quine-like Structure")
    print("-" * 70)
    quine_graph = create_quine_like_structure()
    analyzer = QuineAnalyzer(quine_graph)
    analysis = analyzer.analyze()
    
    print(f"Is Quine: {analysis.get('is_quine', False)}")
    print(f"Size: {analysis.get('size', 0)} nodes")
    print(f"Node Types: {analysis.get('node_types', {})}")
    print(f"Connectivity: {analysis.get('connectivity', 0.0):.2f}")
    
    if analysis.get('is_quine'):
        replication_rate = measure_replication_rate(quine_graph, steps=50)
        print(f"Replication Rate: {replication_rate:.4f}")
    
    print()
    
    # Test 2: Ouroboros
    print("Test 2: Ouroboros Structure")
    print("-" * 70)
    ouroboros_graph = create_ouroboros_like()
    analyzer2 = QuineAnalyzer(ouroboros_graph)
    analysis2 = analyzer2.analyze()
    
    print(f"Is Quine: {analysis2.get('is_quine', False)}")
    print(f"Size: {analysis2.get('size', 0)} nodes")
    print(f"Node Types: {analysis2.get('node_types', {})}")
    print(f"Connectivity: {analysis2.get('connectivity', 0.0):.2f}")
    
    if analysis2.get('is_quine'):
        replication_rate = measure_replication_rate(ouroboros_graph, steps=50)
        print(f"Replication Rate: {replication_rate:.4f}")
    
    print()
    
    # Test 3: Simple graph (not a quine)
    print("Test 3: Simple Application (Not a Quine)")
    print("-" * 70)
    simple_graph = Graph()
    l_id = simple_graph.add_node(NodeType.L)
    a_id = simple_graph.add_node(NodeType.A)
    l_node = simple_graph.nodes[l_id]
    a_node = simple_graph.nodes[a_id]
    simple_graph.connect(l_node.ports["right"], a_node.ports["left"])
    
    analyzer3 = QuineAnalyzer(simple_graph)
    analysis3 = analyzer3.analyze()
    
    print(f"Is Quine: {analysis3.get('is_quine', False)}")
    print(f"Size: {analysis3.get('size', 0)} nodes")
    print()
    
    print("=" * 70)
    print("Quine Detection Test Complete")
    print("=" * 70)


if __name__ == "__main__":
    test_quine_detection()

