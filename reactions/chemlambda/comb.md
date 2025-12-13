# COMB Move

The COMB move eliminates Arrow nodes by connecting nodes directly, simplifying intermediate representations created by other moves.

## Formal Notation

```
M 1, Arrow 1 2 → M 2
```

Where `M` is any node with port `1` connected to Arrow's input port, and Arrow's output port `2` connects to the rest of the graph.

## Visual Representation

### Before
```
    M            Arrow
    1------------1 2
                  |
                  +---> (rest of graph)
```

### After
```
    M
    2---> (rest of graph)
```

## What It Does

The COMB move eliminates Arrow nodes:

- **Removes intermediate connections**: Arrow nodes are temporary
- **Direct connection**: Connects nodes directly
- **Simplifies graph**: Reduces graph complexity
- **Cleanup**: Removes artifacts from other moves

## Why It's Important

### Simplification

- **Removes temporary nodes**: Arrow nodes are created by BETA and FAN-IN
- **Simplifies graphs**: Makes them easier to process
- **Reduces complexity**: Fewer nodes to manage

### Cleanup

- **After BETA**: BETA creates Arrow nodes that need cleanup
- **After FAN-IN**: FAN-IN also creates Arrow nodes
- **After PRUNING**: PRUNING can create Arrow nodes
- **Final step**: COMB cleans up all these arrows

### Efficiency

- **Smaller graphs**: Fewer nodes means faster processing
- **Direct connections**: More efficient than going through Arrow nodes
- **Optimization**: Part of the optimization process

## COMB Cycle

The COMB move is typically applied in a **COMB cycle**:

1. Find all Arrow nodes that can be eliminated
2. Apply COMB moves to eliminate them
3. Repeat until no more Arrow nodes can be eliminated

### Why a Cycle?

- **Cascading**: Eliminating one Arrow may enable eliminating another
- **Complete cleanup**: Ensures all possible Arrows are eliminated
- **Efficiency**: Single pass may not catch all cases

### Termination

The cycle terminates when:
- No Arrow nodes remain, OR
- Remaining Arrow nodes form cycles (cannot be eliminated)

Arrow cycles represent actual cycles in the computation, not just temporary connections.

## Implementation

### Pattern Matching

Find in the graph:
- An Arrow node with its `middle.in` connected to some node `M`
- The Arrow's `middle.out` connects to the rest of the graph

### Application

1. Remove the Arrow node
2. Connect `M`'s port directly to where Arrow's output was connected
3. Update all references

### Cycle Algorithm

```
while there are Arrow nodes that can be eliminated:
    for each Arrow node:
        if it can be eliminated:
            apply COMB move
```

## Examples

### Example 1: After BETA

After BETA move:
```
Arrow 1 3, Arrow 4 2
```

After COMB cycle:
- If `Arrow 1 3` connects node `1` to node `3`: Connect `1` directly to `3`
- If `Arrow 4 2` connects node `4` to node `2`: Connect `4` directly to `2`
- Remove both Arrow nodes

### Example 2: Cascading Elimination

Graph:
```
A a b c, Arrow c d, Arrow d e
```

After first COMB:
```
A a b d, Arrow d e
```

After second COMB:
```
A a b e
```

Both Arrows eliminated.

### Example 3: Arrow Cycle

Graph:
```
Arrow a b, Arrow b a
```

These Arrows form a cycle and cannot be eliminated by COMB. This represents an actual cycle in the computation.

## Relationship to Other Moves

### With BETA

- **BETA creates Arrows**: BETA move produces Arrow nodes
- **COMB eliminates them**: COMB cycle cleans them up
- **Together**: Complete the beta reduction

### With FAN-IN

- **FAN-IN creates Arrows**: FAN-IN move also produces Arrow nodes
- **COMB eliminates them**: Same cleanup process
- **Together**: Complete the fan-in operation

### With PRUNING

- **PRUNING can create Arrows**: Some pruning moves create Arrow nodes
- **COMB eliminates them**: Cleanup after pruning
- **Together**: Complete the pruning process

## Arrow Nodes

Arrow nodes are **temporary**:
- Created by BETA, FAN-IN, and some PRUNING moves
- Represent intermediate connections
- Should be eliminated by COMB
- If they remain, they form cycles (which are meaningful)

## When Arrows Remain

Arrow nodes that cannot be eliminated represent:
- **Cycles**: Actual cycles in the computation
- **Loops**: Computation that loops back on itself
- **Fixed points**: Self-referential structures

These are meaningful structures, not just artifacts.

## Priority in Reduction

COMB moves are applied **after** other moves:

1. Apply BETA, FAN-IN, DIST, PRUNING moves
2. Then apply COMB cycle
3. Repeat until no more moves apply

This ensures cleanup happens after computation.

## Efficiency

COMB cycles are efficient because:
- **Local operation**: Each COMB move is local
- **Parallelizable**: Multiple COMB moves can happen simultaneously
- **Fast**: Simple pattern matching and connection
- **Complete**: Cycle ensures all possible eliminations

## References

- See [BETA Move](beta.md) for how BETA creates Arrow nodes
- See [FAN-IN Move](fan-in.md) for how FAN-IN creates Arrow nodes
- See [PRUNING Moves](pruning.md) for how PRUNING can create Arrow nodes
- See [Chemlambda System](../docs/chemlambda.md) for context

