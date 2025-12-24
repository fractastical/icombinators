# Annihilation Rules (Interaction Combinators)

Annihilation rules govern interactions between **same** symbols in Lafont's Interaction Combinators system. When two identical symbols interact, they eliminate each other in specific ways.

## Overview

Annihilation occurs when two **same** symbols interact:
- **γ-γ**: Two constructors
- **δ-δ**: Two duplicators
- **ε-ε**: Two erasers

## Annihilation Rules

### 1. γ-γ Annihilation

When two constructors (γ) interact:

**What happens**: They eliminate each other, **exchanging** their auxiliary ports.

**Visual representation**:
```
    γ              γ
   /|\            /|\
  a b c          d e f
     |            |
     +------------+
   (connected)
     
     becomes
     
  (ports exchanged: a↔d, b↔e, c↔f)
```

**Key property**: The ports are **exchanged**, not just connected. This is different from δ-δ annihilation.

**Why important**:
- Enables swapping of structures
- Essential for encoding operations
- Foundation for expressiveness

### 2. δ-δ Annihilation

When two duplicators (δ) interact:

**What happens**: They eliminate each other, **duplicating** connections between their auxiliary ports.

**Visual representation**:
```
    δ              δ
   /|\            /|\
  a b c          d e f
     |            |
     +------------+
   (connected)
     
     becomes
     
  δ(a,d)  δ(b,e)  δ(c,f)
  (duplicated connections)
```

**Key property**: Connections are **duplicated**, creating new δ cells connecting corresponding ports.

**Why important**:
- Enables duplication of structures
- Essential for copying operations
- Foundation for replication

### 3. ε-ε Annihilation

When two erasers (ε) interact:

**What happens**: They eliminate each other completely.

**Visual representation**:
```
    ε              ε
     |             |
     +-------------+
   (connected)
     
     becomes
     
  (nothing - both eliminated)
```

**Why important**:
- Enables complete erasure
- Essential for cleanup
- Simplifies graphs

## Key Properties

### Exchange vs Duplication

- **γ-γ**: Exchanges ports (swaps structures)
- **δ-δ**: Duplicates connections (copies structures)
- **ε-ε**: Eliminates completely (removes structures)

### Locality

- **Local operation**: Only involves two connected cells
- **No global coordination**: Can happen independently
- **Parallelizable**: Many annihilations can happen simultaneously

### Determinism

- **Unique result**: Same input always produces same output
- **Strong confluence**: Different reduction orders lead to same result
- **Predictable**: Behavior is well-defined

## Why Annihilation Is Important

### Expressiveness

- **Enables encoding**: Can encode many interaction systems
- **Foundation**: Part of a minimal expressive system
- **Flexibility**: Handles same-symbol interactions

### Duplication and Exchange

- **δ-δ enables duplication**: Can copy structures
- **γ-γ enables exchange**: Can swap structures
- **Essential operations**: Needed for computation

### Cleanup

- **ε-ε enables erasure**: Can remove structures completely
- **Garbage collection**: Eliminates unnecessary parts
- **Optimization**: Keeps graphs small

## Implementation

### Pattern Matching

Find in the graph:
- Two cells of the **same** type connected by their principal ports
- Check which type they are (γ, δ, or ε)
- Apply the appropriate annihilation rule

### Application

1. Identify the two identical symbols
2. Determine their connection pattern
3. Apply the annihilation rule:
   - **γ-γ**: Exchange auxiliary ports
   - **δ-δ**: Duplicate connections between ports
   - **ε-ε**: Remove both cells
4. Rewire connections according to the rule

## Examples

### Example 1: γ-γ Annihilation

Initial graph:
```
γ(a, b, c) connected to γ(d, e, f)
```

After annihilation:
```
Ports exchanged: a connected to d, b to e, c to f
```

### Example 2: δ-δ Annihilation

Initial graph:
```
δ(a, b, c) connected to δ(d, e, f)
```

After annihilation:
```
δ(a, d), δ(b, e), δ(c, f)
```

New δ cells connect corresponding ports.

### Example 3: ε-ε Annihilation

Initial graph:
```
ε connected to ε
```

After annihilation:
```
(nothing - both eliminated)
```

## Relationship to Commutation

Annihilation and commutation work together:

- **Annihilation**: Same symbols eliminate
- **Commutation**: Different symbols exchange
- **Both needed**: Together they enable all computation
- **Complementary**: Handle different cases

## Non-Terminating Example

There exist graphs that reduce to themselves:

```
δ(ε, x) = γ(x, ε)
```

This creates a cycle that reduces to itself in 4 steps, demonstrating that not all reductions terminate.

## References

- See [Commutation Rules](commutation.md) for interactions between different symbols
- See [Interaction Combinators](../docs/interaction_combinators.md) for context
- Lafont, Y. (1997). "Interaction Combinators." Information and Computation 137(1): 69-101.

