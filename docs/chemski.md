# chemSKI System

chemSKI is a purely local graph rewrite system for the SKI combinator calculus, developed in chemlambda style. It provides an alternative to lambda calculus for graph rewriting, using combinatory logic instead.

## Motivation

German Kruszewski posed the problem of creating a chemlambda-style graph rewriting version of Combinatory Chemistry. chemSKI addresses this by:

- Providing local graph rewrites for SKI combinators
- Enabling conservative rewrites through tokens
- Showing universality through SKI combinators
- Demonstrating cost estimation of computation

## Basic Components

### SKI Combinator Nodes

1. **S (Substitution)** - Arity 3
   - Takes three arguments: S a b c
   - Reduces to: (a c) (b c)
   - Most complex combinator

2. **K (Constant)** - Arity 2
   - Takes two arguments: K a b
   - Reduces to: a
   - Erases second argument

3. **I (Identity)** - Arity 1
   - Takes one argument: I a
   - Reduces to: a
   - Simplest combinator

### Token Molecules

Small two-node molecules used to make rewrites conservative:
- **I-A**: Identity-Application token
- **S-A**: Substitution-Application token
- **S-K**: Substitution-Constant token
- And others...

Tokens enable:
- Conservative rewrites (preserve node and edge counts)
- Cost estimation of computation
- Resource management

## Key Reactions

### S Combinator Reduction

```
S a b c → (a c) (b c)
```

**What it does**: Substitutes the third argument into both the first and second arguments, then applies them.

**Graph representation**:
```
    S
   /|\
  a b c
```

becomes a graph representing `(a c) (b c)`.

**Why important**:
- Core of combinatory logic
- Enables all computation
- Most complex reduction

### K Combinator Reduction

```
K a b → a
```

**What it does**: Returns the first argument, discarding the second.

**Graph representation**:
```
    K
   /|\
  a b
```

becomes just `a`.

**Why important**:
- Enables erasure
- Simplest non-trivial combinator
- Foundation for other combinators

### I Combinator Reduction

```
I a → a
```

**What it does**: Returns the argument unchanged.

**Graph representation**:
```
    I
    |
    a
```

becomes `a`.

**Why important**:
- Simplest combinator
- Identity operation
- Can be defined as S K K

## Token-Based Conservative Rewrites

### Problem

Standard graph rewrites are not conservative:
- Nodes and edges can be created or destroyed
- Makes cost estimation difficult
- Doesn't preserve resources

### Solution: Tokens

Tokens are small molecules that:
- Are created/destroyed to balance rewrites
- Make rewrites conservative
- Enable cost tracking

### Example

A rewrite that would create nodes instead:
- Creates token molecules
- Tokens balance the rewrite
- Total nodes + tokens remains constant

## Synthesis Rewrites

### Building Larger Graphs

In Combinatory Chemistry, reactions can build larger graphs:
```
A + B → A B
```

chemSKI achieves this through **synthesis rewrites**:
- Insert/glue token molecules to edges
- Build larger structures from smaller ones
- Enable graph construction

### Token Insertion

- Tokens can be inserted into edges
- Create new connections
- Build complex structures

## Comparison with Combinatory Chemistry

| Property | Combinatory Chemistry | chemSKI |
|----------|----------------------|---------|
| Conservative | Yes | Yes (with tokens) |
| Local rewrites | No | Yes |
| Graph building | Direct | Via synthesis |
| Duplication | Delegated | Via tokens |
| Cost tracking | Limited | Via tokens |

## Advantages

### Local Rewrites

- All rewrites are local
- No global coordination needed
- Enables distributed computation

### Conservative with Tokens

- Rewrites can be made conservative
- Enables cost estimation
- Resource management

### Expressiveness

- SKI combinators demonstrate significant computational expressiveness
- Can encode many computations
- Alternative to lambda calculus

## Implementation

chemSKI can be implemented as:
- **Artificial chemistry**: Random reactions
- **Virtual machine**: Deterministic reduction
- **Distributed system**: Local, asynchronous

## Cost Estimation

Tokens enable cost estimation:
- Each rewrite has a token cost
- Can track computational resources
- Enables optimization

## Examples

### Simple Reduction

```
S K K a
```

Reduces to:
```
K a (K a)
```

Then:
```
a
```

### Complex Reduction

```
S (K a) (K b) c
```

Reduces through multiple steps to:
```
a b
```

## References

- Buliga, M. (2023). "chemSKI with tokens: world building and economy in the SKI universe." arXiv:2306.00938
- See [SKI Combinator Reactions](reactions/chemski/ski.md) for detailed reactions
- [GitHub: mbuliga/chemski](https://github.com/mbuliga/chemski)

