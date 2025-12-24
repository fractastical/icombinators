"""
DIST Family Reactions (Distribution Moves)
Implements all distribution reactions for parallel reduction
"""

from typing import List, Tuple
from .graph import Graph, Node, NodeType, Port
from .reactions import Reaction


class DistReaction(Reaction):
    """Base class for DIST reactions"""
    
    def get_name(self):
        return "DIST"
    
    def can_apply(self, graph: Graph) -> List[Tuple]:
        """Find all DIST opportunities"""
        matches = []
        
        # FO-FOE Distribution: FO 1 2 c, FOE c 3 4 → FI j i 2, FO k i 3, FO l j 4, FOE 1 k l
        for fo_id, fo_node in graph.nodes.items():
            if fo_node.node_type != NodeType.FO:
                continue
            
            fo_middle_in = fo_node.ports.get("middle")
            fo_left_out = fo_node.ports.get("left")
            fo_right_out = fo_node.ports.get("right")
            
            if not all([fo_middle_in, fo_left_out, fo_right_out]):
                continue
            
            # Check if connected to FOE
            fo_middle_connected = graph.get_connected(fo_middle_in)
            if fo_middle_connected:
                foe_node = graph.nodes.get(fo_middle_connected.node_id)
                if foe_node and foe_node.node_type == NodeType.FOE:
                    matches.append(("FO_FOE", fo_id, fo_middle_connected.node_id))
        
        # FI-FO Distribution: FI 1 4 c, FO c 2 3 → FO 1 i j, FI i k 2, FI j l 3, FO 4 k l
        for fi_id, fi_node in graph.nodes.items():
            if fi_node.node_type != NodeType.FI:
                continue
            
            fi_left_in = fi_node.ports.get("left")
            fi_right_in = fi_node.ports.get("right")
            fi_middle_out = fi_node.ports.get("middle")
            
            if not all([fi_left_in, fi_right_in, fi_middle_out]):
                continue
            
            # Check if connected to FO
            fi_middle_connected = graph.get_connected(fi_middle_out)
            if fi_middle_connected:
                fo_node = graph.nodes.get(fi_middle_connected.node_id)
                if fo_node and fo_node.node_type == NodeType.FO:
                    matches.append(("FI_FO", fi_id, fi_middle_connected.node_id))
        
        # L-FO Distribution: L 1 2 c, FO c 3 4 → FI j i 2, L k i 3, L l j 4, FOE 1 k l
        for l_id, l_node in graph.nodes.items():
            if l_node.node_type != NodeType.L:
                continue
            
            l_middle_in = l_node.ports.get("middle")
            l_left_out = l_node.ports.get("left")
            l_right_out = l_node.ports.get("right")
            
            if not all([l_middle_in, l_left_out, l_right_out]):
                continue
            
            # Check if connected to FO
            l_right_connected = graph.get_connected(l_right_out)
            if l_right_connected:
                fo_node = graph.nodes.get(l_right_connected.node_id)
                if fo_node and fo_node.node_type == NodeType.FO:
                    matches.append(("L_FO", l_id, l_right_connected.node_id))
        
        # L-FOE Distribution: L 1 2 c, FOE c 3 4 → FI j i 2, L k i 3, L l j 4, FOE 1 k l
        for l_id, l_node in graph.nodes.items():
            if l_node.node_type != NodeType.L:
                continue
            
            l_middle_in = l_node.ports.get("middle")
            l_left_out = l_node.ports.get("left")
            l_right_out = l_node.ports.get("right")
            
            if not all([l_middle_in, l_left_out, l_right_out]):
                continue
            
            # Check if connected to FOE
            l_right_connected = graph.get_connected(l_right_out)
            if l_right_connected:
                foe_node = graph.nodes.get(l_right_connected.node_id)
                if foe_node and foe_node.node_type == NodeType.FOE:
                    matches.append(("L_FOE", l_id, l_right_connected.node_id))
        
        # A-FO Distribution: A 1 4 c, FO c 2 3 → FOE 1 i j, A i k 2, A j l 3, FOE 4 k l
        for a_id, a_node in graph.nodes.items():
            if a_node.node_type != NodeType.A:
                continue
            
            a_left_in = a_node.ports.get("left")
            a_right_in = a_node.ports.get("right")
            a_middle_out = a_node.ports.get("middle")
            
            if not all([a_left_in, a_right_in, a_middle_out]):
                continue
            
            # Check if connected to FO
            a_middle_connected = graph.get_connected(a_middle_out)
            if a_middle_connected:
                fo_node = graph.nodes.get(a_middle_connected.node_id)
                if fo_node and fo_node.node_type == NodeType.FO:
                    matches.append(("A_FO", a_id, a_middle_connected.node_id))
        
        # A-FOE Distribution: A 1 4 c, FOE c 2 3 → FOE 1 i j, A i k 2, A j l 3, FOE 4 k l
        for a_id, a_node in graph.nodes.items():
            if a_node.node_type != NodeType.A:
                continue
            
            a_left_in = a_node.ports.get("left")
            a_right_in = a_node.ports.get("right")
            a_middle_out = a_node.ports.get("middle")
            
            if not all([a_left_in, a_right_in, a_middle_out]):
                continue
            
            # Check if connected to FOE
            a_middle_connected = graph.get_connected(a_middle_out)
            if a_middle_connected:
                foe_node = graph.nodes.get(a_middle_connected.node_id)
                if foe_node and foe_node.node_type == NodeType.FOE:
                    matches.append(("A_FOE", a_id, a_middle_connected.node_id))
        
        return matches
    
    def apply(self, graph: Graph, match: Tuple) -> bool:
        """Apply DIST move"""
        dist_type = match[0]
        node1_id = match[1]
        node2_id = match[2]
        
        if node1_id not in graph.nodes or node2_id not in graph.nodes:
            return False
        
        node1 = graph.nodes[node1_id]
        node2 = graph.nodes[node2_id]
        
        if dist_type == "FO_FOE":
            return self._apply_fo_foe(graph, node1_id, node2_id)
        elif dist_type == "FI_FO":
            return self._apply_fi_fo(graph, node1_id, node2_id)
        elif dist_type == "L_FO":
            return self._apply_l_fo(graph, node1_id, node2_id)
        elif dist_type == "L_FOE":
            return self._apply_l_foe(graph, node1_id, node2_id)
        elif dist_type == "A_FO":
            return self._apply_a_fo(graph, node1_id, node2_id)
        elif dist_type == "A_FOE":
            return self._apply_a_foe(graph, node1_id, node2_id)
        
        return False
    
    def _apply_fo_foe(self, graph: Graph, fo_id: int, foe_id: int) -> bool:
        """FO-FOE Distribution: FO 1 2 c, FOE c 3 4 → FI j i 2, FO k i 3, FO l j 4, FOE 1 k l"""
        fo = graph.nodes[fo_id]
        foe = graph.nodes[foe_id]
        
        fo_middle_in = fo.ports.get("middle")
        fo_left_out = fo.ports.get("left")
        fo_right_out = fo.ports.get("right")
        foe_middle_in = foe.ports.get("middle")
        foe_left_out = foe.ports.get("left")
        foe_right_out = foe.ports.get("right")
        
        if not all([fo_middle_in, fo_left_out, fo_right_out, foe_middle_in, foe_left_out, foe_right_out]):
            return False
        
        # Check connection
        if graph.get_connected(fo_middle_in).node_id != foe_id:
            return False
        
        # Get connections
        fo_middle_connected = graph.get_connected(fo_middle_in)
        fo_left_connected = graph.get_connected(fo_left_out)
        fo_right_connected = graph.get_connected(fo_right_out)
        foe_left_connected = graph.get_connected(foe_left_out)
        foe_right_connected = graph.get_connected(foe_right_out)
        
        # Create new nodes: FI j i 2, FO k i 3, FO l j 4, FOE 1 k l
        fi_id = graph.add_node(NodeType.FI)
        fo1_id = graph.add_node(NodeType.FO)
        fo2_id = graph.add_node(NodeType.FO)
        foe_new_id = graph.add_node(NodeType.FOE)
        
        fi = graph.nodes[fi_id]
        fo1 = graph.nodes[fo1_id]
        fo2 = graph.nodes[fo2_id]
        foe_new = graph.nodes[foe_new_id]
        
        # Disconnect old connections
        graph.disconnect(fo_middle_in)
        graph.disconnect(fo_left_out)
        graph.disconnect(fo_right_out)
        graph.disconnect(foe_left_out)
        graph.disconnect(foe_right_out)
        
        # Connect FI j i 2 (FI connects to fo_right_out)
        if fo_right_connected:
            graph.connect(fo_right_connected, fi.ports["left"])
        graph.connect(fi.ports["right"], fo_right_connected if fo_right_connected else fo_right_out)
        
        # Connect FO k i 3 (FO1 connects FI to foe_left_out)
        graph.connect(fi.ports["middle"], fo1.ports["middle"])
        if foe_left_connected:
            graph.connect(fo1.ports["left"], foe_left_connected)
        graph.connect(fo1.ports["right"], foe_left_connected if foe_left_connected else foe_left_out)
        
        # Connect FO l j 4 (FO2 connects FI to foe_right_out)
        graph.connect(fi.ports["middle"], fo2.ports["middle"])
        if foe_right_connected:
            graph.connect(fo2.ports["left"], foe_right_connected)
        graph.connect(fo2.ports["right"], foe_right_connected if foe_right_connected else foe_right_out)
        
        # Connect FOE 1 k l (FOE connects fo_left_out to FO1 and FO2)
        if fo_left_connected:
            graph.connect(fo_left_connected, foe_new.ports["middle"])
        graph.connect(foe_new.ports["left"], fo1.ports["middle"])
        graph.connect(foe_new.ports["right"], fo2.ports["middle"])
        
        # Remove old nodes
        graph.remove_node(fo_id)
        graph.remove_node(foe_id)
        
        return True
    
    def _apply_fi_fo(self, graph: Graph, fi_id: int, fo_id: int) -> bool:
        """FI-FO Distribution: FI 1 4 c, FO c 2 3 → FO 1 i j, FI i k 2, FI j l 3, FO 4 k l"""
        fi = graph.nodes[fi_id]
        fo = graph.nodes[fo_id]
        
        fi_left_in = fi.ports.get("left")
        fi_right_in = fi.ports.get("right")
        fi_middle_out = fi.ports.get("middle")
        fo_middle_in = fo.ports.get("middle")
        fo_left_out = fo.ports.get("left")
        fo_right_out = fo.ports.get("right")
        
        if not all([fi_left_in, fi_right_in, fi_middle_out, fo_middle_in, fo_left_out, fo_right_out]):
            return False
        
        # Check connection
        if graph.get_connected(fi_middle_out).node_id != fo_id:
            return False
        
        # Get connections
        fi_left_connected = graph.get_connected(fi_left_in)
        fi_right_connected = graph.get_connected(fi_right_in)
        fo_left_connected = graph.get_connected(fo_left_out)
        fo_right_connected = graph.get_connected(fo_right_out)
        
        # Create new nodes: FO 1 i j, FI i k 2, FI j l 3, FO 4 k l
        fo1_id = graph.add_node(NodeType.FO)
        fi1_id = graph.add_node(NodeType.FI)
        fi2_id = graph.add_node(NodeType.FI)
        fo2_id = graph.add_node(NodeType.FO)
        
        fo1 = graph.nodes[fo1_id]
        fi1 = graph.nodes[fi1_id]
        fi2 = graph.nodes[fi2_id]
        fo2 = graph.nodes[fo2_id]
        
        # Disconnect old connections
        graph.disconnect(fi_left_in)
        graph.disconnect(fi_right_in)
        graph.disconnect(fi_middle_out)
        graph.disconnect(fo_left_out)
        graph.disconnect(fo_right_out)
        
        # Connect FO 1 i j (FO1 connects fi_left_in to FI1 and FI2)
        if fi_left_connected:
            graph.connect(fi_left_connected, fo1.ports["middle"])
        graph.connect(fo1.ports["left"], fi1.ports["left"])
        graph.connect(fo1.ports["right"], fi2.ports["left"])
        
        # Connect FI i k 2 (FI1 connects FO1 to fo_left_out)
        graph.connect(fi1.ports["right"], fo1.ports["middle"])
        if fo_left_connected:
            graph.connect(fi1.ports["middle"], fo_left_connected)
        graph.connect(fi1.ports["middle"], fo_left_connected if fo_left_connected else fo_left_out)
        
        # Connect FI j l 3 (FI2 connects FO1 to fo_right_out)
        graph.connect(fi2.ports["right"], fo1.ports["middle"])
        if fo_right_connected:
            graph.connect(fi2.ports["middle"], fo_right_connected)
        graph.connect(fi2.ports["middle"], fo_right_connected if fo_right_connected else fo_right_out)
        
        # Connect FO 4 k l (FO2 connects fi_right_in to FI1 and FI2)
        if fi_right_connected:
            graph.connect(fi_right_connected, fo2.ports["middle"])
        graph.connect(fo2.ports["left"], fi1.ports["right"])
        graph.connect(fo2.ports["right"], fi2.ports["right"])
        
        # Remove old nodes
        graph.remove_node(fi_id)
        graph.remove_node(fo_id)
        
        return True
    
    def _apply_l_fo(self, graph: Graph, l_id: int, fo_id: int) -> bool:
        """L-FO Distribution: L 1 2 c, FO c 3 4 → FI j i 2, L k i 3, L l j 4, FOE 1 k l"""
        l = graph.nodes[l_id]
        fo = graph.nodes[fo_id]
        
        l_middle_in = l.ports.get("middle")
        l_left_out = l.ports.get("left")
        l_right_out = l.ports.get("right")
        fo_middle_in = fo.ports.get("middle")
        fo_left_out = fo.ports.get("left")
        fo_right_out = fo.ports.get("right")
        
        if not all([l_middle_in, l_left_out, l_right_out, fo_middle_in, fo_left_out, fo_right_out]):
            return False
        
        # Check connection
        if graph.get_connected(l_right_out).node_id != fo_id:
            return False
        
        # Get connections
        l_middle_connected = graph.get_connected(l_middle_in)
        l_left_connected = graph.get_connected(l_left_out)
        fo_left_connected = graph.get_connected(fo_left_out)
        fo_right_connected = graph.get_connected(fo_right_out)
        
        # Create new nodes: FI j i 2, L k i 3, L l j 4, FOE 1 k l
        fi_id = graph.add_node(NodeType.FI)
        l1_id = graph.add_node(NodeType.L)
        l2_id = graph.add_node(NodeType.L)
        foe_id = graph.add_node(NodeType.FOE)
        
        fi = graph.nodes[fi_id]
        l1 = graph.nodes[l1_id]
        l2 = graph.nodes[l2_id]
        foe = graph.nodes[foe_id]
        
        # Disconnect old connections
        graph.disconnect(l_middle_in)
        graph.disconnect(l_left_out)
        graph.disconnect(l_right_out)
        graph.disconnect(fo_left_out)
        graph.disconnect(fo_right_out)
        
        # Connect FI j i 2 (FI connects l_left_out)
        if l_left_connected:
            graph.connect(l_left_connected, fi.ports["left"])
        graph.connect(fi.ports["right"], l_left_connected if l_left_connected else l_left_out)
        
        # Connect L k i 3 (L1 connects FI to fo_left_out)
        graph.connect(fi.ports["middle"], l1.ports["right"])
        if fo_left_connected:
            graph.connect(l1.ports["left"], fo_left_connected)
        graph.connect(l1.ports["middle"], fo_left_connected if fo_left_connected else fo_left_out)
        
        # Connect L l j 4 (L2 connects FI to fo_right_out)
        graph.connect(fi.ports["middle"], l2.ports["right"])
        if fo_right_connected:
            graph.connect(l2.ports["left"], fo_right_connected)
        graph.connect(l2.ports["middle"], fo_right_connected if fo_right_connected else fo_right_out)
        
        # Connect FOE 1 k l (FOE connects l_middle_in to L1 and L2)
        if l_middle_connected:
            graph.connect(l_middle_connected, foe.ports["middle"])
        graph.connect(foe.ports["left"], l1.ports["right"])
        graph.connect(foe.ports["right"], l2.ports["right"])
        
        # Remove old nodes
        graph.remove_node(l_id)
        graph.remove_node(fo_id)
        
        return True
    
    def _apply_l_foe(self, graph: Graph, l_id: int, foe_id: int) -> bool:
        """L-FOE Distribution: Same as L-FO but with FOE"""
        return self._apply_l_fo(graph, l_id, foe_id)
    
    def _apply_a_fo(self, graph: Graph, a_id: int, fo_id: int) -> bool:
        """A-FO Distribution: A 1 4 c, FO c 2 3 → FOE 1 i j, A i k 2, A j l 3, FOE 4 k l"""
        a = graph.nodes[a_id]
        fo = graph.nodes[fo_id]
        
        a_left_in = a.ports.get("left")
        a_right_in = a.ports.get("right")
        a_middle_out = a.ports.get("middle")
        fo_middle_in = fo.ports.get("middle")
        fo_left_out = fo.ports.get("left")
        fo_right_out = fo.ports.get("right")
        
        if not all([a_left_in, a_right_in, a_middle_out, fo_middle_in, fo_left_out, fo_right_out]):
            return False
        
        # Check connection
        if graph.get_connected(a_middle_out).node_id != fo_id:
            return False
        
        # Get connections
        a_left_connected = graph.get_connected(a_left_in)
        a_right_connected = graph.get_connected(a_right_in)
        fo_left_connected = graph.get_connected(fo_left_out)
        fo_right_connected = graph.get_connected(fo_right_out)
        
        # Create new nodes: FOE 1 i j, A i k 2, A j l 3, FOE 4 k l
        foe1_id = graph.add_node(NodeType.FOE)
        a1_id = graph.add_node(NodeType.A)
        a2_id = graph.add_node(NodeType.A)
        foe2_id = graph.add_node(NodeType.FOE)
        
        foe1 = graph.nodes[foe1_id]
        a1 = graph.nodes[a1_id]
        a2 = graph.nodes[a2_id]
        foe2 = graph.nodes[foe2_id]
        
        # Disconnect old connections
        graph.disconnect(a_left_in)
        graph.disconnect(a_right_in)
        graph.disconnect(a_middle_out)
        graph.disconnect(fo_left_out)
        graph.disconnect(fo_right_out)
        
        # Connect FOE 1 i j (FOE1 connects a_left_in to A1 and A2)
        if a_left_connected:
            graph.connect(a_left_connected, foe1.ports["middle"])
        graph.connect(foe1.ports["left"], a1.ports["left"])
        graph.connect(foe1.ports["right"], a2.ports["left"])
        
        # Connect A i k 2 (A1 connects FOE1 to fo_left_out)
        graph.connect(foe1.ports["middle"], a1.ports["left"])
        if fo_left_connected:
            graph.connect(a1.ports["middle"], fo_left_connected)
        graph.connect(a1.ports["right"], fo_left_connected if fo_left_connected else fo_left_out)
        
        # Connect A j l 3 (A2 connects FOE1 to fo_right_out)
        graph.connect(foe1.ports["middle"], a2.ports["left"])
        if fo_right_connected:
            graph.connect(a2.ports["middle"], fo_right_connected)
        graph.connect(a2.ports["right"], fo_right_connected if fo_right_connected else fo_right_out)
        
        # Connect FOE 4 k l (FOE2 connects a_right_in to A1 and A2)
        if a_right_connected:
            graph.connect(a_right_connected, foe2.ports["middle"])
        graph.connect(foe2.ports["left"], a1.ports["right"])
        graph.connect(foe2.ports["right"], a2.ports["right"])
        
        # Remove old nodes
        graph.remove_node(a_id)
        graph.remove_node(fo_id)
        
        return True
    
    def _apply_a_foe(self, graph: Graph, a_id: int, foe_id: int) -> bool:
        """A-FOE Distribution: Same as A-FO but with FOE"""
        return self._apply_a_fo(graph, a_id, foe_id)

