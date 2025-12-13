"""
Chemlambda Graph Structure
Implements the graph representation for chemlambda molecules
"""

from typing import Dict, List, Set, Tuple, Optional
from enum import Enum
from dataclasses import dataclass


class NodeType(Enum):
    """Node types in chemlambda"""
    L = "L"      # Lambda
    A = "A"      # Application
    FI = "FI"    # Fan-In
    FO = "FO"    # Fan-Out
    FOE = "FOE"  # Fan-Out-Extra
    T = "T"      # Termination
    ARROW = "Arrow"  # Arrow connector
    FRIN = "FRIN"    # Free input
    FROUT = "FROUT"  # Free output


@dataclass
class Port:
    """Represents a port on a node"""
    node_id: int
    port_type: str  # "middle", "left", "right"
    direction: str  # "in" or "out"
    
    def __hash__(self):
        return hash((self.node_id, self.port_type, self.direction))
    
    def __eq__(self, other):
        return (self.node_id == other.node_id and 
                self.port_type == other.port_type and
                self.direction == other.direction)


@dataclass
class Node:
    """Represents a node in the graph"""
    node_id: int
    node_type: NodeType
    ports: Dict[str, Port]  # port_type -> Port
    
    def __init__(self, node_id: int, node_type: NodeType):
        self.node_id = node_id
        self.node_type = node_type
        self.ports = {}
        self._init_ports()
    
    def _init_ports(self):
        """Initialize ports based on node type"""
        if self.node_type == NodeType.L:
            self.ports["middle"] = Port(self.node_id, "middle", "in")
            self.ports["left"] = Port(self.node_id, "left", "out")
            self.ports["right"] = Port(self.node_id, "right", "out")
        elif self.node_type == NodeType.A:
            self.ports["left"] = Port(self.node_id, "left", "in")
            self.ports["right"] = Port(self.node_id, "right", "in")
            self.ports["middle"] = Port(self.node_id, "middle", "out")
        elif self.node_type == NodeType.FI:
            self.ports["left"] = Port(self.node_id, "left", "in")
            self.ports["right"] = Port(self.node_id, "right", "in")
            self.ports["middle"] = Port(self.node_id, "middle", "out")
        elif self.node_type == NodeType.FO:
            self.ports["middle"] = Port(self.node_id, "middle", "in")
            self.ports["left"] = Port(self.node_id, "left", "out")
            self.ports["right"] = Port(self.node_id, "right", "out")
        elif self.node_type == NodeType.FOE:
            self.ports["middle"] = Port(self.node_id, "middle", "in")
            self.ports["left"] = Port(self.node_id, "left", "out")
            self.ports["right"] = Port(self.node_id, "right", "out")
        elif self.node_type == NodeType.T:
            self.ports["middle"] = Port(self.node_id, "middle", "in")
        elif self.node_type == NodeType.ARROW:
            self.ports["middle"] = Port(self.node_id, "middle", "in")
            self.ports["middle_out"] = Port(self.node_id, "middle", "out")
        elif self.node_type == NodeType.FRIN:
            self.ports["middle"] = Port(self.node_id, "middle", "out")
        elif self.node_type == NodeType.FROUT:
            self.ports["middle"] = Port(self.node_id, "middle", "in")


