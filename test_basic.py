#!/usr/bin/env python3
"""
Basic tests for chemlambda implementation
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chemlambda import Graph, NodeType, Simulator


def test_graph_creation():
    """Test basic graph creation"""
    print("Test 1: Graph Creation")
    graph = Graph()
    
    l_id = graph.add_node(NodeType.L)
    a_id = graph.add_node(NodeType.A)
    
    assert len(graph.nodes) == 2
    assert l_id in graph.nodes
    assert a_id in graph.nodes
    
    print("  ✓ Graph creation works")
    return True


def test_connections():
    """Test node connections"""
    print("Test 2: Node Connections")
    graph = Graph()
    
    l_id = graph.add_node(NodeType.L)
    a_id = graph.add_node(NodeType.A)
    
    l_node = graph.nodes[l_id]
    a_node = graph.nodes[a_id]
    
    graph.connect(l_node.ports["right"], a_node.ports["left"])
    
    connected = graph.get_connected(l_node.ports["right"])
    assert connected == a_node.ports["left"]
    
    print("  ✓ Node connections work")
    return True


def test_beta_reaction():
    """Test BETA reaction"""
    print("Test 3: BETA Reaction")
    from chemlambda.reactions import BetaReaction
    
    graph = Graph()
    l_id = graph.add_node(NodeType.L)
    a_id = graph.add_node(NodeType.A)
    
    l_node = graph.nodes[l_id]
    a_node = graph.nodes[a_id]
    
    # Connect L.right.out to A.left.in (BETA pattern)
    graph.connect(l_node.ports["right"], a_node.ports["left"])
    
    reaction = BetaReaction()
    matches = reaction.can_apply(graph)
    
    assert len(matches) > 0
    
    # Apply reaction
    success = reaction.apply(graph, matches[0])
    assert success
    
    print("  ✓ BETA reaction works")
    return True


def test_simulator():
    """Test simulator"""
    print("Test 4: Simulator")
    from chemlambda import create_simple_application
    
    graph = create_simple_application()
    simulator = Simulator(graph)
    
    # Run one step
    applied = simulator.step()
    
    assert applied  # Should apply BETA
    
    stats = simulator.get_stats()
    assert stats['total_steps'] > 0
    assert 'BETA' in stats['reaction_counts']
    
    print("  ✓ Simulator works")
    return True


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Basic Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_graph_creation,
        test_connections,
        test_beta_reaction,
        test_simulator,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"  ✗ {test.__name__} failed")
        except Exception as e:
            failed += 1
            print(f"  ✗ {test.__name__} failed with error: {e}")
        print()
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

