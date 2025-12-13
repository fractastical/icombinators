# DIST Family (Distribution Moves)

The DIST family of moves enables distribution of operations over fan-out nodes, which is essential for parallel reduction and efficient computation.

## Overview

Distribution moves allow operations to be "distributed" over fan-out nodes, creating multiple copies of the operation that can be processed in parallel. This is crucial for:

- **Parallel reduction**: Multiple reductions can happen simultaneously
- **Efficiency**: Avoids sequential processing
- **Non-linear computation**: Handles cases where values are used multiple times

## DIST Moves

### 1. FO-FOE Distribution

```
FO 1 2 c, FOE c 3 4 → FI j i 2, FO k i 3, FO l j 4, FOE 1 k l
```

**What it does**: Distributes fan-out over fan-out-extra, creating a network of fan operations.

**Why important**: 
- Enables parallel duplication
- Creates multiple fan-out paths
- Essential for efficient reduction

### 2. FI-FO Distribution

```
FI 1 4 c, FO c 2 3 → FO 1 i j, FI i k 2, FI j l 3, FO 4 k l
```

**What it does**: Distributes fan-in over fan-out, creating a network that combines multiple inputs and outputs.

**Why important**:
- Handles complex parallel operations
- Combines multiple inputs/outputs
- Enables efficient reduction

### 3. L-FO Distribution

```
L 1 2 c, FO c 3 4 → FI j i 2, L k i 3, L l j 4, FOE 1 k l
```

**What it does**: Distributes lambda abstraction over fan-out, duplicating the lambda.

**Why important**:
- Enables parallel lambda reductions
- Handles cases where lambda is used multiple times
- Critical for efficient computation

### 4. L-FOE Distribution

```
L 1 2 c, FOE c 3 4 → FI j i 2, L k i 3, L l j 4, FOE 1 k l
```

Same as L-FO but with FOE instead of FO.

### 5. A-FO Distribution

```
A 1 4 c, FO c 2 3 → FOE 1 i j, A i k 2, A j l 3, FOE 4 k l
```

**What it does**: Distributes application over fan-out, creating multiple applications.

**Why important**:
- Enables parallel application reductions
- Handles multiple uses of an argument
- Essential for efficient computation

### 6. A-FOE Distribution

```
A 1 4 c, FOE c 2 3 → FOE 1 i j, A i k 2, A j l 3, FOE 4 k l
```

Same as A-FO but with FOE instead of FO.

## Visual Representation

### Example: L-FO Distribution

#### Before
```
    L              FO
   /|\            /|\
  1 2 c          c 3 4
     |            |
     +------------+
   (connected)
```

#### After
```
  FI              L              L            FOE
 j i 2          k i 3          l j 4        1 k l
```

## Why DIST Moves Are Important

### Parallel Reduction

- **Enables parallelism**: Multiple operations can happen simultaneously
- **Efficiency**: Avoids sequential bottlenecks
- **Scalability**: Works for large computations

### Non-Linear Computation

- **Handles duplication**: When values are used multiple times
- **Distributes work**: Creates multiple copies for parallel processing
- **Optimizes reduction**: More efficient than sequential reduction

### Local Operation

- **No global coordination**: Each move is local
- **Independent**: Moves can happen in parallel
- **Decentralized**: No central control needed

## Implementation

### Pattern Matching

For each DIST move:
1. Find the pattern (e.g., L connected to FO)
2. Identify all connections
3. Create new nodes according to the rule
4. Wire them together correctly

### Application

1. Remove the original connection
2. Create new nodes (FI, L, FOE, etc.)
3. Wire them according to the rule
4. Connect to the rest of the graph

## Example: Distributing a Lambda

### Initial Graph
```
L a b c, FO c d e
```

This represents a lambda that will be used in two places.

### After L-FO Distribution
```
FI j i b, L k i d, L l j e, FOE a k l
```

Now we have:
- Two lambda nodes (L k i d and L l j e)
- A fan-in (FI j i b) combining them
- A fan-out-extra (FOE a k l) for the input

### Result

The lambda is now duplicated and can be reduced in parallel in both places.

## Relationship to Other Moves

### With BETA

- DIST moves prepare graphs for BETA reduction
- Create multiple lambda/application pairs
- Enable parallel beta reductions

### With PRUNING

- DIST moves can create unused branches
- PRUNING removes them
- Together they optimize reduction

### With COMB

- DIST moves create Arrow nodes
- COMB eliminates them
- Together they simplify graphs

## Priority in Reduction

DIST moves typically have **high priority** in reduction algorithms:

1. **First**: FO-FOE distribution
2. **Second**: Other DIST moves with free nodes
3. **Third**: BETA and FAN-IN moves
4. **Fourth**: PRUNING moves

This ensures efficient parallel reduction.

## References

- See [BETA Move](beta.md) for how DIST prepares for beta reduction
- See [PRUNING Moves](pruning.md) for cleanup after DIST
- See [Chemlambda System](../docs/chemlambda.md) for context

