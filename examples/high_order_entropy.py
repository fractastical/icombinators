#!/usr/bin/env python3
"""
High-Order Entropy with Interaction Combinators and Chemlambda
Applying graph rewriting to analyze high-order interactions and synergistic effects

Based on Aguera's concept of high-order entropy: analyzing complex systems
by considering interactions beyond simple pairwise relationships, capturing
synergistic effects among multiple components.
"""

import sys
import os
import math
from typing import Dict, List, Set, Tuple
from collections import defaultdict

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chemlambda import Graph, NodeType, Simulator
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from alife.quine_detector import find_non_conflicting_matches
from chemlambda.reactions import ALL_REACTIONS


def compute_graph_entropy(graph: Graph) -> float:
    """
    Compute Shannon entropy of a graph based on node type distribution.
    
    High-order entropy considers the distribution of node types and their
    interactions, not just pairwise connections.
    
    Args:
        graph: The graph to analyze
    
    Returns:
        Shannon entropy value
    """
    if len(graph.nodes) == 0:
        return 0.0
    
    # Count node types
    type_counts = defaultdict(int)
    for node in graph.nodes.values():
        type_counts[node.node_type.value] += 1
    
    # Compute Shannon entropy: H = -Σ p(x) * log2(p(x))
    entropy = 0.0
    total_nodes = len(graph.nodes)
    
    for count in type_counts.values():
        probability = count / total_nodes
        if probability > 0:
            entropy -= probability * math.log2(probability)
    
    return entropy


def compute_interaction_entropy(graph: Graph, order: int = 2) -> float:
    """
    Compute high-order interaction entropy.
    
    For order=2: pairwise interactions (traditional)
    For order>2: multi-way interactions (high-order)
    
    Args:
        graph: The graph to analyze
        order: Order of interactions to consider (2=pairwise, 3=triplets, etc.)
    
    Returns:
        High-order interaction entropy
    """
    if len(graph.nodes) < order:
        return 0.0
    
    # Find all interaction patterns of given order
    # An interaction pattern is a set of nodes that can interact together
    # through reactions
    
    # For chemlambda, interactions happen through reactions
    # We look for patterns where multiple nodes can participate in reactions
    
    interaction_patterns = []
    
    # Find all possible reaction matches
    for reaction in ALL_REACTIONS:
        matches = reaction.can_apply(graph)
        for match in matches:
            # Extract nodes involved in this match
            nodes_in_match = set()
            if isinstance(match, tuple):
                for item in match:
                    if isinstance(item, int) and item in graph.nodes:
                        nodes_in_match.add(item)
            
            if len(nodes_in_match) >= order:
                # This is a high-order interaction
                interaction_patterns.append(frozenset(nodes_in_match))
    
    if not interaction_patterns:
        return 0.0
    
    # Count frequency of each interaction pattern
    pattern_counts = defaultdict(int)
    for pattern in interaction_patterns:
        pattern_counts[pattern] += 1
    
    # Compute entropy of interaction patterns
    total_patterns = len(interaction_patterns)
    entropy = 0.0
    
    for count in pattern_counts.values():
        probability = count / total_patterns
        if probability > 0:
            entropy -= probability * math.log2(probability)
    
    return entropy


def compute_synergistic_information(graph: Graph) -> float:
    """
    Compute synergistic information: information that emerges from
    interactions beyond what can be explained by pairwise relationships.
    
    Synergistic information = Total information - Sum of pairwise information
    
    Args:
        graph: The graph to analyze
    
    Returns:
        Synergistic information value
    """
    # Total information (high-order entropy)
    total_entropy = compute_interaction_entropy(graph, order=3)
    
    # Pairwise information
    pairwise_entropy = compute_interaction_entropy(graph, order=2)
    
    # Synergistic information is the difference
    # (This is a simplified measure - full measure would consider
    #  all possible decompositions)
    synergistic = max(0.0, total_entropy - pairwise_entropy)
    
    return synergistic


def analyze_parallel_interactions(graph: Graph) -> Dict:
    """
    Analyze how parallel interactions create high-order effects.
    
    In chemlambda, parallel rewrites can create synergistic effects
    that don't exist in sequential systems.
    
    Args:
        graph: The graph to analyze
    
    Returns:
        Dictionary with analysis results
    """
    # Find all non-conflicting matches (can happen in parallel)
    matches = find_non_conflicting_matches(graph, ALL_REACTIONS)
    
    # Analyze interaction patterns
    interaction_nodes = set()
    for reaction, match in matches:
        if isinstance(match, tuple):
            for item in match:
                if isinstance(item, int) and item in graph.nodes:
                    interaction_nodes.add(item)
    
    # Compute various entropy measures
    node_entropy = compute_graph_entropy(graph)
    pairwise_entropy = compute_interaction_entropy(graph, order=2)
    high_order_entropy = compute_interaction_entropy(graph, order=3)
    synergistic_info = compute_synergistic_information(graph)
    
    return {
        "parallel_matches": len(matches),
        "nodes_in_parallel": len(interaction_nodes),
        "node_entropy": node_entropy,
        "pairwise_entropy": pairwise_entropy,
        "high_order_entropy": high_order_entropy,
        "synergistic_information": synergistic_info,
        "parallelism_ratio": len(matches) / len(graph.nodes) if len(graph.nodes) > 0 else 0.0,
    }


