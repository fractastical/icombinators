# Quine Graphs

Quine graphs are self-replicating graphs that exhibit metabolism, replication, and death. They represent a major contribution of Buliga's work, demonstrating artificial life properties in graph rewriting systems.

## Definition

A **quine graph** G is a graph such that:

1. It has a **non-void maximal collection** of non-conflicting matches of rewrite patterns
2. After **parallel application** of these rewrites, the result is **isomorphic to G**
3. The graph can produce copies of itself through reduction

### Formal Definition

Given a graph rewrite system, a graph G is a quine graph if:
- There exists a maximal collection of non-conflicting matches of left-hand-side patterns
- When these matches are applied in parallel, the resulting graph is isomorphic to G
- This property can be maintained through multiple reduction steps

## Key Properties

### Metabolism

Quine graphs exhibit **metabolism**:
- Process "food" (other graphs or patterns)
- Transform themselves through reactions
- Maintain structure while changing
- Can multiply or die depending on reactions

### Replication

- Can create copies of themselves
- Through parallel application of rewrites
- Demonstrates self-reproduction
- Similar to biological cell division

### Death

- Can fail to replicate
- Can be destroyed by certain reactions
- Demonstrates mortality
- Shows life-like behavior

### Senescence

Some quines show **aging behavior**:
- Replication becomes less likely over time
- Structure degrades
- Similar to biological aging
- Can be studied through hazard functions

## Examples

### Ouroboros

The **Ouroboros quine** is inspired by the lambda calculus predecessor term:

- Self-replicating structure
- Named after the mythical snake eating its own tail
- Demonstrates circular self-reference
- Can replicate through parallel rewrites

**Properties**:
- Stable replication pattern
- Well-studied example
- Demonstrates key quine mechanisms

### 9-Quine

A quine graph with 9 nodes:

- Simpler than Ouroboros
- Still exhibits replication
- Used in experiments on senescence
- Shows that small graphs can be quines

### Ackermann Quines

Quines that compute the Ackermann function:

- Combine computation with replication
- Show that computation and life can coexist
- Demonstrate complex quine behavior
- Used in molecular computing experiments

## Mechanisms

### Non-Conflicting Matches

For a quine to replicate:
- Must have multiple non-conflicting rewrite matches
- These matches can be applied in parallel
- Result preserves graph structure
- Enables replication

### Parallel Application

- All matching rewrites applied simultaneously
- No sequential ordering needed
- Preserves isomorphism
- Enables self-replication

### Random Rewriting

Quine graphs are studied with **random rewriting algorithms**:
- Random selection of applicable rewrites
- Can lead to replication or death
- Demonstrates probabilistic behavior
- Similar to biological processes

## Artificial Life Properties

### Replication

- Graphs create copies of themselves
- Through parallel rewrites
- Demonstrates self-reproduction
- Foundation for artificial life

### Metabolism

- Process and transform structures
- Maintain identity while changing
- Process "food" (other graphs)
- Demonstrate life-like behavior

### Death

- Can fail to replicate
- Can be destroyed
- Shows mortality
- Completes life cycle

### Evolution

- Can evolve through mutations
- Different reduction paths
- Selection through replication success
- Demonstrates evolution

## Experimental Studies

### Hazard Functions

Study of quine "lifespan":
- Probability of replication vs. death
- Hazard functions over time
- Senescence patterns
- Life expectancy

### Population Dynamics

- Multiple quines in a system
- Competition for resources
- Population growth/decline
- Ecosystem behavior

### Open-Ended Evolution

- New quine types can emerge
- Evolution of new species
- Complexification over time
- Demonstrates open-endedness

## Why Quines Matter

### Artificial Life

- Demonstrate life-like behavior
- Show that life can emerge from computation
- Bridge computation and biology
- Enable study of life principles

### Molecular Computing

- Potential for self-replicating computers
- Understanding biological replication
- Molecular implementation possibility
- Bridge to real chemistry

### Graph Rewriting Theory

- Extends understanding of graph rewriting
- Shows importance of conflicts
- Demonstrates new computational paradigms
- Reveals structure-behavior relationships

### Philosophy

- Challenges notions of life
- Shows computation can be alive
- Demonstrates emergence
- Connects mathematics and biology

## Comparison: Quines in Different Systems

### Directed Interaction Combinators

- Strong quine properties
- Good replication
- Well-studied

### Chemlambda

- Also supports quines
- Different mechanisms
- Complementary to IC quines

### Both Systems

- Quines require conflicting rewrites
- Parallel application essential
- Random algorithms reveal behavior
- Life-like properties emerge

## Research Directions

### Finding New Quines

- Search algorithms for quine graphs
- Classification of quine types
- Understanding quine structure

### Quine Evolution

- How quines evolve
- Emergence of new quine types
- Evolution of complexity

### Molecular Implementation

- Can quines be implemented in chemistry?
- What molecules would be needed?
- Experimental feasibility

## References

- Buliga, M. (2020). "Artificial chemistry experiments with chemlambda, lambda calculus, interaction combinators." arXiv:2003.14332
- Buliga, M. (2020). "Artificial life properties of directed interaction combinators vs. chemlambda." arXiv:2005.06060
- See [Ouroboros Example](examples/ouroboros.md) for detailed Ouroboros documentation
- See [9-Quine Example](examples/9-quine.md) for 9-quine documentation

