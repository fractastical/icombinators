/**
 * Example graph constructions for chemlambda (JavaScript)
 * Includes loops, cycles, and complex reaction patterns
 */

const { Graph, NodeType } = require('./graph.js');

function createLoopExample() {
    const graph = new Graph();
    
    // Create a simple loop: Arrow -> Arrow -> Arrow
    const arrow1Id = graph.addNode(NodeType.ARROW);
    const arrow2Id = graph.addNode(NodeType.ARROW);
    const arrow3Id = graph.addNode(NodeType.ARROW);
    
    const arrow1 = graph.nodes[arrow1Id];
    const arrow2 = graph.nodes[arrow2Id];
    const arrow3 = graph.nodes[arrow3Id];
    
    // Connect in a cycle
    graph.connect(arrow1.ports.middle_out, arrow2.ports.middle);
    graph.connect(arrow2.ports.middle_out, arrow3.ports.middle);
    graph.connect(arrow3.ports.middle_out, arrow1.ports.middle);
    
    return graph;
}

function createFixedPointCombinator() {
    const graph = new Graph();
    
    // Y combinator structure with loops
    const l1Id = graph.addNode(NodeType.L);
    const l1 = graph.nodes[l1Id];
    
    const l2Id = graph.addNode(NodeType.L);
    const l2 = graph.nodes[l2Id];
    
    const l3Id = graph.addNode(NodeType.L);
    const l3 = graph.nodes[l3Id];
    
    const a1Id = graph.addNode(NodeType.A);
    const a1 = graph.nodes[a1Id];
    
    const a2Id = graph.addNode(NodeType.A);
    const a2 = graph.nodes[a2Id];
    
    const a3Id = graph.addNode(NodeType.A);
    const a3 = graph.nodes[a3Id];
    
    graph.connect(l1.ports.right, a1.ports.left);
    graph.connect(l2.ports.right, a2.ports.left);
    graph.connect(l3.ports.right, a3.ports.left);
    
    // Create self-application loops
    graph.connect(a2.ports.middle, a2.ports.right);
    graph.connect(a3.ports.middle, a3.ports.right);
    
    graph.connect(l2.ports.left, a1.ports.middle);
    graph.connect(l3.ports.left, a1.ports.right);
    
    return graph;
}

function createQuineLikeStructure() {
    const graph = new Graph();
    
    // Create multiple lambda-application pairs
    const pairs = [];
    for (let i = 0; i < 3; i++) {
        const lId = graph.addNode(NodeType.L);
        const aId = graph.addNode(NodeType.A);
        pairs.push([lId, aId]);
        
        const lNode = graph.nodes[lId];
        const aNode = graph.nodes[aId];
        
        graph.connect(lNode.ports.right, aNode.ports.left);
        graph.connect(lNode.ports.left, aNode.ports.middle);
    }
    
    return graph;
}

function createChemicalReactionNetwork() {
    const graph = new Graph();
    
    // Create multiple "molecules"
    const molecules = [];
    
    for (let i = 0; i < 3; i++) {
        const lId = graph.addNode(NodeType.L);
        const aId = graph.addNode(NodeType.A);
        molecules.push([lId, aId]);
        
        const lNode = graph.nodes[lId];
        const aNode = graph.nodes[aId];
        
        graph.connect(lNode.ports.right, aNode.ports.left);
        graph.connect(lNode.ports.left, aNode.ports.middle);
    }
    
    // Connect molecules so they can react
    const mol0L = graph.nodes[molecules[0][0]];
    const mol1A = graph.nodes[molecules[1][1]];
    graph.connect(mol0L.ports.middle, mol1A.ports.right);
    
    const mol1L = graph.nodes[molecules[1][0]];
    const mol2A = graph.nodes[molecules[2][1]];
    graph.connect(mol1L.ports.middle, mol2A.ports.right);
    
    // Create a cycle
    const mol2L = graph.nodes[molecules[2][0]];
    const mol0A = graph.nodes[molecules[0][1]];
    graph.connect(mol2L.ports.middle, mol0A.ports.right);
    
    return graph;
}

function createOuroborosLike() {
    const graph = new Graph();
    
    // Create a chain of nodes
    const chainLength = 5;
    const nodes = [];
    
    for (let i = 0; i < chainLength; i++) {
        const nodeId = (i % 2 === 0) 
            ? graph.addNode(NodeType.L)
            : graph.addNode(NodeType.A);
        nodes.push(nodeId);
    }
    
    // Connect chain
    for (let i = 0; i < chainLength - 1; i++) {
        const node1 = graph.nodes[nodes[i]];
        const node2 = graph.nodes[nodes[i + 1]];
        
        if (node1.nodeType === NodeType.L) {
            graph.connect(node1.ports.right, node2.ports.left);
        } else {
            graph.connect(node1.ports.middle, node2.ports.left);
        }
    }
    
    // Close the loop (Ouroboros!)
    const lastNode = graph.nodes[nodes[nodes.length - 1]];
    const firstNode = graph.nodes[nodes[0]];
    
    if (lastNode.nodeType === NodeType.A) {
        graph.connect(lastNode.ports.middle, firstNode.ports.middle);
    } else {
        graph.connect(lastNode.ports.right, firstNode.ports.middle);
    }
    
    return graph;
}

function createMetabolismExample() {
    const graph = new Graph();
    
    // "Organism" - can process inputs
    const organismLId = graph.addNode(NodeType.L);
    const organismL = graph.nodes[organismLId];
    
    const organismAId = graph.addNode(NodeType.A);
    const organismA = graph.nodes[organismAId];
    
    graph.connect(organismL.ports.right, organismA.ports.left);
    graph.connect(organismL.ports.left, organismA.ports.middle);
    
    // "Food" molecules
    const foodNodes = [];
    for (let i = 0; i < 3; i++) {
        const foodId = graph.addNode(NodeType.A);
        foodNodes.push(foodId);
        const foodNode = graph.nodes[foodId];
        graph.connect(foodNode.ports.middle, organismA.ports.right);
    }
    
    // Fan-out for distribution
    const foId = graph.addNode(NodeType.FO);
    const fo = graph.nodes[foId];
    
    graph.connect(fo.ports.middle, organismL.ports.middle);
    graph.connect(fo.ports.left, graph.nodes[foodNodes[0]].ports.left);
    graph.connect(fo.ports.right, graph.nodes[foodNodes[1]].ports.left);
    
    return graph;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        createLoopExample,
        createFixedPointCombinator,
        createQuineLikeStructure,
        createChemicalReactionNetwork,
        createOuroborosLike,
        createMetabolismExample,
    };
}

