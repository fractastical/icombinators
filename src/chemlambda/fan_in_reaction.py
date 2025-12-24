"""
FAN-IN Reaction
FI 1 4 c, FOE c 2 3 → Arrow 1 3, Arrow 4 2
"""

from typing import List, Tuple
from .graph import Graph, Node, NodeType, Port
from .reactions import Reaction


class FanInReaction(Reaction):
    """FAN-IN move: FI 1 4 c, FOE c 2 3 → Arrow 1 3, Arrow 4 2"""
    
    def get_name(self):
        return "FAN-IN"
    
    def can_apply(self, graph: Graph) -> List[Tuple]:
        """Find all FI-FOE pairs connected through FI.middle.out and FOE.middle.in"""
        matches = []
        
        for fi_id, fi_node in graph.nodes.items():
            if fi_node.node_type != NodeType.FI:
                continue
            
            fi_middle_out = fi_node.ports.get("middle")
            if not fi_middle_out:
                continue
            
            connected = graph.get_connected(fi_middle_out)
            if not connected:
                continue
            
            foe_node = graph.nodes.get(connected.node_id)
            if not foe_node or foe_node.node_type != NodeType.FOE:
                continue
            
            foe_middle_in = foe_node.ports.get("middle")
            if connected != foe_middle_in:
                continue
            
            matches.append((fi_id, connected.node_id))
        
        return matches
    
    def apply(self, graph: Graph, match: Tuple) -> bool:
        """Apply FAN-IN move"""
        fi_id, foe_id = match
        
        if fi_id not in graph.nodes or foe_id not in graph.nodes:
            return False
        
        fi_node = graph.nodes[fi_id]
        foe_node = graph.nodes[foe_id]
        
        if fi_node.node_type != NodeType.FI or foe_node.node_type != NodeType.FOE:
            return False
        
        # Get ports
        fi_left_in = fi_node.ports.get("left")
        fi_right_in = fi_node.ports.get("right")
        fi_middle_out = fi_node.ports.get("middle")
        
        foe_middle_in = foe_node.ports.get("middle")
        foe_left_out = foe_node.ports.get("left")
        foe_right_out = foe_node.ports.get("right")
        
        if not all([fi_left_in, fi_right_in, fi_middle_out, foe_middle_in, foe_left_out, foe_right_out]):
            return False
        
        # Check connection
        if graph.get_connected(fi_middle_out) != foe_middle_in:
            return False
        
        # Disconnect FI-FOE connection
        graph.disconnect(fi_middle_out)
        
        # Create Arrow nodes
        arrow1_id = graph.add_node(NodeType.ARROW)
        arrow2_id = graph.add_node(NodeType.ARROW)
        
        arrow1 = graph.nodes[arrow1_id]
        arrow2 = graph.nodes[arrow2_id]
        
        # Connect Arrow 1: fi_left_in -> foe_right_out
        arrow1_in = arrow1.ports.get("middle")
        arrow1_out = arrow1.ports.get("middle_out")
        
        fi_left_connected = graph.get_connected(fi_left_in)
        foe_right_connected = graph.get_connected(foe_right_out)
        
        if fi_left_connected:
            graph.disconnect(fi_left_in)
            graph.connect(fi_left_connected, arrow1_in)
        graph.connect(arrow1_out, foe_right_connected if foe_right_connected else foe_right_out)
        
        # Connect Arrow 2: fi_right_in -> foe_left_out
        arrow2_in = arrow2.ports.get("middle")
        arrow2_out = arrow2.ports.get("middle_out")
        
        fi_right_connected = graph.get_connected(fi_right_in)
        foe_left_connected = graph.get_connected(foe_left_out)
        
        if fi_right_connected:
            graph.disconnect(fi_right_in)
            graph.connect(fi_right_connected, arrow2_in)
        graph.connect(arrow2_out, foe_left_connected if foe_left_connected else foe_left_out)
        
        # Remove FI and FOE nodes
        graph.remove_node(fi_id)
        graph.remove_node(foe_id)
        
        return True

