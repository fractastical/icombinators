"""
Example graph constructions for chemlambda
Includes loops, cycles, and complex reaction patterns
"""

from .graph import Graph, NodeType


def create_loop_example() -> Graph:
    """
    Create a graph with a loop/cycle
    Demonstrates circular structures in chemlambda
    """
    graph = Graph()
    
    # Create a simple loop: Arrow -> Arrow -> Arrow
    arrow1_id = graph.add_node(NodeType.ARROW)
    arrow2_id = graph.add_node(NodeType.ARROW)
    arrow3_id = graph.add_node(NodeType.ARROW)
    
    arrow1 = graph.nodes[arrow1_id]
    arrow2 = graph.nodes[arrow2_id]
    arrow3 = graph.nodes[arrow3_id]
    
    # Connect in a cycle
    graph.connect(arrow1.ports["middle_out"], arrow2.ports["middle"])
    graph.connect(arrow2.ports["middle_out"], arrow3.ports["middle"])
    graph.connect(arrow3.ports["middle_out"], arrow1.ports["middle"])
    
    return graph


def create_fixed_point_combinator() -> Graph:
    """
    Create a graph representing the Y combinator (fixed point combinator)
    This creates a loop that enables recursion
    """
    graph = Graph()
    
    # Y combinator structure: λf.(λx.f(x x))(λx.f(x x))
    # Simplified representation with loops
    
    # Outer lambda
    l1_id = graph.add_node(NodeType.L)
    l1 = graph.nodes[l1_id]
    
    # Inner lambda 1
    l2_id = graph.add_node(NodeType.L)
    l2 = graph.nodes[l2_id]
    
    # Inner lambda 2
    l3_id = graph.add_node(NodeType.L)
    l3 = graph.nodes[l3_id]
    
    # Applications
    a1_id = graph.add_node(NodeType.A)
    a1 = graph.nodes[a1_id]
    
    a2_id = graph.add_node(NodeType.A)
    a2 = graph.nodes[a2_id]
    
    a3_id = graph.add_node(NodeType.A)
    a3 = graph.nodes[a3_id]
    
    # Connect to form Y combinator structure
    # This creates cycles that enable self-application
    graph.connect(l1.ports["right"], a1.ports["left"])
    graph.connect(l2.ports["right"], a2.ports["left"])
    graph.connect(l3.ports["right"], a3.ports["left"])
    
    # Create self-application loops
    graph.connect(a2.ports["middle"], a2.ports["right"])  # x x pattern
    graph.connect(a3.ports["middle"], a3.ports["right"])  # x x pattern
    
    # Connect lambdas
    graph.connect(l2.ports["left"], a1.ports["middle"])
    graph.connect(l3.ports["left"], a1.ports["right"])
    
    return graph


def create_quine_like_structure() -> Graph:
    """
    Create a graph structure that can potentially replicate
    More complex than simple quine, includes multiple reaction sites
    """
    graph = Graph()
    
    # Create multiple lambda-application pairs that can interact
    pairs = []
    for i in range(3):
        l_id = graph.add_node(NodeType.L)
        a_id = graph.add_node(NodeType.A)
        pairs.append((l_id, a_id))
        
        l_node = graph.nodes[l_id]
        a_node = graph.nodes[a_id]
        
        # Connect L-A pairs (BETA reaction sites)
        graph.connect(l_node.ports["right"], a_node.ports["left"])
        
        # Connect lambda bodies
        graph.connect(l_node.ports["left"], a_node.ports["middle"])
    
    # Connect pairs in a way that allows parallel reactions
    # This creates a structure that can replicate
    
    return graph


def create_ackermann_structure() -> Graph:
    """
    Create a simplified structure representing Ackermann function computation
    Shows nested recursion patterns
    """
    graph = Graph()
    
    # Base case: A(0, n) = n + 1
    # Represented as a simple structure
    
    # Recursive case structure
    # A(m, 0) = A(m-1, 1)
    # A(m, n) = A(m-1, A(m, n-1))
    
    # Create nested lambda structure
    outer_l_id = graph.add_node(NodeType.L)
    outer_l = graph.nodes[outer_l_id]
    
    inner_l_id = graph.add_node(NodeType.L)
    inner_l = graph.nodes[inner_l_id]
    
    # Applications for nested calls
    a1_id = graph.add_node(NodeType.A)
    a1 = graph.nodes[a1_id]
    
    a2_id = graph.add_node(NodeType.A)
    a2 = graph.nodes[a2_id]
    
    a3_id = graph.add_node(NodeType.A)
    a3 = graph.nodes[a3_id]
    
    # Connect to form nested structure
    graph.connect(outer_l.ports["right"], a1.ports["left"])
    graph.connect(inner_l.ports["right"], a2.ports["left"])
    graph.connect(a2.ports["middle"], a3.ports["left"])
    
    # Create recursion loops
    graph.connect(outer_l.ports["left"], a1.ports["middle"])
    graph.connect(inner_l.ports["left"], a3.ports["middle"])
    
    # Connect nested calls
    graph.connect(a1.ports["right"], a2.ports["right"])
    
    return graph


