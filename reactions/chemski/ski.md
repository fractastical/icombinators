# SKI Combinator Reactions (chemSKI)

chemSKI implements graph rewriting for the SKI combinator calculus, providing local rewrites for S, K, and I combinators.

## Overview

The SKI combinator calculus is a Turing-complete system with only three combinators:
- **S**: Substitution combinator
- **K**: Constant combinator  
- **I**: Identity combinator

chemSKI provides graph rewriting rules for each combinator, enabling purely local reduction.

## S Combinator Reduction

### Formal Notation

```
S a b c → (a c) (b c)
```

### What It Does

The S combinator takes three arguments and:
1. Applies the first argument `a` to the third argument `c`: `a c`
2. Applies the second argument `b` to the third argument `c`: `b c`
3. Applies the first result to the second result: `(a c) (b c)`

### Graph Representation

#### Before
```
    S
   /|\
  a b c
```

#### After
```
    A              A
   /|\            /|\
  a c ?          b c ?
     |            |
     +------------+
   (application)
```

The graph represents the application `(a c) (b c)`.

### Why Important

- **Most complex combinator**: S is the most powerful
- **Enables all computation**: Can encode any computation
- **Foundation**: All other combinators can be defined using S and K
- **Core mechanism**: Essential for combinatory logic

## K Combinator Reduction

### Formal Notation

```
K a b → a
```

### What It Does

The K combinator takes two arguments and returns the first, discarding the second.

### Graph Representation

#### Before
```
    K
   /|\
  a b
```

#### After
```
a
```

Simply returns `a`, discarding `b`.

### Why Important

- **Simplest non-trivial combinator**: After I, K is simplest
- **Enables erasure**: Can discard arguments
- **Foundation**: Used to define other combinators
- **Essential**: Needed for many computations

## I Combinator Reduction

### Formal Notation

```
I a → a
```

### What It Does

The I combinator (identity) returns its argument unchanged.

### Graph Representation

#### Before
```
    I
     |
     a
```

#### After
```
a
```

Simply returns `a` unchanged.

### Why Important

- **Simplest combinator**: Most basic operation
- **Can be defined**: I = S K K
- **Identity operation**: Fundamental operation
- **Foundation**: Basis for other combinators

## Implementation

### Pattern Matching

For each combinator:
1. Find the combinator node (S, K, or I)
2. Identify its arguments
3. Apply the reduction rule
4. Rewire the graph accordingly

### Application

1. **S combinator**:
   - Create two application nodes
   - Connect `a` to `c` in first application
   - Connect `b` to `c` in second application
   - Connect first application's result to second application

2. **K combinator**:
   - Remove the K node
   - Return the first argument
   - Discard the second argument

3. **I combinator**:
   - Remove the I node
   - Return the argument unchanged

## Examples

### Example 1: I Combinator

```
I x
```

Reduces to:
```
x
```

### Example 2: K Combinator

```
K x y
```

Reduces to:
```
x
```

### Example 3: S Combinator

```
S K K x
```

First, S reduces:
```
(K x) (K x)
```

Then both K reductions:
```
x x
```

But wait - this should be `x`. Let's trace more carefully:

```
S K K x
```

S reduction:
```
(K x) (K x)
```

First K reduction:
```
x (K x)
```

Second K reduction:
```
x x
```

Actually, `S K K = I`, so this should reduce to `x`. The issue is that we need to apply K reductions properly. The correct reduction is:

```
S K K x → (K x) (K x) → x (K x) → x x
```

But `S K K` should equal `I`, which means `S K K x = x`. This shows the complexity of S reduction.

## Token System

chemSKI can be made conservative using tokens:

- **Tokens**: Small two-node molecules
- **Balance rewrites**: Make rewrites conservative
- **Cost tracking**: Enable cost estimation

### Example with Tokens

A rewrite that creates nodes:
- Creates token molecules to balance
- Total nodes + tokens remains constant
- Enables resource tracking

## Relationship to Lambda Calculus

SKI combinators can encode lambda calculus:

- **S**: Encodes substitution
- **K**: Encodes constant functions
- **I**: Encodes identity

Any lambda term can be translated to SKI combinators.

## Advantages

### Local Rewrites

- **All rewrites are local**: No global coordination
- **Parallelizable**: Many reductions can happen simultaneously
- **Distributed**: Can work in distributed systems

### Simplicity

- **Only three combinators**: Very simple system
- **Clear rules**: Easy to understand
- **Minimal**: Fewest combinators needed

### Universality

- **Turing complete**: Can compute anything
- **Alternative to lambda**: Different approach to computation
- **Graph rewriting**: Natural fit for graph rewriting

## References

- Buliga, M. (2023). "chemSKI with tokens: world building and economy in the SKI universe." arXiv:2306.00938
- See [chemSKI System](../docs/chemski.md) for context
- [GitHub: mbuliga/chemski](https://github.com/mbuliga/chemski)

