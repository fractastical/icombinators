/**
 * Chemlambda Graph Structure (JavaScript)
 * Implements the graph representation for chemlambda molecules
 */

const NodeType = {
    L: 'L',           // Lambda
    A: 'A',           // Application
    FI: 'FI',         // Fan-In
    FO: 'FO',         // Fan-Out
    FOE: 'FOE',       // Fan-Out-Extra
    T: 'T',           // Termination
    ARROW: 'Arrow',   // Arrow connector
    FRIN: 'FRIN',     // Free input
    FROUT: 'FROUT'    // Free output
};

class Port {
    constructor(nodeId, portType, direction) {
        this.nodeId = nodeId;
        this.portType = portType;  // "middle", "left", "right"
        this.direction = direction; // "in" or "out"
    }
    
    equals(other) {
        return this.nodeId === other.nodeId && 
               this.portType === other.portType &&
               this.direction === other.direction;
    }
    
    toString() {
        return `Port(${this.nodeId}, ${this.portType}, ${this.direction})`;
    }
}

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

class Graph {
    constructor() {
        this.nodes = {};
        this.edges = new Map();  // Maps port -> connected port
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
        // Disconnect all ports
        Object.values(node.ports).forEach(port => {
            this.disconnect(port);
        });
        
        delete this.nodes[nodeId];
    }
    
    clone() {
        const newGraph = new Graph();
        newGraph.nextNodeId = this.nextNodeId;
        
        // Copy nodes
        Object.keys(this.nodes).forEach(nodeId => {
            const node = this.nodes[nodeId];
            newGraph.nodes[nodeId] = new Node(parseInt(nodeId), node.nodeType);
        });
        
        // Copy edges
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
                case NodeType.FI:
                    line = `FI ${this._getPortVar(node, 'left', 'in')} ${this._getPortVar(node, 'right', 'in')} ${this._getPortVar(node, 'middle', 'out')}`;
                    break;
                case NodeType.FO:
                    line = `FO ${this._getPortVar(node, 'middle', 'in')} ${this._getPortVar(node, 'left', 'out')} ${this._getPortVar(node, 'right', 'out')}`;
                    break;
                case NodeType.FOE:
                    line = `FOE ${this._getPortVar(node, 'middle', 'in')} ${this._getPortVar(node, 'left', 'out')} ${this._getPortVar(node, 'right', 'out')}`;
                    break;
                case NodeType.T:
                    line = `T ${this._getPortVar(node, 'middle', 'in')}`;
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
        if (connected) {
            return `n${connected.nodeId}`;
        }
        return `p${node.nodeId}_${portType}.${direction}`;
    }
    
    toString() {
        return `Graph(${Object.keys(this.nodes).length} nodes, ${this.edges.size / 2} edges)`;
    }
}

// Export for Node.js or browser
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Graph, Node, NodeType, Port };
}

