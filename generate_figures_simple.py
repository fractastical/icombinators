#!/usr/bin/env python3
"""
Simple SVG figure generator for LaTeX document
Generates SVG files without external dependencies
"""

import sys
import os
import math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chemlambda import Graph, NodeType, Simulator
from chemlambda.examples import (
    create_loop_example,
    create_ouroboros_like,
    create_quine_like_structure,
    create_chemical_reaction_network,
)

def create_svg(graph, filename, width=600, height=400):
    """Create SVG file directly"""
    nodes = list(graph.nodes.values())
    n = len(nodes)
    
    # Node colors
    colors = {
        'L': '#4ec9b0', 'A': '#ce9178', 'FI': '#569cd6',
        'FO': '#dcdcaa', 'FOE': '#d7ba7d', 'T': '#808080',
        'Arrow': '#c586c0', 'FRIN': '#9cdcfe', 'FROUT': '#9cdcfe'
    }
    
    # Layout
    center_x = width / 2
    center_y = height / 2
    radius = min(width, height) / 3 if n > 1 else 0
    
    node_positions = {}
    for i, node in enumerate(nodes):
        if n == 1:
            x, y = center_x, center_y
        else:
            angle = 2 * math.pi * i / n
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
        node_positions[node.node_id] = (x, y)
    
    # Generate SVG
    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        f'<rect width="{width}" height="{height}" fill="#000000"/>',
    ]
    
    # Draw edges
    drawn_edges = set()
    for port1, port2 in graph.edges.items():
        id1 = port1.node_id
        id2 = port2.node_id
        edge_key = (min(id1, id2), max(id1, id2))
        
        if edge_key not in drawn_edges and id1 in node_positions and id2 in node_positions:
            drawn_edges.add(edge_key)
            x1, y1 = node_positions[id1]
            x2, y2 = node_positions[id2]
            svg_lines.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#666666" stroke-width="2"/>')
    
    # Draw nodes
    for node_id, (x, y) in node_positions.items():
        node = graph.nodes[node_id]
        color = colors.get(node.node_type.value, '#ffffff')
        label = node.node_type.value
        
        svg_lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="{color}" stroke="#ffffff" stroke-width="2"/>')
        svg_lines.append(f'<text x="{x:.1f}" y="{y + 5:.1f}" fill="#ffffff" font-size="10" font-family="monospace" text-anchor="middle">{label}</text>')
    
    svg_lines.append('</svg>')
    
    with open(filename, 'w') as f:
        f.write('\n'.join(svg_lines))
    
    print(f"Created {filename}")

def generate_all():
    """Generate all figures"""
    os.makedirs("figures", exist_ok=True)
    
    print("Generating loop example...")
    create_svg(create_loop_example(), "figures/loop_example.svg")
    
    print("Generating ouroboros...")
    create_svg(create_ouroboros_like(), "figures/ouroboros.svg")
    
    print("Generating quine-like structure...")
    create_svg(create_quine_like_structure(), "figures/quine_structure.svg")
    
    print("Generating chemical reaction network...")
    create_svg(create_chemical_reaction_network(), "figures/reaction_network.svg")
    
    print("Generating BETA reduction...")
    beta_before = Graph()
    l_id = beta_before.add_node(NodeType.L)
    a_id = beta_before.add_node(NodeType.A)
    l_node = beta_before.nodes[l_id]
    a_node = beta_before.nodes[a_id]
    beta_before.connect(l_node.ports["right"], a_node.ports["left"])
    create_svg(beta_before, "figures/beta_before.svg")
    
    simulator = Simulator(beta_before.clone())
    simulator.step()
    create_svg(simulator.graph, "figures/beta_after.svg")
    
    print("\nAll SVG figures created in figures/")
    print("To convert to PDF for LaTeX:")
    print("  - Use Inkscape: inkscape --export-pdf=file.pdf file.svg")
    print("  - Or include SVG directly in LaTeX with \\includesvg (requires svg package)")

if __name__ == "__main__":
    generate_all()

