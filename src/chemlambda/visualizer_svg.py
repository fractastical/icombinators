"""
SVG Visualizer for chemlambda graphs
Creates visual representations similar to Buliga's original demos
"""

from typing import Dict, Tuple, Optional
import math
from .graph import Graph, Node, NodeType


class SVGVisualizer:
    """Creates SVG visualizations of chemlambda graphs"""
    
    def __init__(self, graph: Graph, width=800, height=600):
        self.graph = graph
        self.width = width
        self.height = height
        self.node_positions: Dict[int, Tuple[float, float]] = {}
        self._layout_graph()
    
    def _layout_graph(self):
        """Layout nodes in a circular/force-directed manner"""
        nodes = list(self.graph.nodes.keys())
        n = len(nodes)
        
        if n == 0:
            return
        
        # Center point
        center_x = self.width / 2
        center_y = self.height / 2
        
        # Radius for circular layout
        if n == 1:
            radius = 0
        else:
            radius = min(self.width, self.height) / 3
        
        # Place nodes in a circle
        for i, node_id in enumerate(nodes):
            angle = 2 * math.pi * i / n
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.node_positions[node_id] = (x, y)
    
    def _get_node_color(self, node_type: NodeType) -> str:
        """Get color for node type (matching Buliga's conventions)"""
        colors = {
            NodeType.L: "#4ec9b0",      # Cyan/teal for Lambda
            NodeType.A: "#ce9178",      # Orange/brown for Application
            NodeType.FI: "#569cd6",     # Blue for Fan-In
            NodeType.FO: "#dcdcaa",     # Yellow for Fan-Out
            NodeType.FOE: "#d7ba7d",    # Light yellow for Fan-Out-Extra
            NodeType.T: "#808080",      # Gray for Termination
            NodeType.ARROW: "#c586c0",  # Purple for Arrow
            NodeType.FRIN: "#9cdcfe",   # Light blue for Free In
            NodeType.FROUT: "#9cdcfe",  # Light blue for Free Out
        }
        return colors.get(node_type, "#ffffff")
    
    def _get_node_label(self, node_type: NodeType) -> str:
        """Get label for node type"""
        return node_type.value
    
    def to_svg(self) -> str:
        """Generate SVG representation of the graph"""
        svg_parts = [
            f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">',
            '<defs>',
            '<marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">',
            '<polygon points="0 0, 10 3, 0 6" fill="#888" />',
            '</marker>',
            '</defs>',
            '<rect width="100%" height="100%" fill="#1e1e1e"/>',
        ]
        
        # Draw edges first (so they appear behind nodes)
        for port1, port2 in self.graph.edges.items():
            if port1.node_id in self.node_positions and port2.node_id in self.node_positions:
                x1, y1 = self.node_positions[port1.node_id]
                x2, y2 = self.node_positions[port2.node_id]
                
                # Only draw each edge once
                if port1.node_id < port2.node_id:
                    svg_parts.append(
                        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                        f'stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>'
                    )
        
        # Draw nodes
        for node_id, (x, y) in self.node_positions.items():
            node = self.graph.nodes[node_id]
            color = self._get_node_color(node.node_type)
            label = self._get_node_label(node.node_type)
            
            # Node circle
            radius = 15
            svg_parts.append(
                f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" stroke="#fff" stroke-width="2"/>'
            )
            
            # Node label
            svg_parts.append(
                f'<text x="{x}" y="{y + 5}" text-anchor="middle" fill="#fff" font-size="10" font-family="monospace">{label}</text>'
            )
        
        svg_parts.append('</svg>')
        return '\n'.join(svg_parts)
    
    def save_svg(self, filename: str):
        """Save SVG to file"""
        with open(filename, 'w') as f:
            f.write(self.to_svg())


def visualize_graph(graph: Graph, width=800, height=600) -> str:
    """Convenience function to get SVG string"""
    viz = SVGVisualizer(graph, width, height)
    return viz.to_svg()

