/**
 * Chemlambda Reaction Implementations (JavaScript)
 * Implements all the graph rewriting reactions (moves)
 */

const { Graph, NodeType } = require('./graph.js');

class Reaction {
    canApply(graph) {
        throw new Error('Not implemented');
    }
    
    apply(graph, match) {
        throw new Error('Not implemented');
    }
    
    getName() {
        throw new Error('Not implemented');
    }
}

class BetaReaction extends Reaction {
    getName() {
        return 'BETA';
    }
    
    canApply(graph) {
        const matches = [];
        
        Object.values(graph.nodes).forEach(lNode => {
            if (lNode.nodeType !== NodeType.L) return;
            
            const lRightOut = lNode.ports.right;
            if (!lRightOut) return;
            
            const connected = graph.getConnected(lRightOut);
            if (!connected) return;
            
            const aNode = graph.nodes[connected.nodeId];
            if (!aNode || aNode.nodeType !== NodeType.A) return;
            
            const aLeftIn = aNode.ports.left;
            if (connected.equals(aLeftIn)) {
                matches.push([lNode.nodeId, aNode.nodeId]);
            }
        });
        
        return matches;
    }
    
    apply(graph, match) {
        const [lId, aId] = match;
        
        if (!graph.nodes[lId] || !graph.nodes[aId]) {
            return false;
        }
        
        const lNode = graph.nodes[lId];
        const aNode = graph.nodes[aId];
        
        if (lNode.nodeType !== NodeType.L || aNode.nodeType !== NodeType.A) {
            return false;
        }
        
        const lMiddleIn = lNode.ports.middle;
        const lLeftOut = lNode.ports.left;
        const lRightOut = lNode.ports.right;
        
        const aLeftIn = aNode.ports.left;
        const aRightIn = aNode.ports.right;
        const aMiddleOut = aNode.ports.middle;
        
        if (!lMiddleIn || !lLeftOut || !lRightOut || 
            !aLeftIn || !aRightIn || !aMiddleOut) {
            return false;
        }
        
        // Check connection
        if (!graph.getConnected(lRightOut).equals(aLeftIn)) {
            return false;
        }
        
        // Disconnect L-A connection
        graph.disconnect(lRightOut);
        
        // Create Arrow nodes
        const arrow1Id = graph.addNode(NodeType.ARROW);
        const arrow2Id = graph.addNode(NodeType.ARROW);
        
        const arrow1 = graph.nodes[arrow1Id];
        const arrow2 = graph.nodes[arrow2Id];
        
        const arrow1In = arrow1.ports.middle;
        const arrow1Out = arrow1.ports.middle_out;
        const arrow2In = arrow2.ports.middle;
        const arrow2Out = arrow2.ports.middle_out;
        
        // Connect Arrow 1: l_middle_in -> a_middle_out
        const lMiddleConnected = graph.getConnected(lMiddleIn);
        const aMiddleConnected = graph.getConnected(aMiddleOut);
        
        if (lMiddleConnected) {
            graph.disconnect(lMiddleIn);
            graph.connect(lMiddleConnected, arrow1In);
        }
        if (aMiddleConnected) {
            graph.disconnect(aMiddleOut);
            graph.connect(arrow1Out, aMiddleConnected);
        } else {
            graph.connect(arrow1Out, aMiddleOut);
        }
        
        // Connect Arrow 2: a_right_in -> l_left_out
        const aRightConnected = graph.getConnected(aRightIn);
        const lLeftConnected = graph.getConnected(lLeftOut);
        
        if (aRightConnected) {
            graph.disconnect(aRightIn);
            graph.connect(aRightConnected, arrow2In);
        }
        if (lLeftConnected) {
            graph.disconnect(lLeftOut);
            graph.connect(arrow2Out, lLeftConnected);
        } else {
            graph.connect(arrow2Out, lLeftOut);
        }
        
        // Remove L and A nodes
        graph.removeNode(lId);
        graph.removeNode(aId);
        
        return true;
    }
}

class CombReaction extends Reaction {
    getName() {
        return 'COMB';
    }
    
    canApply(graph) {
        const matches = [];
        
        Object.values(graph.nodes).forEach(arrowNode => {
            if (arrowNode.nodeType !== NodeType.ARROW) return;
            
            const arrowIn = arrowNode.ports.middle;
            const arrowOut = arrowNode.ports.middle_out;
            
            if (!arrowIn || !arrowOut) return;
            
            const connectedIn = graph.getConnected(arrowIn);
            const connectedOut = graph.getConnected(arrowOut);
            
            if (connectedIn && connectedOut) {
                // Don't eliminate if it would create a cycle with another Arrow
                if (connectedIn.nodeId !== arrowNode.nodeId && 
                    connectedOut.nodeId !== arrowNode.nodeId) {
                    matches.push([arrowNode.nodeId]);
                }
            }
        });
        
        return matches;
    }
    
