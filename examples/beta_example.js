#!/usr/bin/env node
/**
 * Example: Running BETA reduction (JavaScript/Node.js)
 * Demonstrates the BETA move in action
 */

const { Graph, NodeType } = require('../src/chemlambda/graph.js');
const { Simulator, createSimpleApplication } = require('../src/chemlambda/simulator.js');

function main() {
    console.log('='.repeat(60));
    console.log('Chemlambda BETA Reduction Example (JavaScript)');
    console.log('='.repeat(60));
    console.log();
    
    // Create graph for (λx.x) y
    console.log('Creating graph for (λx.x) y (identity function applied to y)');
    const graph = createSimpleApplication();
    
    console.log(`Initial graph: ${graph}`);
    console.log(`Nodes: ${Object.keys(graph.nodes).length}`);
    console.log(`Edges: ${graph.edges.size / 2}`);
    console.log();
    
    console.log('Initial graph structure:');
    console.log(graph.toMolFormat());
    console.log();
    
    // Create simulator
    const simulator = new Simulator(graph);
    
    // Run simulation
    console.log('Running simulation...');
    console.log('-'.repeat(60));
    
    let steps = 0;
    const maxSteps = 10;
    
    while (steps < maxSteps) {
        const applied = simulator.step(false);
        if (!applied) {
            console.log('No more reactions can be applied.');
            break;
        }
        
        steps++;
        const [step, reactionName, match] = simulator.reactionHistory[simulator.reactionHistory.length - 1];
        console.log(`Step ${step}: Applied ${reactionName}`);
        console.log(`  Graph: ${simulator.graph}`);
        console.log(`  Nodes: ${Object.keys(simulator.graph.nodes).length}, ` +
                   `Edges: ${simulator.graph.edges.size / 2}`);
    }
    
    console.log('-'.repeat(60));
    console.log();
    
    // Final state
    console.log('Final graph structure:');
    console.log(simulator.graph.toMolFormat());
    console.log();
    
    // Statistics
    const stats = simulator.getStats();
    console.log('Simulation Statistics:');
    console.log(`  Total steps: ${stats.totalSteps}`);
    console.log(`  Reaction counts:`, stats.reactionCounts);
    console.log(`  Final nodes: ${stats.finalNodes}`);
    console.log(`  Final edges: ${stats.finalEdges}`);
}

if (require.main === module) {
    main();
}