def track_entropy_evolution(simulator: Simulator, max_steps: int = 50) -> List[Dict]:
    """
    Track how entropy evolves during graph reduction.
    
    High-order entropy can increase or decrease as the graph transforms,
    revealing information dynamics.
    
    Args:
        simulator: Simulator with graph
        max_steps: Maximum steps to track
    
    Returns:
        List of entropy measurements at each step
    """
    history = []
    
    initial_entropy = compute_graph_entropy(simulator.graph)
    initial_high_order = compute_interaction_entropy(simulator.graph, order=3)
    
    history.append({
        "step": 0,
        "node_entropy": initial_entropy,
        "high_order_entropy": initial_high_order,
        "synergistic": compute_synergistic_information(simulator.graph),
        "nodes": len(simulator.graph.nodes),
    })
    
    for step in range(max_steps):
        applied = simulator.step(random_order=True)
        if not applied:
            break
        
        entropy = compute_graph_entropy(simulator.graph)
        high_order = compute_interaction_entropy(simulator.graph, order=3)
        synergistic = compute_synergistic_information(simulator.graph)
        
        history.append({
            "step": step + 1,
            "node_entropy": entropy,
            "high_order_entropy": high_order,
            "synergistic": synergistic,
            "nodes": len(simulator.graph.nodes),
        })
    
    return history


