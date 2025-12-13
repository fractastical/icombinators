# Marius Buliga's Work on Interaction Combinators and Chemlambda

A comprehensive documentation and **working implementation** of Marius Buliga's research on graph rewriting systems, interaction combinators, and chemlambda artificial chemistry.

## Overview

This repository documents and implements the key contributions of Marius Buliga to the field of graph rewriting systems and artificial chemistry, including:

1. **Chemlambda** - A graph rewriting system inspired by lambda calculus that enables purely local, distributed computation
2. **Interaction Combinators** - Based on Yves Lafont's foundational work, adapted for directed graphs
3. **Directed Interaction Combinators** - Buliga's adaptation enabling artificial life properties
4. **chemSKI** - A graph rewriting system for SKI combinator calculus
5. **Quine Graphs** - Self-replicating graphs that exhibit metabolism, replication, and death

## Features

- ✅ **Working Python Implementation** - Actual code that runs
- ✅ **Working JavaScript/Browser Implementation** - Runs in browser, matches original demos
- ✅ **Graph Rewriting Engine** - Simulator for chemlambda reactions
- ✅ **Example Simulations** - Runnable examples demonstrating key concepts
- ✅ **Interactive Web Demo** - Browser-based visualization
- ✅ **Comprehensive Documentation** - Detailed explanations of all systems

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd icombinators

# Python 3.7+ required
python3 --version

# No external dependencies required (uses only standard library)
```

### Run Examples

**Python:**
```bash
# Run BETA reduction example
python3 examples/run_beta_example.py

# Run quine simulation example
python3 examples/run_quine_simulation.py

# Run interactive simulator
python3 examples/interactive_simulator.py

# Run tests
python3 test_basic.py
```

**JavaScript/Browser:**
```bash
# Open browser demo (no server needed!)
open examples/browser_demo.html

# Or with a local server:
python3 -m http.server 8000
# Then open http://localhost:8000/examples/browser_demo.html
```

## Implementation Structure

```
icombinators/
├── src/
│   ├── chemlambda/
│   │   ├── graph.py          # Graph data structure (Python)
│   │   ├── graph.js          # Graph data structure (JavaScript)
│   │   ├── reactions.py      # Reaction implementations (Python)
│   │   ├── reactions.js      # Reaction implementations (JavaScript)
│   │   ├── simulator.py      # Simulation engine (Python)
│   │   ├── simulator.js      # Simulation engine (JavaScript)
│   │   ├── visualizer.py     # Visualization (Python)
│   │   └── __init__.py
│   ├── interaction_combinators/  # (Coming soon)
│   └── chemski/              # (Coming soon)
├── examples/
│   ├── run_beta_example.py   # BETA reduction demo (Python)
│   ├── beta_example.js       # BETA reduction demo (JavaScript)
│   ├── browser_demo.html      # Interactive browser demo
│   ├── chemlambda-browser.js # Browser bundle
│   ├── run_quine_simulation.py  # Quine simulation
│   └── interactive_simulator.py # Interactive Python simulator
├── docs/                      # Documentation
├── reactions/                 # Reaction documentation
├── test_basic.py             # Python tests
└── README.md
```

## Table of Contents

- [Introduction and Background](docs/introduction.md)
- [Chemlambda System](docs/chemlambda.md)
- [Interaction Combinators](docs/interaction_combinators.md)
- [Directed Interaction Combinators](docs/directed_interaction_combinators.md)
- [chemSKI System](docs/chemski.md)
- [Quine Graphs](docs/quine_graphs.md)
- [Applications and Significance](docs/applications.md)

## Key Reactions

### Chemlambda Reactions (Implemented)
- [BETA Move](reactions/chemlambda/beta.md) - Core lambda calculus beta reduction ✅
- [FAN-IN Move](reactions/chemlambda/fan-in.md) - Fan-in operations
- [DIST Moves](reactions/chemlambda/dist.md) - Distribution operations for parallel reduction
- [PRUNING Moves](reactions/chemlambda/pruning.md) - Garbage collection and termination ✅
- [COMB Move](reactions/chemlambda/comb.md) - Arrow elimination ✅

### Interaction Combinators Reactions
- [Commutation Rules](reactions/interaction_combinators/commutation.md) - Interaction between different symbols
- [Annihilation Rules](reactions/interaction_combinators/annihilation.md) - Interaction between same symbols

### chemSKI Reactions
- [SKI Combinator Reductions](reactions/chemski/ski.md) - S, K, I combinator reactions

## Examples

- [Ackermann Function](examples/ackermann.md) - Computing Ackermann(2,2) with chemlambda
- [Ouroboros Quine](examples/ouroboros.md) - Self-replicating graph example
- [9-Quine](examples/9-quine.md) - Another quine graph example

## Usage

### Basic Usage

```python
from chemlambda import Graph, NodeType, Simulator, create_simple_application

