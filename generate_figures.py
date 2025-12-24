#!/usr/bin/env python3
"""
Generate visualization figures for LaTeX document
Creates SVG/PNG images of chemlambda graphs using D3.js-style rendering
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chemlambda import Graph, NodeType, Simulator
from chemlambda.examples import (
    create_loop_example,
    create_ouroboros_like,
    create_quine_like_structure,
    create_chemical_reaction_network,
)

try:
    import cairosvg
    import svgwrite
    HAS_SVG = True
except ImportError:
    HAS_SVG = False
    print("Warning: cairosvg/svgwrite not available. Install with: pip install cairosvg svgwrite")

def create_svg_visualization(graph, filename, width=800, height=600):
    """Create SVG visualization of graph"""
    if not HAS_SVG:
        print(f"Skipping {filename} - SVG libraries not available")
        return False
    
    dwg = svgwrite.Drawing(filename, size=(f'{width}px', f'{height}px'))
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill='#000000'))
    
    # Node type colors (matching D3 demo)
    node_colors = {
        NodeType.L: '#4ec9b0',      # Cyan
        NodeType.A: '#ce9178',      # Orange
        NodeType.FI: '#569cd6',     # Blue
        NodeType.FO: '#dcdcaa',     # Yellow
        NodeType.FOE: '#d7ba7d',    # Light yellow
        NodeType.T: '#808080',      # Gray
        NodeType.ARROW: '#c586c0',  # Purple
        NodeType.FRIN: '#9cdcfe',   # Light blue
        NodeType.FROUT: '#9cdcfe',  # Light blue
    }
    
    # Layout nodes in a circle
    nodes = list(graph.nodes.values())
    n = len(nodes)
    center_x = width / 2
    center_y = height / 2
    radius = min(width, height) / 3 if n > 1 else 0
    
    node_positions = {}
    for i, node in enumerate(nodes):
        angle = 2 * 3.14159 * i / n if n > 0 else 0
        x = center_x + radius * (0.8 if n > 1 else 0) * (1 if n == 1 else (angle / 3.14159))
        y = center_y + radius * (0.8 if n > 1 else 0) * (1 if n == 1 else (angle / 3.14159))
        node_positions[node.node_id] = (x, y)
    
    # Draw edges
    drawn_edges = set()
    for port1, port2 in graph.edges.items():
        id1 = port1.node_id
        id2 = port2.node_id
        
        if id1 in node_positions and id2 in node_positions:
            edge_key = (min(id1, id2), max(id1, id2))
            if edge_key not in drawn_edges:
                drawn_edges.add(edge_key)
                x1, y1 = node_positions[id1]
                x2, y2 = node_positions[id2]
                
                dwg.add(dwg.line(
                    start=(x1, y1),
                    end=(x2, y2),
                    stroke='#666666',
                    stroke_width=2
                ))
    
    # Draw nodes
    for node_id, (x, y) in node_positions.items():
        node = graph.nodes[node_id]
        color = node_colors.get(node.node_type, '#ffffff')
        label = node.node_type.value
        
        # Draw circle
        dwg.add(dwg.circle(
            center=(x, y),
            r=15,
            fill=color,
            stroke='#ffffff',
            stroke_width=2
        ))
        
        # Draw label
        dwg.add(dwg.text(
            label,
            insert=(x, y + 5),
            fill='#ffffff',
            font_size='10px',
            font_family='monospace',
            text_anchor='middle'
        ))
    
    dwg.save()
    print(f"Created {filename}")
    return True

def generate_all_figures():
    """Generate all figures for the document"""
    figures_dir = "figures"
    os.makedirs(figures_dir, exist_ok=True)
    
    # Figure 1: Loop example
    print("Generating loop example...")
    loop_graph = create_loop_example()
    create_svg_visualization(loop_graph, f"{figures_dir}/loop_example.svg")
    
    # Figure 2: Ouroboros
    print("Generating ouroboros...")
    ouroboros_graph = create_ouroboros_like()
    create_svg_visualization(ouroboros_graph, f"{figures_dir}/ouroboros.svg")
    
    # Figure 3: Quine-like structure
    print("Generating quine-like structure...")
    quine_graph = create_quine_like_structure()
    create_svg_visualization(quine_graph, f"{figures_dir}/quine_structure.svg")
    
    # Figure 4: Chemical reaction network
    print("Generating chemical reaction network...")
    reaction_graph = create_chemical_reaction_network()
    create_svg_visualization(reaction_graph, f"{figures_dir}/reaction_network.svg")
    
    # Figure 5: Before/After BETA reduction
    print("Generating BETA reduction example...")
    # Simple lambda application: (λx.x) y
    beta_before = Graph()
    l_id = beta_before.add_node(NodeType.L)
    a_id = beta_before.add_node(NodeType.A)
    l_node = beta_before.nodes[l_id]
    a_node = beta_before.nodes[a_id]
    beta_before.connect(l_node.ports["right"], a_node.ports["left"])
    create_svg_visualization(beta_before, f"{figures_dir}/beta_before.svg")
    
    # After BETA
    simulator = Simulator(beta_before.clone())
    simulator.step()
    create_svg_visualization(simulator.graph, f"{figures_dir}/beta_after.svg")
    
    print(f"\nAll figures generated in {figures_dir}/")
    print("Convert SVG to PDF/PNG for LaTeX inclusion:")
    print("  - Use Inkscape: inkscape --export-pdf=file.pdf file.svg")
    print("  - Use cairosvg: cairosvg file.svg -o file.pdf")

if __name__ == "__main__":
    generate_all_figures()

