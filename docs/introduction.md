# Introduction and Background

## Historical Context

Marius Buliga's work on chemlambda and interaction combinators represents a significant contribution to the fields of graph rewriting, artificial chemistry, and molecular computing. The development can be traced through several key stages:

### From Graphic Lambda Calculus to Chemlambda

1. **Graphic Lambda Calculus (GLC)** - Buliga's initial work on a graphical representation of lambda calculus
2. **Chemical Concrete Machine** - First version of chemlambda (2013), introducing the concept of molecules and enzymes
3. **Chemlambda v1** - Refinement with local moves and graph rewriting
4. **Chemlambda v2** - Introduction of FOE (extra fan-out) node and additional moves
5. **Directed Interaction Combinators** - Adaptation of Lafont's interaction combinators for directed graphs
6. **chemSKI** - Graph rewriting system for SKI combinator calculus

## Relationship to Lafont's Interaction Combinators

Yves Lafont's **Interaction Combinators** (1997) provide a minimal system for graph rewriting with only three symbols (γ, δ, ε) and six interaction rules. Lafont showed that:

- Many interaction systems can be encoded using interaction combinators
- Lambda calculus can be encoded, demonstrating computational expressiveness
- The system provides a foundation for understanding graph rewriting computation

Buliga's contribution extends this work by:

- Adapting interaction combinators to **directed graphs**
- Showing that **conflicting rewrites** are beneficial for artificial life
- Demonstrating **quine graphs** and self-replication
- Connecting graph rewriting to **molecular computing**

## Key Papers Timeline

- **2013**: Graphic lambda calculus, Chemical concrete machine
- **2014**: Chemlambda, universality and self-multiplication (with L.H. Kauffman)
- **2015**: Molecular computers
- **2020**: Artificial chemistry experiments with chemlambda (arXiv:2003.14332)
- **2020**: Graph rewrites, from graphic lambda calculus, to chemlambda, to directed interaction combinators (arXiv:2007.10288)
- **2020**: Artificial life properties of directed interaction combinators vs. chemlambda (arXiv:2005.06060)
- **2023**: chemSKI with tokens (arXiv:2306.00938)

## Motivation: Molecular Computers and Artificial Chemistry

### The Three-Stage Process

Traditional computation follows:
1. **Meaning to Structure**: Program → Graph
2. **Structure to Structure**: Graph reduction
3. **Structure to Meaning**: Final graph → Result

Buliga's approach focuses on **structure-to-structure** computation:

1. **Meaning to Structure**: Create initial molecule from specification
2. **Structure to Structure**: Random chemical reactions transform the molecule
3. **Structure to Meaning**: Observe the final structure

### Key Differences

- **No semantic constraints**: The reduction doesn't need to preserve meaning
- **No control**: Reactions happen randomly, mediated by enzymes
- **Decentralized**: No global coordination needed
- **Local**: Each reaction involves only a small part of the graph

### Molecular Computing Goal

The ultimate goal is to build a **molecular computer** where:
- One molecule encodes a computation
- Random chemical reactions (mediated by enzymes) transform it
- The final molecule represents the result
- Example: Compute Ackermann(2,2) with ~40 chemical reactions

## Core Concepts

### Graph Rewriting

Graphs are transformed by **local rewrite rules** that:
- Match a pattern in the graph
- Replace it with another pattern
- Are applied in parallel when possible
- Require no global coordination

### Artificial Chemistry

The graph rewriting rules are viewed as **chemical reactions**:
- Graphs are "molecules"
- Rewrite rules are "reactions"
- Enzymes mediate reactions
- Reactions can happen randomly

### Quine Graphs

Special graphs that can **replicate themselves**:
- Have non-conflicting matches of rewrite patterns
- After parallel application, produce isomorphic copies
- Exhibit metabolism: can multiply or die
- Demonstrate artificial life properties

## Significance

Buliga's work is significant because it:

1. **Bridges computation and chemistry**: Shows how computation can be performed through chemical reactions
2. **Enables decentralized computing**: Local, asynchronous algorithms
3. **Demonstrates artificial life**: Self-replication, metabolism, death
4. **Demonstrates expressiveness**: Minimal systems that can encode many computations
5. **Challenges semantics**: Shows computation can emerge from structure alone

## Next Steps

- [Chemlambda System](chemlambda.md) - Detailed documentation of the chemlambda graph rewriting system
- [Interaction Combinators](interaction_combinators.md) - Lafont's foundational system
- [Directed Interaction Combinators](directed_interaction_combinators.md) - Buliga's adaptation

