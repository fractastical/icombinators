# BETA Move

The BETA move is the core computational mechanism of chemlambda, implementing lambda calculus beta reduction in a purely local, graph-rewriting form.

## Formal Notation

```
L 1 2 c, A c 4 3 → Arrow 1 3, Arrow 4 2
```

In mol format:
- Input: Lambda node `L` with ports `1` (middle.in), `2` (left.out), `c` (right.out)
- Input: Application node `A` with ports `c` (left.in), `4` (right.in), `3` (middle.out)
- Output: Two Arrow nodes connecting `1→3` and `4→2`

## Visual Representation

### Before (Left-hand side)
```
    L              A
   /|\            /|\
  1 2 c          c 4 3
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

The BETA move implements **lambda calculus beta reduction**:

- When a lambda abstraction `L` is applied to an argument `A`
- The lambda's bound variable (port `c`) is connected to the argument
- The lambda body (port `2`) connects to the application result (port `3`)
- The argument (port `4`) connects to where the variable was used (port `1`)

This is equivalent to the lambda calculus reduction:
```
(λx.M) N → M[N/x]
```

Where:
- `λx.M` is the lambda (L node)
- `N` is the argument (A node)
- `M[N/x]` is substitution (the result)

## Why It's Important

### Core Computational Mechanism

- **Enables function application**: Without BETA, no computation can happen
- **Foundation for lambda calculus**: All lambda calculus computation relies on beta reduction
- **Local operation**: No global coordination needed
- **Parallelizable**: Many BETA moves can happen simultaneously

### Key Properties

1. **Local**: Only involves two connected nodes
2. **Deterministic**: Always produces the same result
3. **Reversible**: Can be undone (though not typically done)
4. **Parallel**: Many BETA moves can happen at once

## Implementation

### Pattern Matching

Find in the graph:
- An `L` node with its `right.out` port connected to
- An `A` node's `left.in` port

### Application

1. Remove the connection between `L`'s `right.out` and `A`'s `left.in`
2. Create Arrow from `L`'s `middle.in` to `A`'s `middle.out`
3. Create Arrow from `A`'s `right.in` to `L`'s `left.out`
4. Remove the `L` and `A` nodes (or mark them for removal)

### COMB Cycle

After BETA, a COMB cycle typically follows to eliminate Arrow nodes:
- Arrow nodes are eliminated by connecting their endpoints directly
- Continues until no more Arrow eliminations are possible

## Example

### Lambda Term: (λx.x) y

Graph representation:
```
L a b x, A x y c
```

After BETA move:
```
Arrow a c, Arrow y b
```

After COMB cycle:
```
y (connected to where L's left.out was)
```

Result: `y` (identity function applied to `y`)

## Relationship to Lambda Calculus

The BETA move is a **graphical version** of beta reduction:

- **Lambda abstraction**: L node
- **Application**: A node
- **Variable binding**: Connection through port `c`
- **Substitution**: Rewiring through Arrow nodes

### Differences

- **No variable names**: Uses port connections instead
- **Graphical**: Works on graph structure, not syntax
- **Parallel**: Many reductions can happen simultaneously
- **Local**: No need to find all occurrences of variable

## Variants

### FAN-IN Move

Similar structure but for fan operations:
```
FI 1 4 c, FOE c 2 3 → Arrow 1 3, Arrow 4 2
```

Works the same way but with Fan-In and Fan-Out-Extra nodes instead of Lambda and Application.

## References

- See [Chemlambda System](../docs/chemlambda.md) for context
- See [COMB Move](comb.md) for cleanup after BETA
- Buliga, M. (2015). "Molecular computers."