class Graph:
    """Represents a chemlambda graph"""
    
    def __init__(self):
        self.nodes: Dict[int, Node] = {}
        self.edges: Dict[Port, Port] = {}  # Maps port -> connected port
        self.next_node_id = 0
    
    def add_node(self, node_type: NodeType) -> int:
        """Add a node to the graph, returns node_id"""
        node_id = self.next_node_id
        self.next_node_id += 1
        self.nodes[node_id] = Node(node_id, node_type)
        return node_id
    
    def connect(self, port1: Port, port2: Port):
        """Connect two ports"""
        self.edges[port1] = port2
        self.edges[port2] = port1
    
    def disconnect(self, port: Port):
        """Disconnect a port"""
        if port in self.edges:
            other = self.edges[port]
            del self.edges[port]
            if other in self.edges:
                del self.edges[other]
    
    def get_connected(self, port: Port) -> Optional[Port]:
        """Get the port connected to this port"""
        return self.edges.get(port)
    
    def remove_node(self, node_id: int):
        """Remove a node and all its connections"""
        if node_id not in self.nodes:
            return
        
        node = self.nodes[node_id]
        # Disconnect all ports
        for port in node.ports.values():
            self.disconnect(port)
        
        del self.nodes[node_id]
    
    def clone(self) -> 'Graph':
        """Create a deep copy of the graph"""
        new_graph = Graph()
        new_graph.next_node_id = self.next_node_id
        
        # Copy nodes
        for node_id, node in self.nodes.items():
            new_graph.nodes[node_id] = Node(node_id, node.node_type)
        
        # Copy edges
        for port1, port2 in self.edges.items():
            if port1.node_id in new_graph.nodes and port2.node_id in new_graph.nodes:
                node1 = new_graph.nodes[port1.node_id]
                node2 = new_graph.nodes[port2.node_id]
                port1_new = node1.ports[port1.port_type]
                port2_new = node2.ports[port2.port_type]
                new_graph.connect(port1_new, port2_new)
        
        return new_graph
    
    def to_mol_format(self) -> str:
        """Convert graph to .mol file format"""
        lines = []
        for node_id, node in sorted(self.nodes.items()):
            ports = []
            if node.node_type == NodeType.L:
                ports = ["middle.in", "left.out", "right.out"]
            elif node.node_type == NodeType.A:
                ports = ["left.in", "right.in", "middle.out"]
            elif node.node_type == NodeType.FI:
                ports = ["left.in", "right.in", "middle.out"]
            elif node.node_type == NodeType.FO:
                ports = ["middle.in", "left.out", "right.out"]
            elif node.node_type == NodeType.FOE:
                ports = ["middle.in", "left.out", "right.out"]
            elif node.node_type == NodeType.T:
                ports = ["middle.in"]
            elif node.node_type == NodeType.ARROW:
                ports = ["middle.in", "middle.out"]
            
            # Find connections
            port_vars = {}
            for port_name in ports:
                port = node.ports.get(port_name.split(".")[0])
                if port:
                    connected = self.get_connected(port)
                    if connected:
                        # Use connected node's ID as variable name
                        port_vars[port_name] = f"n{connected.node_id}"
                    else:
                        port_vars[port_name] = f"p{node_id}_{port_name}"
            
            # Format line
            if node.node_type == NodeType.L:
                line = f"L {port_vars.get('middle.in', '?')} {port_vars.get('left.out', '?')} {port_vars.get('right.out', '?')}"
            elif node.node_type == NodeType.A:
                line = f"A {port_vars.get('left.in', '?')} {port_vars.get('right.in', '?')} {port_vars.get('middle.out', '?')}"
            elif node.node_type == NodeType.FI:
                line = f"FI {port_vars.get('left.in', '?')} {port_vars.get('right.in', '?')} {port_vars.get('middle.out', '?')}"
            elif node.node_type == NodeType.FO:
                line = f"FO {port_vars.get('middle.in', '?')} {port_vars.get('left.out', '?')} {port_vars.get('right.out', '?')}"
            elif node.node_type == NodeType.FOE:
                line = f"FOE {port_vars.get('middle.in', '?')} {port_vars.get('left.out', '?')} {port_vars.get('right.out', '?')}"
            elif node.node_type == NodeType.T:
                line = f"T {port_vars.get('middle.in', '?')}"
            elif node.node_type == NodeType.ARROW:
                line = f"Arrow {port_vars.get('middle.in', '?')} {port_vars.get('middle.out', '?')}"
            else:
                continue
            
            lines.append(line)
        
        return "\n".join(lines)
    
    def __repr__(self):
        return f"Graph({len(self.nodes)} nodes, {len(self.edges)//2} edges)"

