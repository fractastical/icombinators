"""
Simple ASCII visualizer for chemlambda graphs
"""

from typing import Dict, Set
from .graph import Graph, Node, NodeType


class GraphVisualizer:
    """Simple ASCII visualization of graphs"""
    
    def __init__(self, graph: Graph):
        self.graph = graph
        self.node_positions: Dict[int, tuple] = {}
        self._layout_nodes()
    
    def _layout_nodes(self):
        """Simple layout algorithm - place nodes in a grid"""
        nodes = list(self.graph.nodes.keys())
        import math
        cols = int(math.ceil(math.sqrt(len(nodes))))
        
        for i, node_id in enumerate(nodes):
            row = i // cols
            col = i % cols
            self.node_positions[node_id] = (row, col)
    
    def visualize(self) -> str:
        """Create ASCII visualization"""
        lines = []
        lines.append("=" * 60)
        lines.append(f"Graph Visualization: {len(self.graph.nodes)} nodes, "
                    f"{len(self.graph.edges) // 2} edges")
        lines.append("=" * 60)
        lines.append("")
        
        # Node information
        lines.append("Nodes:")
        for node_id, node in sorted(self.graph.nodes.items()):
            node_type = node.node_type.value
            lines.append(f"  {node_id}: {node_type}")
            
            # Show connections
            connections = []
            for port_name, port in node.ports.items():
                connected = self.graph.get_connected(port)
                if connected:
                    connections.append(f"{port_name} -> node {connected.node_id}")
            
            if connections:
                for conn in connections:
                    lines.append(f"    {conn}")
        
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def visualize_step(self, step: int, reaction_name: str) -> str:
        """Visualize a single step"""
        lines = []
        lines.append(f"Step {step}: {reaction_name}")
        lines.append("-" * 60)
        lines.append(self.visualize())
        return "\n".join(lines)


def print_graph(graph: Graph, title: str = "Graph"):
    """Convenience function to print a graph"""
    viz = GraphVisualizer(graph)
    print(f"\n{title}:")
    print(viz.visualize())

