"""
Quine Detection for Artificial Life Research
Detects self-replicating graphs (quines) in chemlambda
"""

from typing import List, Set, Tuple, Optional
import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.chemlambda.graph import Graph
from src.chemlambda.simulator import Simulator
from src.chemlambda.reactions import Reaction


def find_non_conflicting_matches(graph: Graph, reactions: List[Reaction]) -> List[Tuple]:
    """
    Find all non-conflicting reaction matches.
    Two matches conflict if they share nodes or edges.
    """
    all_matches = []
    
    for reaction in reactions:
        matches = reaction.can_apply(graph)
        for match in matches:
            all_matches.append((reaction, match))
    
    # Find non-conflicting sets
    non_conflicting = []
    used_nodes = set()
    used_edges = set()
    
    for reaction, match in all_matches:
        # Get nodes involved in this match
        match_nodes = get_match_nodes(graph, reaction, match)
        match_edges = get_match_edges(graph, reaction, match)
        
        # Check for conflicts
        if not (match_nodes & used_nodes) and not (match_edges & used_edges):
            non_conflicting.append((reaction, match))
            used_nodes.update(match_nodes)
            used_edges.update(match_edges)
    
    return non_conflicting


def get_match_nodes(graph: Graph, reaction: Reaction, match: Tuple) -> Set[int]:
    """Get set of node IDs involved in a reaction match"""
    nodes = set()
    
    # Extract node IDs from match tuple
    # This depends on the reaction type
    if isinstance(match, tuple):
        for item in match:
            if isinstance(item, int) and item in graph.nodes:
                nodes.add(item)
    
    return nodes


def get_match_edges(graph: Graph, reaction: Reaction, match: Tuple) -> Set[Tuple]:
    """Get set of edges involved in a reaction match"""
    edges = set()
    nodes = get_match_nodes(graph, reaction, match)
    
    # Get edges connected to these nodes
    for node_id in nodes:
        node = graph.nodes[node_id]
        for port in node.ports.values():
            connected = graph.get_connected(port)
            if connected:
                edge = tuple(sorted([node_id, connected.node_id]))
                edges.add(edge)
    
    return edges


def apply_parallel_rewrites(graph: Graph, matches: List[Tuple]) -> Graph:
    """
    Apply multiple rewrites in parallel (non-conflicting matches).
    Returns a new graph with rewrites applied.
    """
    result = graph.clone()
    
    # Apply all matches
    for reaction, match in matches:
        reaction.apply(result, match)
    
    return result


def is_isomorphic(graph1: Graph, graph2: Graph) -> bool:
    """
    Check if two graphs are isomorphic.
    Simplified version - checks node types and connectivity patterns.
    """
    if len(graph1.nodes) != len(graph2.nodes):
        return False
    
    # Count node types
    types1 = {}
    types2 = {}
    
    for node in graph1.nodes.values():
        node_type = node.node_type
        types1[node_type] = types1.get(node_type, 0) + 1
    
    for node in graph2.nodes.values():
        node_type = node.node_type
        types2[node_type] = types2.get(node_type, 0) + 1
    
    if types1 != types2:
        return False
    
    # Check connectivity (simplified)
    edges1 = len(graph1.edges)
    edges2 = len(graph2.edges)
    
    if edges1 != edges2:
        return False
    
    # More sophisticated isomorphism checking would go here
    # For now, this is a basic check
    
    return True


def detect_quine(graph: Graph, simulator: Optional[Simulator] = None) -> bool:
    """
    Detect if a graph is a quine.
    
    A quine is a graph that, after applying all non-conflicting
    rewrites in parallel, produces a graph isomorphic to itself.
    """
    if simulator is None:
        from src.chemlambda.reactions import ALL_REACTIONS
        reactions = ALL_REACTIONS
    else:
        reactions = simulator.reactions
    
    # Find all non-conflicting matches
    matches = find_non_conflicting_matches(graph, reactions)
    
    if not matches:
        return False  # No reactions possible
    
    # Apply parallel rewrites
    result = apply_parallel_rewrites(graph, matches)
    
    # Check if isomorphic
    return is_isomorphic(graph, result)


def measure_replication_rate(graph: Graph, steps: int = 100) -> float:
    """
    Measure replication rate of a quine.
    Returns average number of quine copies produced per step.
    """
    if not detect_quine(graph):
        return 0.0  # Not a quine
    
    simulator = Simulator(graph.clone())
    initial_quines = count_quine_copies(simulator.graph)
    
    total_replicated = 0
    
    for step in range(steps):
        applied = simulator.step(random_order=True)
        if applied:
            current_quines = count_quine_copies(simulator.graph)
            replicated = current_quines - initial_quines
            total_replicated += max(0, replicated)
            initial_quines = current_quines
    
    return total_replicated / steps if steps > 0 else 0.0


def count_quine_copies(graph: Graph) -> int:
    """
    Count how many quine copies are in a graph.
    This is a simplified version - would need proper quine detection.
    """
    # For now, count connected components that might be quines
    # This is a placeholder - proper implementation needed
    return 1  # Simplified


def find_quines_in_graph(graph: Graph) -> List[Graph]:
    """
    Find all quine subgraphs in a larger graph.
    Returns list of quine graphs.
    """
    quines = []
    
    # Find connected components
    components = find_connected_components(graph)
    
    # Check each component
    for component in components:
        if detect_quine(component):
            quines.append(component)
    
    return quines


def find_connected_components(graph: Graph) -> List[Graph]:
    """
    Find all connected components in a graph.
    Returns list of subgraphs, each a connected component.
    """
    # Simplified implementation
    # Proper implementation would use graph traversal
    return [graph]  # Placeholder


class QuineAnalyzer:
    """Analyzer for quine properties"""
    
    def __init__(self, graph: Graph):
        self.graph = graph
        self.is_quine = detect_quine(graph)
    
    def analyze(self) -> dict:
        """Analyze quine properties"""
        if not self.is_quine:
            return {"is_quine": False}
        
        return {
            "is_quine": True,
            "size": len(self.graph.nodes),
            "replication_rate": measure_replication_rate(self.graph),
            "node_types": self._count_node_types(),
            "connectivity": self._measure_connectivity(),
        }
    
    def _count_node_types(self) -> dict:
        """Count node types in graph"""
        counts = {}
        for node in self.graph.nodes.values():
            node_type = node.node_type.value
            counts[node_type] = counts.get(node_type, 0) + 1
        return counts
    
    def _measure_connectivity(self) -> float:
        """Measure graph connectivity"""
        n = len(self.graph.nodes)
        if n == 0:
            return 0.0
        e = len(self.graph.edges) // 2  # Undirected edges
        max_edges = n * (n - 1) / 2
        return e / max_edges if max_edges > 0 else 0.0

