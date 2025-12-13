/**
 * Chemlambda Browser Bundle
 * All chemlambda code bundled for browser use
 */

// NodeType enum
const NodeType = {
    L: 'L',
    A: 'A',
    FI: 'FI',
    FO: 'FO',
    FOE: 'FOE',
    T: 'T',
    ARROW: 'Arrow',
    FRIN: 'FRIN',
    FROUT: 'FROUT'
};

// Port class
class Port {
    constructor(nodeId, portType, direction) {
        this.nodeId = nodeId;
        this.portType = portType;
        this.direction = direction;
    }
    
    equals(other) {
        return this.nodeId === other.nodeId && 
               this.portType === other.portType &&
               this.direction === other.direction;
    }
}

// Node class
class Node {
    constructor(nodeId, nodeType) {
        this.nodeId = nodeId;
        this.nodeType = nodeType;
        this.ports = {};
        this._initPorts();
    }
    
    _initPorts() {
        switch (this.nodeType) {
            case NodeType.L:
                this.ports.middle = new Port(this.nodeId, 'middle', 'in');
                this.ports.left = new Port(this.nodeId, 'left', 'out');
                this.ports.right = new Port(this.nodeId, 'right', 'out');
                break;
            case NodeType.A:
                this.ports.left = new Port(this.nodeId, 'left', 'in');
                this.ports.right = new Port(this.nodeId, 'right', 'in');
                this.ports.middle = new Port(this.nodeId, 'middle', 'out');
                break;
            case NodeType.FI:
                this.ports.left = new Port(this.nodeId, 'left', 'in');
                this.ports.right = new Port(this.nodeId, 'right', 'in');
                this.ports.middle = new Port(this.nodeId, 'middle', 'out');
                break;
            case NodeType.FO:
                this.ports.middle = new Port(this.nodeId, 'middle', 'in');
                this.ports.left = new Port(this.nodeId, 'left', 'out');
                this.ports.right = new Port(this.nodeId, 'right', 'out');
                break;
            case NodeType.FOE:
                this.ports.middle = new Port(this.nodeId, 'middle', 'in');
                this.ports.left = new Port(this.nodeId, 'left', 'out');
                this.ports.right = new Port(this.nodeId, 'right', 'out');
                break;
            case NodeType.T:
                this.ports.middle = new Port(this.nodeId, 'middle', 'in');
                break;
            case NodeType.ARROW:
                this.ports.middle = new Port(this.nodeId, 'middle', 'in');
                this.ports.middle_out = new Port(this.nodeId, 'middle', 'out');
                break;
            case NodeType.FRIN:
                this.ports.middle = new Port(this.nodeId, 'middle', 'out');
                break;
            case NodeType.FROUT:
                this.ports.middle = new Port(this.nodeId, 'middle', 'in');
                break;
        }
    }
}

// Graph class
class Graph {
    constructor() {
        this.nodes = {};
        this.edges = new Map();
        this.nextNodeId = 0;
    }
    
    addNode(nodeType) {
        const nodeId = this.nextNodeId++;
        this.nodes[nodeId] = new Node(nodeId, nodeType);
        return nodeId;
    }
    
    connect(port1, port2) {
        this.edges.set(port1, port2);
        this.edges.set(port2, port1);
    }
    
    disconnect(port) {
        const other = this.edges.get(port);
        if (other) {
            this.edges.delete(port);
            this.edges.delete(other);
        }
    }
    
    getConnected(port) {
        return this.edges.get(port) || null;
    }
    
    removeNode(nodeId) {
        if (!this.nodes[nodeId]) return;
        const node = this.nodes[nodeId];
        Object.values(node.ports).forEach(port => this.disconnect(port));
        delete this.nodes[nodeId];
    }
    
    clone() {
        const newGraph = new Graph();
        newGraph.nextNodeId = this.nextNodeId;
        Object.keys(this.nodes).forEach(nodeId => {
            const node = this.nodes[nodeId];
            newGraph.nodes[nodeId] = new Node(parseInt(nodeId), node.nodeType);
        });
        this.edges.forEach((port2, port1) => {
            const node1 = newGraph.nodes[port1.nodeId];
            const node2 = newGraph.nodes[port2.nodeId];
            if (node1 && node2) {
                const port1New = node1.ports[port1.portType];
                const port2New = node2.ports[port2.portType];
                if (port1New && port2New) {
                    newGraph.connect(port1New, port2New);
                }
            }
        });
        return newGraph;
    }
    
    toMolFormat() {
        const lines = [];
        const nodeIds = Object.keys(this.nodes).map(id => parseInt(id)).sort((a, b) => a - b);
        nodeIds.forEach(nodeId => {
            const node = this.nodes[nodeId];
            let line = '';
            switch (node.nodeType) {
                case NodeType.L:
                    line = `L ${this._getPortVar(node, 'middle', 'in')} ${this._getPortVar(node, 'left', 'out')} ${this._getPortVar(node, 'right', 'out')}`;
                    break;
                case NodeType.A:
                    line = `A ${this._getPortVar(node, 'left', 'in')} ${this._getPortVar(node, 'right', 'in')} ${this._getPortVar(node, 'middle', 'out')}`;
                    break;
                case NodeType.ARROW:
                    line = `Arrow ${this._getPortVar(node, 'middle', 'in')} ${this._getPortVar(node, 'middle', 'out')}`;
                    break;
            }
            if (line) lines.push(line);
        });
        return lines.join('\n');
    }
    
