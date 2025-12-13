# PRUNING Family

PRUNING moves handle unused variables and garbage collection, removing unnecessary parts of the graph to optimize computation.

## Overview

PRUNING moves eliminate parts of the graph that are no longer needed:

- **Unused variables**: Variables that don't appear in the body
- **Dead branches**: Computations that will never be used
- **Garbage collection**: Cleanup of unnecessary nodes

## PRUNING Moves

### 1. Application Pruning

```
A 1 2 3, T 3 → T 1, T 2
FI 1 2 3, T 3 → T 1, T 2
```

**What it does**: When an application or fan-in is connected to a termination node, both inputs are terminated.

**Why important**:
- Garbage collection for unused computations
- Prevents unnecessary computation
- Cleans up dead branches

**Visual representation**:
```
    A              T
   /|\             |
  1 2 3------------+
  
  becomes
  
    T              T
    1              2
```

### 2. Lambda Pruning

```
L 1 2 3, T 3 → T 1, T c, FRIN c
```

**What it does**: When a lambda's bound variable is unused, the lambda is pruned and a free input is created.

**Why important**:
- Handles unused lambda variables
- Enables optimization
- Cleans up unnecessary abstractions

**Visual representation**:
```
    L              T
   /|\             |
  1 2 3------------+
  
  becomes
  
    T              T            FRIN
    1              c             c
```

### 3. Fan-Out Pruning (Left Output)

```
FO 1 2 3, T 2 → Arrow 1 3
FOE 1 2 3, T 2 → Arrow 1 3
```

**What it does**: When the left output of a fan-out is unused, eliminate it and connect input directly to right output.

**Why important**:
- Optimizes fan-out operations
- Removes unnecessary duplication
- Simplifies the graph

**Visual representation**:
```
    FO             T
   /|\             |
  1 2 3------------+
     |
  
  becomes
  
  Arrow
   1 3
```

### 4. Fan-Out Pruning (Right Output)

```
FO 1 2 3, T 3 → Arrow 1 2
FOE 1 2 3, T 3 → Arrow 1 2
```

**What it does**: When the right output of a fan-out is unused, eliminate it and connect input directly to left output.

**Why important**: Same as left output pruning but for the other branch.

## Why PRUNING Is Important

### Garbage Collection

- **Removes unused nodes**: Prevents accumulation of garbage
- **Optimizes memory**: Keeps graphs small
- **Improves performance**: Less to process

### Optimization

- **Eliminates dead code**: Removes computations that will never be used
- **Simplifies graphs**: Makes them easier to process
- **Reduces complexity**: Smaller graphs are faster

### Correctness

- **Handles unused variables**: Properly deals with lambda variables that don't appear
- **Maintains semantics**: Doesn't change meaning (when semantics exist)
- **Completes reduction**: Allows reduction to finish

## Implementation

### Pattern Matching

For each PRUNING move:
1. Find a node connected to a termination node `T`
2. Check which ports are connected to `T`
3. Apply the appropriate pruning rule

### Application

1. Remove the connection to `T`
2. Create new termination nodes or arrows as needed
3. Remove or simplify the original node
4. Connect remaining parts correctly

## Examples

### Example 1: Unused Application

Graph:
```
A a b c, T c
```

After pruning:
```
T a, T b
```

Both inputs are terminated since the application result is unused.

### Example 2: Unused Lambda Variable

Graph:
```
L a b c, T c
```

After pruning:
```
T a, T c, FRIN c
```

The lambda is pruned, its input is terminated, and a free input is created for the unused variable.

### Example 3: Unused Fan-Out Branch

Graph:
```
FO a b c, T b
```

After pruning:
```
Arrow a c
```

The unused branch is removed, and input connects directly to the used output.

## Relationship to Other Moves

### With BETA

- PRUNING cleans up after BETA reduction
- Removes unused parts created by beta reduction
- Completes the reduction process

### With DIST

- DIST can create unused branches
- PRUNING removes them
- Together they optimize reduction

### With COMB

- PRUNING creates Arrow nodes
- COMB eliminates them
- Together they simplify graphs

## Priority in Reduction

PRUNING moves typically have **low priority** in reduction algorithms:

1. **First**: FO-FOE distribution
2. **Second**: Other DIST moves
3. **Third**: BETA and FAN-IN moves
4. **Fourth**: PRUNING moves (cleanup)

This ensures computation happens before cleanup.

## Termination Nodes

Termination nodes (`T`) represent:
- **Unused variables**: Variables that don't appear in the body
- **Dead ends**: Computations that will never be used
- **Garbage**: Parts of the graph to be removed

## Free Port Nodes

After pruning, free ports may be created:
- **FRIN**: Free input node (middle.out)
- **FROUT**: Free output node (middle.in)

These represent ports that are no longer connected.

## References

- See [BETA Move](beta.md) for how PRUNING cleans up after beta reduction
- See [COMB Move](comb.md) for how PRUNING creates arrows for COMB
- See [Chemlambda System](../docs/chemlambda.md) for context

