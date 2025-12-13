"""
Chemlambda Reaction Implementations
Implements all the graph rewriting reactions (moves)
"""

from typing import List, Tuple, Optional
from .graph import Graph, Node, NodeType, Port


class Reaction:
    """Base class for reactions"""
    
    def can_apply(self, graph: Graph) -> List[Tuple]:
        """Check if reaction can be applied, returns list of matches"""
        raise NotImplementedError
    
    def apply(self, graph: Graph, match: Tuple) -> bool:
        """Apply the reaction given a match, returns True if successful"""
        raise NotImplementedError
    
    def get_name(self) -> str:
        """Get the name of this reaction"""
        raise NotImplementedError


class BetaReaction(Reaction):
    """BETA move: L 1 2 c, A c 4 3 → Arrow 1 3, Arrow 4 2"""
    
    def get_name(self):
        return "BETA"
    
    def can_apply(self, graph: Graph) -> List[Tuple]:
        """Find all L-A pairs connected through L.right.out and A.left.in"""
        matches = []
        
        for l_id, l_node in graph.nodes.items():
            if l_node.node_type != NodeType.L:
                continue
            
            l_right_out = l_node.ports.get("right")
            if not l_right_out:
                continue
            
            connected = graph.get_connected(l_right_out)
            if not connected:
                continue
            
            a_node = graph.nodes.get(connected.node_id)
            if not a_node or a_node.node_type != NodeType.A:
                continue
            
            a_left_in = a_node.ports.get("left")
            if connected != a_left_in:
                continue
            
            matches.append((l_id, connected.node_id))
        
        return matches
    
    def apply(self, graph: Graph, match: Tuple) -> bool:
        """Apply BETA move"""
        l_id, a_id = match
        
        if l_id not in graph.nodes or a_id not in graph.nodes:
            return False
        
        l_node = graph.nodes[l_id]
        a_node = graph.nodes[a_id]
        
        if l_node.node_type != NodeType.L or a_node.node_type != NodeType.A:
            return False
        
        # Get ports
        l_middle_in = l_node.ports.get("middle")
        l_left_out = l_node.ports.get("left")
        l_right_out = l_node.ports.get("right")
        
        a_left_in = a_node.ports.get("left")
        a_right_in = a_node.ports.get("right")
        a_middle_out = a_node.ports.get("middle")
        
        if not all([l_middle_in, l_left_out, l_right_out, a_left_in, a_right_in, a_middle_out]):
            return False
        
        # Check connection
        if graph.get_connected(l_right_out) != a_left_in:
            return False
        
        # Disconnect L-A connection
        graph.disconnect(l_right_out)
        
        # Create Arrow nodes
        arrow1_id = graph.add_node(NodeType.ARROW)
        arrow2_id = graph.add_node(NodeType.ARROW)
        
        arrow1 = graph.nodes[arrow1_id]
        arrow2 = graph.nodes[arrow2_id]
        
        # Connect Arrow 1: l_middle_in -> a_middle_out
        arrow1_in = arrow1.ports.get("middle")
        arrow1_out = arrow1.ports.get("middle_out")
        
        l_middle_connected = graph.get_connected(l_middle_in)
        a_middle_connected = graph.get_connected(a_middle_out)
        
        if l_middle_connected:
            graph.disconnect(l_middle_in)
            graph.connect(l_middle_connected, arrow1_in)
        graph.connect(arrow1_out, a_middle_connected if a_middle_connected else a_middle_out)
        
        # Connect Arrow 2: a_right_in -> l_left_out
        arrow2_in = arrow2.ports.get("middle")
        arrow2_out = arrow2.ports.get("middle_out")
        
        a_right_connected = graph.get_connected(a_right_in)
        l_left_connected = graph.get_connected(l_left_out)
        
        if a_right_connected:
            graph.disconnect(a_right_in)
            graph.connect(a_right_connected, arrow2_in)
        graph.connect(arrow2_out, l_left_connected if l_left_connected else l_left_out)
        
        # Remove L and A nodes
        graph.remove_node(l_id)
        graph.remove_node(a_id)
        
        return True