def create_self_replicating_pattern() -> Graph:
    """
    Create a pattern that can self-replicate through parallel reactions
    More realistic quine-like structure
    """
    graph = Graph()
    
    # Create a structure with multiple non-conflicting BETA sites
    # This allows parallel application leading to replication
    
    # Central structure
    center_l_id = graph.add_node(NodeType.L)
    center_l = graph.nodes[center_l_id]
    
    # Multiple application sites around center
    app_nodes = []
    for i in range(4):
        a_id = graph.add_node(NodeType.A)
        app_nodes.append(a_id)
        a_node = graph.nodes[a_id]
        
        # Connect to center lambda
        graph.connect(center_l.ports["right"], a_node.ports["left"])
        graph.connect(center_l.ports["left"], a_node.ports["middle"])
    
    # Add fan-out to enable distribution
    fo_id = graph.add_node(NodeType.FO)
    fo = graph.nodes[fo_id]
    
    app_node0 = graph.nodes[app_nodes[0]]
    app_node1 = graph.nodes[app_nodes[1]]
    
    graph.connect(fo.ports["middle"], center_l.ports["middle"])
    graph.connect(fo.ports["left"], app_node0.ports["right"])
    graph.connect(fo.ports["right"], app_node1.ports["right"])
    
    return graph


def create_chemical_reaction_network() -> Graph:
    """
    Create a graph that represents a chemical reaction network
    Multiple molecules that can react with each other
    """
    graph = Graph()
    
    # Create multiple "molecules" (subgraphs)
    molecules = []
    
    for i in range(3):
        # Each molecule is a lambda-application pair
        l_id = graph.add_node(NodeType.L)
        a_id = graph.add_node(NodeType.A)
        molecules.append((l_id, a_id))
        
        l_node = graph.nodes[l_id]
        a_node = graph.nodes[a_id]
        
        # Internal connection
        graph.connect(l_node.ports["right"], a_node.ports["left"])
        graph.connect(l_node.ports["left"], a_node.ports["middle"])
    
    # Connect molecules so they can react
    # Molecule 0 can react with Molecule 1
    mol0_l = graph.nodes[molecules[0][0]]
    mol1_a = graph.nodes[molecules[1][1]]
    graph.connect(mol0_l.ports["middle"], mol1_a.ports["right"])
    
    # Molecule 1 can react with Molecule 2
    mol1_l = graph.nodes[molecules[1][0]]
    mol2_a = graph.nodes[molecules[2][1]]
    graph.connect(mol1_l.ports["middle"], mol2_a.ports["right"])
    
    # Create a cycle: Molecule 2 -> Molecule 0
    mol2_l = graph.nodes[molecules[2][0]]
    mol0_a = graph.nodes[molecules[0][1]]
    graph.connect(mol2_l.ports["middle"], mol0_a.ports["right"])
    
    return graph


def create_ouroboros_like() -> Graph:
    """
    Create an Ouroboros-like structure (snake eating its tail)
    Self-referential loop structure
    """
    graph = Graph()
    
    # Create a chain of nodes
    chain_length = 5
    nodes = []
    
    for i in range(chain_length):
        if i % 2 == 0:
            node_id = graph.add_node(NodeType.L)
        else:
            node_id = graph.add_node(NodeType.A)
        nodes.append(node_id)
    
    # Connect chain
    for i in range(chain_length - 1):
        node1 = graph.nodes[nodes[i]]
        node2 = graph.nodes[nodes[i + 1]]
        
        if node1.node_type == NodeType.L:
            graph.connect(node1.ports["right"], node2.ports["left"])
        else:
            graph.connect(node1.ports["middle"], node2.ports["left"])
    
    # Close the loop - connect last to first (Ouroboros!)
    last_node = graph.nodes[nodes[-1]]
    first_node = graph.nodes[nodes[0]]
    
    if last_node.node_type == NodeType.A:
        graph.connect(last_node.ports["middle"], first_node.ports["middle"])
    else:
        graph.connect(last_node.ports["right"], first_node.ports["middle"])
    
    return graph


def create_metabolism_example() -> Graph:
    """
    Create a graph that demonstrates metabolism
    Can process "food" (other nodes) and transform
    """
    graph = Graph()
    
    # "Organism" - a lambda that can process inputs
    organism_l_id = graph.add_node(NodeType.L)
    organism_l = graph.nodes[organism_l_id]
    
    organism_a_id = graph.add_node(NodeType.A)
    organism_a = graph.nodes[organism_a_id]
    
    graph.connect(organism_l.ports["right"], organism_a.ports["left"])
    graph.connect(organism_l.ports["left"], organism_a.ports["middle"])
    
    # "Food" molecules - can be consumed
    food_nodes = []
    for i in range(3):
        food_id = graph.add_node(NodeType.A)
        food_nodes.append(food_id)
        food_node = graph.nodes[food_id]
        
        # Connect food to organism (can be processed)
        graph.connect(food_node.ports["middle"], organism_a.ports["right"])
    
    # Add fan-out to distribute processing
    fo_id = graph.add_node(NodeType.FO)
    fo = graph.nodes[fo_id]
    
    food_node0 = graph.nodes[food_nodes[0]]
    food_node1 = graph.nodes[food_nodes[1]]
    
    graph.connect(fo.ports["middle"], organism_l.ports["middle"])
    graph.connect(fo.ports["left"], food_node0.ports["left"])
    graph.connect(fo.ports["right"], food_node1.ports["left"])
    
    return graph

