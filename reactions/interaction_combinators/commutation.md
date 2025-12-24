# Commutation Rules (Interaction Combinators)

Commutation rules govern interactions between **different** symbols in Lafont's Interaction Combinators system. When two different symbols interact, they exchange connections rather than eliminating each other.

## Overview

Commutation occurs when two **different** symbols interact:
- **γ-δ**: Constructor and duplicator
- **γ-ε**: Constructor and eraser
- **δ-ε**: Duplicator and eraser

## Commutation Rules

### 1. γ-δ Commutation

When a constructor (γ) interacts with a duplicator (δ):

**What happens**: They exchange connections, creating a network that distributes the constructor over the duplicator's outputs.

**Visual representation**:
```
    γ              δ
   /|\            /|\
  a b c          d e f
     |            |
     +------------+
   (connected)
     
     becomes
     
  (network distributing γ over δ's outputs)
```

**Why important**:
- Enables distribution of construction over duplication
- Essential for encoding complex operations
- Foundation for expressiveness

### 2. γ-ε Commutation

When a constructor (γ) interacts with an eraser (ε):

**What happens**: The eraser eliminates the constructor, removing its structure.

**Visual representation**:
```
    γ              ε
   /|\             |
  a b c            |
     |             |
     +-------------+
   (connected)
     
     becomes
     
  ε  ε  ε
  a  b  c
```

**Why important**:
- Enables erasure of constructed structures
- Essential for garbage collection
- Allows elimination of unnecessary parts

### 3. δ-ε Commutation

When a duplicator (δ) interacts with an eraser (ε):

**What happens**: The eraser eliminates the duplicator, removing duplication.

**Visual representation**:
```
    δ              ε
   /|\             |
  a b c            |
     |             |
     +-------------+
   (connected)
     
     becomes
     
  ε  ε
  a  (b and c erased)
```

**Why important**:
- Enables erasure of duplicated structures
- Essential for cleanup
- Allows elimination of unnecessary duplication

## Key Properties

### Exchange vs Elimination

- **Commutation**: Different symbols exchange connections
- **Annihilation**: Same symbols eliminate each other
- **Both needed**: Commutation and annihilation together enable universality

### Locality

- **Local operation**: Only involves two connected cells
- **No global coordination**: Can happen independently
- **Parallelizable**: Many commutations can happen simultaneously

### Determinism

- **Unique result**: Same input always produces same output
- **Strong confluence**: Different reduction orders lead to same result
- **Predictable**: Behavior is well-defined

## Why Commutation Is Important

### Expressiveness

- **Enables encoding**: Can encode many interaction systems
- **Foundation**: Part of a minimal expressive system
- **Flexibility**: Handles different symbol combinations

### Distribution

- **Enables distribution**: Operations can be distributed over structures
- **Parallel processing**: Multiple operations can happen simultaneously
- **Efficiency**: More efficient than sequential processing

### Garbage Collection

- **Enables erasure**: Can eliminate unnecessary structures
- **Cleanup**: Removes parts that are no longer needed
- **Optimization**: Keeps graphs small and efficient

## Implementation

### Pattern Matching

Find in the graph:
- Two cells of different types connected by their principal ports
- Check which types they are (γ, δ, or ε)
- Apply the appropriate commutation rule

### Application

1. Identify the two different symbols
2. Determine their connection pattern
3. Apply the commutation rule
4. Rewire connections according to the rule
5. Remove or modify the original cells

## Examples

### Example 1: γ-δ Commutation

Initial graph:
```
γ(a, b, c) connected to δ(d, e, f)
```

After commutation:
```
Network distributing γ over δ's outputs
```

### Example 2: γ-ε Commutation

Initial graph:
```
γ(a, b, c) connected to ε
```

After commutation:
```
ε(a), ε(b), ε(c)
```

The constructor is erased, leaving erasers on its inputs.

## Relationship to Annihilation

Commutation and annihilation work together:

- **Commutation**: Different symbols exchange
- **Annihilation**: Same symbols eliminate
- **Both needed**: Together they enable all computation
- **Complementary**: Handle different cases

## References

- See [Annihilation Rules](annihilation.md) for interactions between same symbols
- See [Interaction Combinators](../docs/interaction_combinators.md) for context
- Lafont, Y. (1997). "Interaction Combinators." Information and Computation 137(1): 69-101.