class CombReaction(Reaction):
    """COMB move: M 1, Arrow 1 2 → M 2"""
    
    def get_name(self):
        return "COMB"
    
    def can_apply(self, graph: Graph) -> List[Tuple]:
        """Find all Arrow nodes that can be eliminated"""
        matches = []
        
        for arrow_id, arrow_node in graph.nodes.items():
            if arrow_node.node_type != NodeType.ARROW:
                continue
            
            arrow_in = arrow_node.ports.get("middle")
            arrow_out = arrow_node.ports.get("middle_out")
            
            if not arrow_in or not arrow_out:
                continue
            
            connected_in = graph.get_connected(arrow_in)
            connected_out = graph.get_connected(arrow_out)
            
            # Can eliminate if both ends are connected (not forming a cycle with another Arrow)
            if connected_in and connected_out:
                # Don't eliminate if it would create a cycle with another Arrow
                if (connected_in.node_id != arrow_id and 
                    connected_out.node_id != arrow_id):
                    matches.append((arrow_id,))
        
        return matches
    
    def apply(self, graph: Graph, match: Tuple) -> bool:
        """Apply COMB move - eliminate Arrow node"""
        arrow_id = match[0]
        
        if arrow_id not in graph.nodes:
            return False
        
        arrow_node = graph.nodes[arrow_id]
        if arrow_node.node_type != NodeType.ARROW:
            return False
        
        arrow_in = arrow_node.ports.get("middle")
        arrow_out = arrow_node.ports.get("middle_out")
        
        if not arrow_in or not arrow_out:
            return False
        
        connected_in = graph.get_connected(arrow_in)
        connected_out = graph.get_connected(arrow_out)
        
        if not connected_in or not connected_out:
            return False
        
        # Don't create self-loops
        if connected_in.node_id == connected_out.node_id:
            return False
        
        # Connect the two ports directly
        graph.disconnect(arrow_in)
        graph.disconnect(arrow_out)
        graph.connect(connected_in, connected_out)
        
        # Remove Arrow node
        graph.remove_node(arrow_id)
        
        return True