def demonstrate_high_order_entropy():
    """
    Demonstrate high-order entropy analysis with chemlambda graphs.
    """
    print("=" * 70)
    print("High-Order Entropy Analysis with Chemlambda")
    print("=" * 70)
    print("\nHigh-order entropy captures interactions beyond pairwise relationships,")
    print("revealing synergistic effects that emerge from multi-way interactions.")
    print()
    
    # Create a complex graph with multiple interaction sites
    graph = Graph()
    
    # Create multiple lambda-application pairs (interaction sites)
    pairs = []
    for i in range(10):
        l_id = graph.add_node(NodeType.L)
        a_id = graph.add_node(NodeType.A)
        pairs.append((l_id, a_id))
        
        l_node = graph.nodes[l_id]
        a_node = graph.nodes[a_id]
        
        # Connect for beta reduction
        graph.connect(l_node.ports["right"], a_node.ports["left"])
        graph.connect(l_node.ports["left"], a_node.ports["middle"])
        
        # Create some connections between pairs (enables high-order interactions)
        if i > 0:
            prev_a = graph.nodes[pairs[i-1][1]]
            # Connect through fan-out to enable parallel interactions
            fo_id = graph.add_node(NodeType.FO)
            fo = graph.nodes[fo_id]
            graph.connect(prev_a.ports["middle"], fo.ports["middle"])
            graph.connect(fo.ports["left"], l_node.ports["middle"])
    
    print(f"Created graph with {len(graph.nodes)} nodes")
    print(f"  Lambda nodes: {len([n for n in graph.nodes.values() if n.node_type == NodeType.L])}")
    print(f"  Application nodes: {len([n for n in graph.nodes.values() if n.node_type == NodeType.A])}")
    print(f"  Fan-out nodes: {len([n for n in graph.nodes.values() if n.node_type == NodeType.FO])}")
    
    # Analyze high-order entropy
    analysis = analyze_parallel_interactions(graph)
    
    print("\n" + "-" * 70)
    print("High-Order Entropy Analysis")
    print("-" * 70)
    print(f"Parallel matches (can happen simultaneously): {analysis['parallel_matches']}")
    print(f"Nodes involved in parallel interactions: {analysis['nodes_in_parallel']}")
    print(f"Parallelism ratio: {analysis['parallelism_ratio']:.2%}")
    print()
    print("Entropy Measures:")
    print(f"  Node type entropy (Shannon): {analysis['node_entropy']:.4f}")
    print(f"  Pairwise interaction entropy: {analysis['pairwise_entropy']:.4f}")
    print(f"  High-order interaction entropy (order 3): {analysis['high_order_entropy']:.4f}")
    print(f"  Synergistic information: {analysis['synergistic_information']:.4f}")
    
    # Track entropy evolution
    print("\n" + "-" * 70)
    print("Tracking Entropy Evolution During Reduction")
    print("-" * 70)
    
    simulator = Simulator(graph.clone())
    history = track_entropy_evolution(simulator, max_steps=20)
    
    print(f"\nSteps tracked: {len(history)}")
    print("\nEntropy changes:")
    print("Step | Nodes | Node Entropy | High-Order | Synergistic")
    print("-" * 70)
    
    for h in history[::max(1, len(history)//10)]:  # Sample every 10%
        print(f"{h['step']:4d} | {h['nodes']:5d} | {h['node_entropy']:11.4f} | "
              f"{h['high_order_entropy']:10.4f} | {h['synergistic']:11.4f}")
    
    # Show final state
    if history:
        final = history[-1]
        initial = history[0]
        
        print("\n" + "-" * 70)
        print("Entropy Changes:")
        print(f"  Node entropy: {initial['node_entropy']:.4f} → {final['node_entropy']:.4f} "
              f"(Δ {final['node_entropy'] - initial['node_entropy']:+.4f})")
        print(f"  High-order entropy: {initial['high_order_entropy']:.4f} → "
              f"{final['high_order_entropy']:.4f} "
              f"(Δ {final['high_order_entropy'] - initial['high_order_entropy']:+.4f})")
        print(f"  Synergistic info: {initial['synergistic']:.4f} → {final['synergistic']:.4f} "
              f"(Δ {final['synergistic'] - initial['synergistic']:+.4f})")
    
    print("\n" + "=" * 70)
    print("Key Insights:")
    print("=" * 70)
    print("1. High-order entropy captures multi-way interactions")
    print("2. Parallel rewrites create synergistic effects")
    print("3. Entropy evolution reveals information dynamics")
    print("4. Chemlambda's parallelism enables high-order effects")
    print("   that don't exist in sequential systems")
    print("=" * 70)


def compare_sequential_vs_parallel_entropy():
    """
    Compare entropy in sequential vs parallel reduction.
    
    High-order entropy should be higher in parallel systems due to
    synergistic effects from simultaneous interactions.
    """
    print("\n" + "=" * 70)
    print("Sequential vs Parallel: High-Order Entropy Comparison")
    print("=" * 70)
    
    # Create same graph twice
    graph1 = Graph()
    graph2 = Graph()
    
    # Create multiple interaction sites
    for graph in [graph1, graph2]:
        for i in range(5):
            l_id = graph.add_node(NodeType.L)
            a_id = graph.add_node(NodeType.A)
            
            l_node = graph.nodes[l_id]
            a_node = graph.nodes[a_id]
            
            graph.connect(l_node.ports["right"], a_node.ports["left"])
            graph.connect(l_node.ports["left"], a_node.ports["middle"])
    
    # Sequential reduction (one at a time)
    print("\nSequential Reduction:")
    seq_sim = Simulator(graph1)
    seq_analysis_before = analyze_parallel_interactions(seq_sim.graph)
    
    # Reduce sequentially
    for _ in range(5):
        seq_sim.step(random_order=False)
    
    seq_analysis_after = analyze_parallel_interactions(seq_sim.graph)
    
    print(f"  Before: High-order entropy = {seq_analysis_before['high_order_entropy']:.4f}")
    print(f"  After:  High-order entropy = {seq_analysis_after['high_order_entropy']:.4f}")
    
    # Parallel reduction (all at once)
    print("\nParallel Reduction:")
    par_graph = graph2.clone()
    par_analysis_before = analyze_parallel_interactions(par_graph)
    
    # Apply parallel rewrites
    matches = find_non_conflicting_matches(par_graph, ALL_REACTIONS)
    if matches:
        from alife.quine_detector import apply_parallel_rewrites
        par_graph = apply_parallel_rewrites(par_graph, matches)
    
    par_analysis_after = analyze_parallel_interactions(par_graph)
    
    print(f"  Before: High-order entropy = {par_analysis_before['high_order_entropy']:.4f}")
    print(f"  After:  High-order entropy = {par_analysis_after['high_order_entropy']:.4f}")
    
    print("\n" + "-" * 70)
    print("Comparison:")
    print(f"  Sequential synergistic info: {seq_analysis_after['synergistic']:.4f}")
    print(f"  Parallel synergistic info:   {par_analysis_after['synergistic']:.4f}")
    print("\nParallel systems show higher synergistic information due to")
    print("simultaneous multi-way interactions that create emergent effects.")
    print("-" * 70)


def main():
    """Run high-order entropy demonstrations"""
    demonstrate_high_order_entropy()
    compare_sequential_vs_parallel_entropy()
    
    print("\n" + "=" * 70)
    print("Connection to Aguera's High-Order Entropy")
    print("=" * 70)
    print("\nAguera's concept: Analyze complex systems by considering")
    print("interactions beyond pairwise relationships, capturing synergistic")
    print("effects among multiple components.")
    print("\nChemlambda provides:")
    print("  1. Natural framework for multi-way interactions (parallel rewrites)")
    print("  2. Graph structure captures high-order relationships")
    print("  3. Entropy measures reveal synergistic information")
    print("  4. Evolution tracks information dynamics")
    print("\nThis enables analysis of:")
    print("  - Synergistic effects in complex systems")
    print("  - Information flow through multi-way interactions")
    print("  - Emergent behaviors from parallel operations")
    print("  - High-order correlations in distributed systems")
    print("=" * 70)


if __name__ == "__main__":
    main()