    _getPortVar(node, portType, direction) {
        const port = node.ports[portType];
        if (!port) return '?';
        const connected = this.getConnected(port);
        if (connected) return `n${connected.nodeId}`;
        return `p${node.nodeId}_${portType}.${direction}`;
    }
    
    toString() {
        return `Graph(${Object.keys(this.nodes).length} nodes, ${this.edges.size / 2} edges)`;
    }
}

// BetaReaction class
class BetaReaction {
    getName() { return 'BETA'; }
    
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
        if (!graph.nodes[lId] || !graph.nodes[aId]) return false;
        const lNode = graph.nodes[lId];
        const aNode = graph.nodes[aId];
        if (lNode.nodeType !== NodeType.L || aNode.nodeType !== NodeType.A) return false;
        
        const lMiddleIn = lNode.ports.middle;
        const lLeftOut = lNode.ports.left;
        const lRightOut = lNode.ports.right;
        const aLeftIn = aNode.ports.left;
        const aRightIn = aNode.ports.right;
        const aMiddleOut = aNode.ports.middle;
        
        if (!lMiddleIn || !lLeftOut || !lRightOut || !aLeftIn || !aRightIn || !aMiddleOut) return false;
        if (!graph.getConnected(lRightOut).equals(aLeftIn)) return false;
        
        graph.disconnect(lRightOut);
        
        const arrow1Id = graph.addNode(NodeType.ARROW);
        const arrow2Id = graph.addNode(NodeType.ARROW);
        const arrow1 = graph.nodes[arrow1Id];
        const arrow2 = graph.nodes[arrow2Id];
        
        const arrow1In = arrow1.ports.middle;
        const arrow1Out = arrow1.ports.middle_out;
        const arrow2In = arrow2.ports.middle;
        const arrow2Out = arrow2.ports.middle_out;
        
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
        
        graph.removeNode(lId);
        graph.removeNode(aId);
        return true;
    }
}

// CombReaction class
class CombReaction {
    getName() { return 'COMB'; }
    
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
                if (connectedIn.nodeId !== arrowNode.nodeId && connectedOut.nodeId !== arrowNode.nodeId) {
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
        if (connectedIn.nodeId === connectedOut.nodeId) return false;
        graph.disconnect(arrowIn);
        graph.disconnect(arrowOut);
        graph.connect(connectedIn, connectedOut);
        graph.removeNode(arrowId);
        return true;
    }
}

const ALL_REACTIONS = [new BetaReaction(), new CombReaction()];

// Simulator class
class Simulator {
    constructor(graph, reactions = null) {
        this.graph = graph;
        this.reactions = reactions || ALL_REACTIONS;
        this.stepCount = 0;
        this.history = [];
        this.reactionHistory = [];
    }
    
    step(randomOrder = true) {
        const allMatches = [];
        this.reactions.forEach(reaction => {
            const matches = reaction.canApply(this.graph);
            matches.forEach(match => allMatches.push([reaction, match]));
        });
        if (allMatches.length === 0) return false;
        
        let reaction, match;
        if (randomOrder) {
            const randomIndex = Math.floor(Math.random() * allMatches.length);
            [reaction, match] = allMatches[randomIndex];
        } else {
            const priorityOrder = ['BETA', 'FAN-IN', 'DIST', 'PRUNING', 'COMB'];
            const sorted = allMatches.sort((a, b) => {
                const aPriority = priorityOrder.indexOf(a[0].getName()) !== -1 ? priorityOrder.indexOf(a[0].getName()) : 999;
                const bPriority = priorityOrder.indexOf(b[0].getName()) !== -1 ? priorityOrder.indexOf(b[0].getName()) : 999;
                return aPriority - bPriority;
            });
            [reaction, match] = sorted[0];
        }
        
        this.history.push(this.graph.clone());
        const success = reaction.apply(this.graph, match);
        
        if (success) {
            this.stepCount++;
            this.reactionHistory.push([this.stepCount, reaction.getName(), match]);
            if (reaction.getName() !== 'COMB') {
                this._combCycle();
            }
        }
        return success;
    }
    
    _combCycle() {
        const combReaction = this.reactions.find(r => r.getName() === 'COMB');
        if (!combReaction) return;
        let iterations = 0;
        while (iterations < 100) {
            const matches = combReaction.canApply(this.graph);
            if (matches.length === 0) break;
            if (!combReaction.apply(this.graph, matches[0])) break;
            iterations++;
        }
    }
    
    run(maxSteps = 1000, randomOrder = true) {
        let steps = 0;
        while (steps < maxSteps) {
            if (!this.step(randomOrder)) break;
            steps++;
        }
        return steps;
    }
    
    getStats() {
        const reactionCounts = {};
        this.reactionHistory.forEach(([step, reactionName, match]) => {
            reactionCounts[reactionName] = (reactionCounts[reactionName] || 0) + 1;
        });
        return {
            totalSteps: this.stepCount,
            reactionCounts: reactionCounts,
            finalNodes: Object.keys(this.graph.nodes).length,
            finalEdges: this.graph.edges.size / 2,
        };
    }
}

function createSimpleApplication() {
    const graph = new Graph();
    const lId = graph.addNode(NodeType.L);
    const lNode = graph.nodes[lId];
    const a1Id = graph.addNode(NodeType.A);
    const a1Node = graph.nodes[a1Id];
    const a2Id = graph.addNode(NodeType.A);
    const a2Node = graph.nodes[a2Id];
    graph.connect(lNode.ports.right, a1Node.ports.left);
    graph.connect(a2Node.ports.middle, a1Node.ports.right);
    graph.connect(lNode.ports.left, a1Node.ports.middle);
    return graph;
}

