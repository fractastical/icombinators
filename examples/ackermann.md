# Ackermann Function Computation

The Ackermann function is a classic example of a non-primitively recursive function that can be computed using chemlambda. Computing Ackermann(2,2) demonstrates the power of the graph rewriting system.

## Goal

Compute **Ackermann(2,2)** using chemlambda graph rewriting:
- Approximately **40 chemical reactions** (rewrites)
- Final molecule is a simple **ring structure**
- Demonstrates feasibility of molecular computing
- Benchmark for molecular computer proposals

## Why Ackermann Function?

### Non-Primitively Recursive

- **Beyond primitive recursion**: Cannot be computed with simple loops
- **Complex computation**: Requires sophisticated reduction
- **Good benchmark**: Tests the system's capabilities

### Manageable Size

- **Ackermann(2,2)**: Small enough to be feasible
- **~40 rewrites**: Manageable number of reactions
- **Simple result**: Final structure is just a ring

### Interesting Properties

- **Exponential growth**: Shows how computation can grow
- **Nested recursion**: Tests nested function calls
- **Complex reduction**: Requires many steps

## Ackermann Function Definition

```
A(0, n) = n + 1
A(m, 0) = A(m-1, 1)
A(m, n) = A(m-1, A(m, n-1))
```

For Ackermann(2,2):
```
A(2, 2) = A(1, A(2, 1))
        = A(1, A(1, A(2, 0)))
        = A(1, A(1, A(1, 1)))
        = ... (many steps)
        = 7
```

## Graph Representation

### Initial Graph

The initial graph encodes the Ackermann function application:
- Lambda abstractions for the function definition
- Applications for function calls
- Natural numbers encoded as graphs

### Reduction Process

The reduction proceeds through approximately 40 steps:

1. **Beta reductions**: Function applications
2. **Distribution moves**: Parallel processing
3. **Pruning moves**: Cleanup of unused parts
4. **COMB cycles**: Simplification

### Final Graph

The final graph is a simple **ring structure**:
- Represents the result: 7 (or the encoding of 7)
- Can be observed in a real experiment
- Simple structure makes verification easier

## Key Reactions Used

### BETA Moves

- **Function application**: Applying Ackermann function
- **Nested calls**: Handling recursive calls
- **Many applications**: Multiple beta reductions needed

### DIST Moves

- **Parallel reduction**: Distributing operations
- **Efficient processing**: Handling multiple operations simultaneously
- **Complex distributions**: Nested distributions

### PRUNING Moves

- **Garbage collection**: Removing unused parts
- **Cleanup**: Simplifying the graph
- **Optimization**: Keeping graph small

### COMB Moves

- **Arrow elimination**: Cleaning up intermediate connections
- **Simplification**: Making graph readable
- **Final cleanup**: Preparing for observation

## Molecular Computing Perspective

### Structure-to-Structure

- **Initial molecule**: Encodes Ackermann(2,2)
- **Chemical reactions**: Transform the molecule
- **Final molecule**: Encodes the result (7)

### Enzymes

Each rewrite requires an enzyme:
- **BETA enzyme**: Mediates beta reductions
- **DIST enzyme**: Mediates distribution moves
- **PRUNING enzyme**: Mediates pruning moves
- **COMB enzyme**: Mediates combination moves

### Observation

The final molecule (ring structure) can be observed:
- **Structure detection**: Identify the ring
- **Result extraction**: Interpret the structure as 7
- **Verification**: Confirm computation succeeded

## Challenges

### Real Chemistry

- **Molecule design**: Need molecules that can perform these rewrites
- **Enzyme design**: Need enzymes for each rewrite type
- **Observation**: Need to detect final structure

### Scalability

- **Larger inputs**: Ackermann(3,2) or Ackermann(4,4) are much larger
- **More reactions**: Exponential growth in number of reactions
- **Complexity**: Graphs become very complex

### Control

- **Random reactions**: Reactions happen randomly
- **No control**: Cannot control order of reactions
- **Reliability**: Need to ensure correct reduction

## Significance

### Proof of Concept

- **Feasibility**: Shows molecular computing is theoretically possible
- **Benchmark**: Provides a concrete example
- **Validation**: Validates the approach

### Molecular Computers

- **Goal**: Build real molecular computers
- **Step forward**: Ackermann(2,2) is a step toward this goal
- **Foundation**: Provides foundation for more complex computations

### Understanding

- **Computation**: Understanding how computation can emerge from chemistry
- **Structure**: Understanding structure-to-structure computation
- **Life**: Connection to biological processes

## References

- Buliga, M. (2015). "Molecular computers." Journal of Brief Ideas
- Buliga, M. (2015). "Molecular computers." [HTML version](http://chorasimilarity.github.io/chemlambda-gui/dynamic/molecular.html)
- See [Chemlambda System](../docs/chemlambda.md) for context on the rewriting system
- See [BETA Move](../reactions/chemlambda/beta.md) for beta reduction details

