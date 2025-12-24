# Interaction Combinators (Lafont's System)

Yves Lafont's Interaction Combinators provide a minimal system for graph rewriting computation. With only three symbols and six rules, they can encode many interaction systems, demonstrating significant expressiveness for graph rewriting.

## Basic Components

### Three Symbols

1. **γ (gamma)** - Constructor, arity 2
   - Principal port + 2 auxiliary ports
   - Used for building structures

2. **δ (delta)** - Duplicator, arity 2
   - Principal port + 2 auxiliary ports
   - Used for duplicating structures

3. **ε (epsilon)** - Eraser, arity 0
   - Principal port only
   - Used for erasing structures

### Interaction Rules

Interaction combinators have exactly **six interaction rules**, divided into two types:

#### Commutation Rules (Different Symbols)

When two **different** symbols interact, they exchange connections:

1. **γ-δ commutation**: γ and δ interact by exchanging their connections
2. **γ-ε commutation**: γ and ε interact, ε erases γ's structure
3. **δ-ε commutation**: δ and ε interact, ε erases δ's structure

#### Annihilation Rules (Same Symbols)

When two **same** symbols interact, they eliminate each other:

1. **γ-γ annihilation**: Two γ cells eliminate each other, exchanging ports
2. **δ-δ annihilation**: Two δ cells eliminate each other, duplicating connections
3. **ε-ε annihilation**: Two ε cells eliminate each other

## Key Properties

### Expressiveness

**Lafont's Result**: Interaction combinators demonstrate significant expressiveness for encoding interaction systems.

This means:
- Many interaction systems can be encoded using interaction combinators
- Lambda calculus can be encoded, establishing computational expressiveness
- The encoding preserves reduction behavior for confluent systems
- This demonstrates significant expressiveness at the graph rewriting level

### Strong Confluence

Interaction nets have the **strong confluence property**:
- If a net can reduce in two different ways, both reductions lead to the same result
- This ensures determinism despite parallel execution
- The reduction is unique up to the order of independent steps

### Locality

- Each interaction involves only two cells connected by their principal ports
- No global coordination needed
- Enables massive parallelism

## Visual Representation

### Commutation Example: γ-δ

```
    γ          δ
   /|\        /|\
  a b c      d e f
     |        |
     +--------+
     
     becomes
     
  (network with exchanged connections)
```

### Annihilation Example: δ-δ

```
    δ          δ
   /|\        /|\
  a b c      d e f
     |        |
     +--------+
     
     becomes
     
  δ(a,d)  δ(b,e)  δ(c,f)
  (duplicated connections)
```

## Relationship to Lambda Calculus

Interaction combinators can encode lambda calculus:
- Lambda abstraction → networks of γ, δ, ε
- Beta reduction → sequences of interactions
- Variable binding → duplication and erasure patterns

However, interaction combinators are more general:
- Not limited to lambda calculus
- Can encode many interaction systems
- Focus on structure, not semantics

## Significance

### Minimal Expressive System

With only **3 symbols** and **6 rules**, interaction combinators are:
- A simple and expressive graph rewriting system
- A foundation for understanding computation at the structural level
- Demonstration that computation can emerge from simple local rules

### Graph Rewriting Expressiveness

Lafont's result demonstrates:
- Significant expressiveness for encoding interaction systems
- Ability to encode lambda calculus and related systems
- Shows that graph rewriting can capture important computational patterns

### Foundation for Molecular Computing

Interaction combinators inspired:
- Buliga's directed interaction combinators
- Chemlambda's local reduction approach
- Understanding of how computation can emerge from chemistry

## Limitations

### Sequential Computation

Some interaction systems (like Turing machines) are inherently sequential:
- They can be encoded but remain sequential
- True parallelism requires different interaction patterns

### No Non-Determinism

Interaction combinators are deterministic:
- Strong confluence ensures unique results
- Cannot directly encode non-deterministic computation
- Would need extensions (like amb agent) for non-determinism

## References

- Lafont, Y. (1997). "Interaction Combinators." Information and Computation 137(1): 69-101.
- See [Commutation Rules](reactions/interaction_combinators/commutation.md) for detailed commutation reactions
- See [Annihilation Rules](reactions/interaction_combinators/annihilation.md) for detailed annihilation reactions
- See [Directed Interaction Combinators](directed_interaction_combinators.md) for Buliga's adaptation