# Create a graph
graph = create_simple_application()

# Create simulator
simulator = Simulator(graph)

# Run simulation
steps = simulator.run(max_steps=100)

# Get statistics
stats = simulator.get_stats()
print(f"Steps: {stats['total_steps']}")
print(f"Reactions: {stats['reaction_counts']}")
```

### Creating Custom Graphs

```python
from chemlambda import Graph, NodeType

graph = Graph()

# Add nodes
l_id = graph.add_node(NodeType.L)
a_id = graph.add_node(NodeType.A)

# Connect nodes
l_node = graph.nodes[l_id]
a_node = graph.nodes[a_id]
graph.connect(l_node.ports["right"], a_node.ports["left"])

# Run simulation
simulator = Simulator(graph)
simulator.run()
```

## Key Papers

- [Artificial chemistry experiments with chemlambda, lambda calculus, interaction combinators](https://arxiv.org/abs/2003.14332) (arXiv:2003.14332)
- [Graph rewrites, from graphic lambda calculus, to chemlambda, to directed interaction combinators](https://arxiv.org/abs/2007.10288) (arXiv:2007.10288)
- [Artificial life properties of directed interaction combinators vs. chemlambda](https://arxiv.org/abs/2005.06060) (arXiv:2005.06060)
- [Molecular computers with interaction combinators like graph rewriting systems](https://github.com/chemlambda/molecular)
- [chemSKI with tokens: world building and economy in the SKI universe](https://arxiv.org/abs/2306.00938) (arXiv:2306.00938)

## Resources

- [Chemlambda Project Page](https://chemlambda.github.io/)
- [Marius Buliga's Homepage](https://mbuliga.github.io/)
- [GitHub: chemlambda/molecular](https://github.com/chemlambda/molecular)
- [GitHub: mbuliga/chemski](https://github.com/mbuliga/chemski)

## Motivation

Buliga's work bridges several important areas:

1. **Molecular Computing**: The goal of computing with real chemistry, where molecules transform through chemical reactions to perform computation
2. **Decentralized Computing**: Local, asynchronous, distributed algorithms that require no global coordination
3. **Artificial Life**: Self-replicating structures that exhibit metabolism, replication, and death
4. **Graph Rewriting Universality**: Understanding computation at the structural level, independent of semantics

## Structure-to-Structure Computation

A key insight of Buliga's work is the focus on **structure-to-structure** computation rather than meaning-to-meaning computation. This allows:

- Computation without semantic constraints
- Natural parallel reduction
- Emergence of artificial life properties
- Potential implementation in real chemistry

## Contributing

Contributions welcome! Areas for contribution:

- More reaction implementations (DIST moves, FAN-IN, etc.)
- Interaction combinators implementation
- chemSKI implementation
- Visualization tools
- More examples
- Performance optimizations

## License

This documentation and implementation is provided for educational and research purposes. Please refer to the original papers and repositories for licensing information.
