"""
Chemlambda Simulator
Runs graph rewriting simulations
"""

import random
from typing import List, Optional, Callable
from .graph import Graph, NodeType
from .reactions import Reaction, ALL_REACTIONS


class Simulator:
    """Simulates chemlambda graph rewriting"""
    
    def __init__(self, graph: Graph, reactions: Optional[List[Reaction]] = None):
        self.graph = graph
        self.reactions = reactions or ALL_REACTIONS
        self.step_count = 0
        self.history: List[Graph] = []
        self.reaction_history: List[tuple] = []  # (step, reaction_name, match)
    
    def step(self, random_order: bool = True) -> bool:
        """
        Perform one step of reduction
        Returns True if a reaction was applied, False otherwise
        """
        # Find all possible reactions
        all_matches = []
        
        for reaction in self.reactions:
            matches = reaction.can_apply(self.graph)
            for match in matches:
                all_matches.append((reaction, match))
        
        if not all_matches:
            return False
        
        # Select a match
        if random_order:
            reaction, match = random.choice(all_matches)
        else:
            # Priority order: BETA/FAN-IN > DIST > PRUNING > COMB
            priority_order = ["BETA", "FAN-IN", "DIST", "PRUNING", "COMB"]
            sorted_matches = sorted(all_matches, 
                                  key=lambda x: priority_order.index(x[0].get_name()) 
                                  if x[0].get_name() in priority_order else 999)
            reaction, match = sorted_matches[0]
        
        # Save current state
        self.history.append(self.graph.clone())
        
        # Apply reaction
        success = reaction.apply(self.graph, match)
        
        if success:
            self.step_count += 1
            self.reaction_history.append((self.step_count, reaction.get_name(), match))
            
            # Apply COMB cycle after other reactions
            if reaction.get_name() != "COMB":
                self._comb_cycle()
        
        return success
    
    def _comb_cycle(self):
        """Apply COMB moves until no more can be applied"""
        comb_reaction = None
        for r in self.reactions:
            if r.get_name() == "COMB":
                comb_reaction = r
                break
        
        if not comb_reaction:
            return
        
        max_comb_iterations = 100  # Prevent infinite loops
        iterations = 0
        
        while iterations < max_comb_iterations:
            matches = comb_reaction.can_apply(self.graph)
            if not matches:
                break
            
            match = matches[0]
            success = comb_reaction.apply(self.graph, match)
            if not success:
                break
            
            iterations += 1
    
    def run(self, max_steps: int = 1000, random_order: bool = True) -> int:
        """
        Run simulation until no more reactions can be applied or max_steps reached
        Returns number of steps taken
        """
        steps = 0
        while steps < max_steps:
            if not self.step(random_order):
                break
            steps += 1
        return steps
    
    def get_stats(self) -> dict:
        """Get statistics about the simulation"""
        reaction_counts = {}
        for _, reaction_name, _ in self.reaction_history:
            reaction_counts[reaction_name] = reaction_counts.get(reaction_name, 0) + 1
        
        return {
            "total_steps": self.step_count,
            "reaction_counts": reaction_counts,
            "final_nodes": len(self.graph.nodes),
            "final_edges": len(self.graph.edges) // 2,
        }


def create_identity_function() -> Graph:
    """Create graph for λx.x (identity function)"""
    graph = Graph()
    
    # L node for lambda
    l_id = graph.add_node(NodeType.L)
    l_node = graph.nodes[l_id]
    
    # A node for application (will be applied to argument)
    a_id = graph.add_node(NodeType.A)
    a_node = graph.nodes[a_id]
    
    # Connect L.right.out to A.left.in (beta reduction connection)
    graph.connect(l_node.ports["right"], a_node.ports["left"])
    
    # Connect L.left.out to A.middle.out (lambda body to result)
    graph.connect(l_node.ports["left"], a_node.ports["middle"])
    
    return graph


def create_simple_application() -> Graph:
    """Create graph for (λx.x) y"""
    graph = Graph()
    
    # Lambda: L
    l_id = graph.add_node(NodeType.L)
    l_node = graph.nodes[l_id]
    
    # Application: A (for applying lambda)
    a1_id = graph.add_node(NodeType.A)
    a1_node = graph.nodes[a1_id]
    
    # Argument: A (represents 'y')
    a2_id = graph.add_node(NodeType.A)
    a2_node = graph.nodes[a2_id]
    
    # Connect L to A1 (lambda application)
    graph.connect(l_node.ports["right"], a1_node.ports["left"])
    
    # Connect A2 (argument) to A1.right.in
    graph.connect(a2_node.ports["middle"], a1_node.ports["right"])
    
    # Connect L.left.out to A1.middle.out (lambda body)
    graph.connect(l_node.ports["left"], a1_node.ports["middle"])
    
    return graph

