# Directed Interaction Combinators

Marius Buliga's adaptation of Lafont's Interaction Combinators for directed graphs, enabling artificial life properties and quine graphs.

## Differences from Lafont's System

### Directed Graphs

- **Lafont's system**: Undirected graphs, symmetric interactions
- **Buliga's system**: Directed graphs, asymmetric interactions
- Enables more complex interaction patterns
- Better suited for artificial chemistry experiments

### Conflicting Rewrites

- **Lafont's system**: Non-conflicting rewrites preferred
- **Buliga's system**: **Conflicting rewrites are beneficial**
- Key insight: Conflicts enable artificial life properties
- Allows graphs to have multiple possible reduction paths

### Artificial Life Focus

- **Lafont's system**: Focus on computation universality
- **Buliga's system**: Focus on artificial life properties
- Enables replication, metabolism, death
- Demonstrates life-like behavior in graph rewriting

## Key Reactions

The directed interaction combinators maintain similar structure to Lafont's but with directionality:

### Directed Commutation

When different symbols interact in directed graphs:
- Connections follow direction
- Information flows in one direction
- Enables sequential and parallel patterns

### Directed Annihilation

When same symbols interact:
- Elimination follows direction
- Can create cycles or propagate changes
- Enables self-replication patterns

## Quine Graphs

A major contribution: graphs that can **replicate themselves**.

### Definition

A **quine graph** is a graph G such that:
- It has a non-void maximal collection of non-conflicting matches of rewrite patterns
- After parallel application of these rewrites, the result is isomorphic to G
- The graph can produce copies of itself

### Properties

- **Metabolism**: Can multiply (replicate) or die (fail to replicate)
- **Self-replication**: Produces isomorphic copies
- **Life-like behavior**: Exhibits properties of living systems

### Examples

- **Ouroboros**: Inspired by lambda calculus predecessor term
- **9-quine**: A quine with 9 nodes
- **Ackermann quines**: Quines that compute Ackermann function

## Artificial Life Properties

### Replication

- Graphs can create copies of themselves
- Through parallel application of rewrites
- Demonstrates self-reproduction

### Metabolism

- Graphs process "food" (other graphs or patterns)
- Transform themselves through reactions
- Maintain structure while changing

### Death

- Graphs can fail to replicate
- Can be destroyed by certain reactions
- Demonstrates mortality

### Senescence

- Some quines show aging behavior
- Replication becomes less likely over time
- Similar to biological aging

## Why Conflicting Rewrites Matter

### Traditional View

- Non-conflicting rewrites preferred
- Ensures deterministic computation
- Good for decentralized computing

### Buliga's Insight

- **Conflicting rewrites enable artificial life**
- Allow multiple reduction paths
- Enable replication and metabolism
- Show that determinism isn't always desirable

### Experimental Evidence

From arXiv:2005.06060:
- Directed interaction combinators with conflicts show better ALife properties
- Quine graphs require conflicting patterns
- Replication emerges from conflicts

## Applications

### Artificial Life

- Study of self-replication
- Understanding life-like behavior
- Emergence of complexity

### Molecular Computing

- Potential for self-replicating molecular computers
- Understanding how computation can emerge from chemistry
- Bridge between computation and biology

### Graph Rewriting Theory

- Extends understanding of graph rewriting
- Shows importance of conflicts
- Demonstrates new computational paradigms

## Comparison: Directed IC vs Chemlambda

| Property | Directed IC | Chemlambda |
|----------|-------------|------------|
| Graph type | Directed | Directed |
| Conflicts | Allowed, beneficial | Allowed |
| ALife properties | Strong | Strong |
| Quine graphs | Yes | Yes |
| Lambda calculus | Via encoding | Direct |
| Node types | 3 (γ, δ, ε) | 7 (L, A, FI, FO, FOE, T, Arrow) |

## Significance

Buliga's directed interaction combinators show:

1. **Conflicts are beneficial**: Not a bug, but a feature for ALife
2. **Life can emerge from computation**: Self-replication in graph rewriting
3. **Structure enables behavior**: No semantics needed for life-like properties
4. **Minimal systems can be complex**: Simple rules, complex behavior

## References

- Buliga, M. (2020). "Artificial life properties of directed interaction combinators vs. chemlambda." arXiv:2005.06060
- See [Quine Graphs](quine_graphs.md) for detailed quine documentation
- See [Interaction Combinators](interaction_combinators.md) for Lafont's original system