    apply(graph, match) {
        const [arrowId] = match;
        
        if (!graph.nodes[arrowId]) return false;
        
        const arrowNode = graph.nodes[arrowId];
        if (arrowNode.nodeType !== NodeType.ARROW) return false;
        
        const arrowIn = arrowNode.ports.middle;
        const arrowOut = arrowNode.ports.middle_out;
        
        if (!arrowIn || !arrowOut) return false;
        
        const connectedIn = graph.getConnected(arrowIn);
        const connectedOut = graph.getConnected(arrowOut);
        
        if (!connectedIn || !connectedOut) return false;
        
        // Don't create self-loops
        if (connectedIn.nodeId === connectedOut.nodeId) return false;
        
        // Connect the two ports directly
        graph.disconnect(arrowIn);
        graph.disconnect(arrowOut);
        graph.connect(connectedIn, connectedOut);
        
        // Remove Arrow node
        graph.removeNode(arrowId);
        
        return true;
    }
}

class PruningReaction extends Reaction {
    getName() {
        return 'PRUNING';
    }
    
    canApply(graph) {
        const matches = [];
        
        // A-T or FI-T pruning
        Object.values(graph.nodes).forEach(node => {
            if (node.nodeType === NodeType.A || node.nodeType === NodeType.FI) {
                const middleOut = node.ports.middle;
                if (middleOut) {
                    const connected = graph.getConnected(middleOut);
                    if (connected) {
                        const tNode = graph.nodes[connected.nodeId];
                        if (tNode && tNode.nodeType === NodeType.T) {
                            matches.push(['A_FI_T', node.nodeId, connected.nodeId]);
                        }
                    }
                }
            }
        });
        
        // L-T pruning
        Object.values(graph.nodes).forEach(node => {
            if (node.nodeType === NodeType.L) {
                const rightOut = node.ports.right;
                if (rightOut) {
                    const connected = graph.getConnected(rightOut);
                    if (connected) {
                        const tNode = graph.nodes[connected.nodeId];
                        if (tNode && tNode.nodeType === NodeType.T) {
                            matches.push(['L_T', node.nodeId, connected.nodeId]);
                        }
                    }
                }
            }
        });
        
        // FO-T pruning
        Object.values(graph.nodes).forEach(node => {
            if (node.nodeType === NodeType.FO || node.nodeType === NodeType.FOE) {
                const leftOut = node.ports.left;
                const rightOut = node.ports.right;
                
                if (leftOut) {
                    const connected = graph.getConnected(leftOut);
                    if (connected) {
                        const tNode = graph.nodes[connected.nodeId];
                        if (tNode && tNode.nodeType === NodeType.T) {
                            matches.push(['FO_T_left', node.nodeId, connected.nodeId]);
                        }
                    }
                }
                
                if (rightOut) {
                    const connected = graph.getConnected(rightOut);
                    if (connected) {
                        const tNode = graph.nodes[connected.nodeId];
                        if (tNode && tNode.nodeType === NodeType.T) {
                            matches.push(['FO_T_right', node.nodeId, connected.nodeId]);
                        }
                    }
                }
            }
        });
        
        return matches;
    }
    
    apply(graph, match) {
        const [pruneType, nodeId, tId] = match;
        
        if (!graph.nodes[nodeId] || !graph.nodes[tId]) {
            return false;
        }
        
        const node = graph.nodes[nodeId];
        const tNode = graph.nodes[tId];
        
        if (pruneType === 'A_FI_T') {
            const leftIn = node.ports.left;
            const rightIn = node.ports.right;
            const middleOut = node.ports.middle;
            
            if (!leftIn || !rightIn || !middleOut) return false;
            
            // Create two T nodes
            const t1Id = graph.addNode(NodeType.T);
            const t2Id = graph.addNode(NodeType.T);
            
            const t1 = graph.nodes[t1Id];
            const t2 = graph.nodes[t2Id];
            
            // Connect T nodes to inputs
            const leftConnected = graph.getConnected(leftIn);
            const rightConnected = graph.getConnected(rightIn);
            
            if (leftConnected) {
                graph.disconnect(leftIn);
                graph.connect(leftConnected, t1.ports.middle);
            }
            if (rightConnected) {
                graph.disconnect(rightIn);
                graph.connect(rightConnected, t2.ports.middle);
            }
            
            // Remove original nodes
            graph.removeNode(nodeId);
            graph.removeNode(tId);
            
            return true;
        }
        // Additional pruning types can be added here
        
        return false;
    }
}

const ALL_REACTIONS = [
    new BetaReaction(),
    new CombReaction(),
    new PruningReaction(),
];

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Reaction, BetaReaction, CombReaction, PruningReaction, ALL_REACTIONS };
}

