/**
 * Chemlambda Simulator (JavaScript)
 * Runs graph rewriting simulations
 */

const { Graph, NodeType } = require('./graph.js');
const { ALL_REACTIONS } = require('./reactions.js');

class Simulator {
    constructor(graph, reactions = null) {
        this.graph = graph;
        this.reactions = reactions || ALL_REACTIONS;
        this.stepCount = 0;
        this.history = [];
        this.reactionHistory = [];
    }
    
    step(randomOrder = true) {
        // Find all possible reactions
        const allMatches = [];
        
        this.reactions.forEach(reaction => {
            const matches = reaction.canApply(this.graph);
            matches.forEach(match => {
                allMatches.push([reaction, match]);
            });
        });
        
        if (allMatches.length === 0) {
            return false;
        }
        
        // Select a match
        let reaction, match;
        if (randomOrder) {
            const randomIndex = Math.floor(Math.random() * allMatches.length);
            [reaction, match] = allMatches[randomIndex];
        } else {
            // Priority order: BETA/FAN-IN > DIST > PRUNING > COMB
            const priorityOrder = ['BETA', 'FAN-IN', 'DIST', 'PRUNING', 'COMB'];
            const sorted = allMatches.sort((a, b) => {
                const aPriority = priorityOrder.indexOf(a[0].getName()) !== -1 
                    ? priorityOrder.indexOf(a[0].getName()) 
                    : 999;
                const bPriority = priorityOrder.indexOf(b[0].getName()) !== -1 
                    ? priorityOrder.indexOf(b[0].getName()) 
                    : 999;
                return aPriority - bPriority;
            });
            [reaction, match] = sorted[0];
        }
        
        // Save current state
        this.history.push(this.graph.clone());
        
        // Apply reaction
        const success = reaction.apply(this.graph, match);
        
        if (success) {
            this.stepCount++;
            this.reactionHistory.push([this.stepCount, reaction.getName(), match]);
            
            // Apply COMB cycle after other reactions
            if (reaction.getName() !== 'COMB') {
                this._combCycle();
            }
        }
        
        return success;
    }
    
    _combCycle() {
        const combReaction = this.reactions.find(r => r.getName() === 'COMB');
        if (!combReaction) return;
        
        const maxIterations = 100;
        let iterations = 0;
        
        while (iterations < maxIterations) {
            const matches = combReaction.canApply(this.graph);
            if (matches.length === 0) break;
            
            const success = combReaction.apply(this.graph, matches[0]);
            if (!success) break;
            
            iterations++;
        }
    }
    
    run(maxSteps = 1000, randomOrder = true) {
        let steps = 0;
        while (steps < maxSteps) {
            if (!this.step(randomOrder)) {
                break;
            }
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
    
    // Lambda: L
    const lId = graph.addNode(NodeType.L);
    const lNode = graph.nodes[lId];
    
    // Application: A (for applying lambda)
    const a1Id = graph.addNode(NodeType.A);
    const a1Node = graph.nodes[a1Id];
    
    // Argument: A (represents 'y')
    const a2Id = graph.addNode(NodeType.A);
    const a2Node = graph.nodes[a2Id];
    
    // Connect L to A1 (lambda application)
    graph.connect(lNode.ports.right, a1Node.ports.left);
    
    // Connect A2 (argument) to A1.right.in
    graph.connect(a2Node.ports.middle, a1Node.ports.right);
    
    // Connect L.left.out to A1.middle.out (lambda body)
    graph.connect(lNode.ports.left, a1Node.ports.middle);
    
    return graph;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Simulator, createSimpleApplication };
}

