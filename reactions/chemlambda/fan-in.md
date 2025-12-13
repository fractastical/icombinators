# FAN-IN Move

The FAN-IN move is similar to the BETA move but operates on fan-in and fan-out nodes instead of lambda and application nodes.

## Formal Notation

```
FI 1 4 c, FOE c 2 3 → Arrow 1 3, Arrow 4 2
```

In mol format:
- Input: Fan-In node `FI` with ports `1` (left.in), `4` (right.in), `c` (middle.out)
- Input: Fan-Out-Extra node `FOE` with ports `c` (middle.in), `2` (left.out), `3` (right.out)
- Output: Two Arrow nodes connecting `1→3` and `4→2`

## Visual Representation

### Before (Left-hand side)
```
    FI            FOE
   /|\            /|\
  1 4 c          c 2 3
     |            |
     +------------+
   (connected)
```

### After (Right-hand side)
```
  Arrow        Arrow
   1 3          4 2
```

## What It Does

The FAN-IN move combines fan-in and fan-out operations:

- When a Fan-In node `FI` combines two inputs
- And a Fan-Out-Extra node `FOE` splits an output
- They interact to route the inputs to the outputs
- Input `1` goes to output `3`
- Input `4` goes to output `2`

## Why It's Important

### Parallel Operations

- **Handles fan operations**: Essential for parallel reduction
- **Works alongside BETA**: Enables complex computations
- **Local operation**: No global coordination needed
- **Distribution**: Enables distribution of computations

### Key Properties

1. **Local**: Only involves two connected nodes
2. **Deterministic**: Always produces the same result
3. **Parallel**: Many FAN-IN moves can happen at once
4. **Complementary**: Works with BETA for full computation

## Implementation

### Pattern Matching

Find in the graph:
- An `FI` node with its `middle.out` port connected to
- An `FOE` node's `middle.in` port

### Application

1. Remove the connection between `FI`'s `middle.out` and `FOE`'s `middle.in`
2. Create Arrow from `FI`'s `left.in` to `FOE`'s `right.out`
3. Create Arrow from `FI`'s `right.in` to `FOE`'s `left.out`
4. Remove the `FI` and `FOE` nodes (or mark them for removal)

### COMB Cycle

After FAN-IN, a COMB cycle typically follows to eliminate Arrow nodes.

## Example

### Simple Fan Operation

Graph representation:
```
FI a b c, FOE c d e
```

After FAN-IN move:
```
Arrow a e, Arrow b d
```

After COMB cycle:
```
a connected to e, b connected to d
```

## Relationship to BETA

FAN-IN is structurally similar to BETA:

- **Same pattern**: Two nodes connected through one port
- **Same result**: Two Arrow nodes
- **Different nodes**: Uses FI/FOE instead of L/A
- **Same purpose**: Enables computation

## Use Cases

### Parallel Reduction

- Enables parallel processing of multiple inputs
- Works with DIST moves for complex distributions
- Essential for efficient reduction

### Fan Operations

- Handles fan-in and fan-out operations
- Enables duplication and combination
- Critical for non-linear computation

## References

- See [BETA Move](beta.md) for comparison
- See [DIST Moves](dist.md) for related distribution operations
- See [Chemlambda System](../docs/chemlambda.md) for context