class PruningReaction(Reaction):
    """PRUNING moves: Various pruning operations"""
    
    def get_name(self):
        return "PRUNING"
    
    def can_apply(self, graph: Graph) -> List[Tuple]:
        """Find all pruning opportunities"""
        matches = []
        
        # A-T or FI-T pruning: A 1 2 3, T 3 → T 1, T 2
        for node_id, node in graph.nodes.items():
            if node.node_type in [NodeType.A, NodeType.FI]:
                middle_out = node.ports.get("middle")
                if middle_out:
                    connected = graph.get_connected(middle_out)
                    if connected:
                        t_node = graph.nodes.get(connected.node_id)
                        if t_node and t_node.node_type == NodeType.T:
                            matches.append(("A_FI_T", node_id, connected.node_id))
        
        # L-T pruning: L 1 2 3, T 3 → T 1, T c, FRIN c
        for node_id, node in graph.nodes.items():
            if node.node_type == NodeType.L:
                right_out = node.ports.get("right")
                if right_out:
                    connected = graph.get_connected(right_out)
                    if connected:
                        t_node = graph.nodes.get(connected.node_id)
                        if t_node and t_node.node_type == NodeType.T:
                            matches.append(("L_T", node_id, connected.node_id))
        
        # FO-T pruning: FO 1 2 3, T 2 → Arrow 1 3
        for node_id, node in graph.nodes.items():
            if node.node_type in [NodeType.FO, NodeType.FOE]:
                left_out = node.ports.get("left")
                right_out = node.ports.get("right")
                if left_out:
                    connected = graph.get_connected(left_out)
                    if connected:
                        t_node = graph.nodes.get(connected.node_id)
                        if t_node and t_node.node_type == NodeType.T:
                            matches.append(("FO_T_left", node_id, connected.node_id))
                if right_out:
                    connected = graph.get_connected(right_out)
                    if connected:
                        t_node = graph.nodes.get(connected.node_id)
                        if t_node and t_node.node_type == NodeType.T:
                            matches.append(("FO_T_right", node_id, connected.node_id))
        
        return matches
    
    def apply(self, graph: Graph, match: Tuple) -> bool:
        """Apply pruning move"""
        prune_type = match[0]
        node_id = match[1]
        t_id = match[2]
        
        if node_id not in graph.nodes or t_id not in graph.nodes:
            return False
        
        node = graph.nodes[node_id]
        t_node = graph.nodes[t_id]
        
        if prune_type == "A_FI_T":
            # A 1 2 3, T 3 → T 1, T 2
            left_in = node.ports.get("left")
            right_in = node.ports.get("right")
            middle_out = node.ports.get("middle")
            
            if not all([left_in, right_in, middle_out]):
                return False
            
            # Create two T nodes
            t1_id = graph.add_node(NodeType.T)
            t2_id = graph.add_node(NodeType.T)
            
            t1 = graph.nodes[t1_id]
            t2 = graph.nodes[t2_id]
            
            # Connect T nodes to inputs
            left_connected = graph.get_connected(left_in)
            right_connected = graph.get_connected(right_in)
            
            if left_connected:
                graph.disconnect(left_in)
                graph.connect(left_connected, t1.ports["middle"])
            if right_connected:
                graph.disconnect(right_in)
                graph.connect(right_connected, t2.ports["middle"])
            
            # Remove original nodes
            graph.remove_node(node_id)
            graph.remove_node(t_id)
            
            return True
        
        elif prune_type == "L_T":
            # L 1 2 3, T 3 → T 1, T c, FRIN c
            middle_in = node.ports.get("middle")
            left_out = node.ports.get("left")
            right_out = node.ports.get("right")
            
            if not all([middle_in, left_out, right_out]):
                return False
            
            # Create T and FRIN nodes
            t1_id = graph.add_node(NodeType.T)
            t2_id = graph.add_node(NodeType.T)
            frin_id = graph.add_node(NodeType.FRIN)
            
            t1 = graph.nodes[t1_id]
            t2 = graph.nodes[t2_id]
            frin = graph.nodes[frin_id]
            
            # Connect T to middle input
            middle_connected = graph.get_connected(middle_in)
            if middle_connected:
                graph.disconnect(middle_in)
                graph.connect(middle_connected, t1.ports["middle"])
            
            # Connect T and FRIN to left output (bound variable)
            left_connected = graph.get_connected(left_out)
            if left_connected:
                graph.disconnect(left_out)
                graph.connect(left_connected, t2.ports["middle"])
                graph.connect(frin.ports["middle"], t2.ports["middle"])
            
            # Remove original nodes
            graph.remove_node(node_id)
            graph.remove_node(t_id)
            
            return True
        
        elif prune_type.startswith("FO_T"):
            # FO 1 2 3, T 2 → Arrow 1 3
            middle_in = node.ports.get("middle")
            left_out = node.ports.get("left")
            right_out = node.ports.get("right")
            
            if not all([middle_in, left_out, right_out]):
                return False
            
            # Determine which output is terminated
            if prune_type == "FO_T_left":
                unused_out = left_out
                used_out = right_out
            else:
                unused_out = right_out
                used_out = left_out
            
            # Create Arrow node
            arrow_id = graph.add_node(NodeType.ARROW)
            arrow = graph.nodes[arrow_id]
            
            # Connect middle_in to used_out through Arrow
            middle_connected = graph.get_connected(middle_in)
            used_connected = graph.get_connected(used_out)
            
            graph.disconnect(middle_in)
            graph.disconnect(used_out)
            
            if middle_connected:
                graph.connect(middle_connected, arrow.ports["middle"])
            if used_connected:
                graph.connect(arrow.ports["middle_out"], used_connected)
            
            # Remove original nodes
            graph.remove_node(node_id)
            graph.remove_node(t_id)
            
            return True
        
        return False


# Export all reactions
ALL_REACTIONS = [
    BetaReaction(),
    CombReaction(),
    PruningReaction(),
]

