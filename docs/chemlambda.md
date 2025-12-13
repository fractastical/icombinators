# Chemlambda System

Chemlambda is a graph rewriting system derived from graphic lambda calculus that can be seen as a simple model of chemical or biological computing. It enables purely local, distributed computation without global coordination.

## Basic Components

### Node Types

Chemlambda molecules are built from 7 elementary node types:

1. **L (Lambda)** - Represents lambda abstraction
   - Ports: `middle.in`, `left.out`, `right.out`
   - Inspired from lambda calculus abstraction

2. **A (Application)** - Represents function application
   - Ports: `left.in`, `right.in`, `middle.out`
   - Inspired from lambda calculus application

3. **FI (Fan-In)** - No direct lambda calculus correspondent
   - Ports: `left.in`, `right.in`, `middle.out`
   - Combines two inputs into one output

4. **FO (Fan-Out)** - No direct lambda calculus correspondent
   - Ports: `middle.in`, `left.out`, `right.out`
   - Splits one input into two outputs

5. **FOE (Extra Fan-Out)** - No direct lambda calculus correspondent
   - Ports: `middle.in`, `left.out`, `right.out`
   - Additional fan-out node for distribution moves

6. **Arrow** - Simple connector node
   - Ports: `middle.in`, `middle.out`
   - Used for intermediate connections in reactions

7. **T (Termination)** - Represents unused variables
   - Ports: `middle.in`
   - Used for variables that don't appear in the body

### Port System

Each node has ports with two properties:
- **Type**: `in` or `out` (direction of information flow)
- **Position**: `middle`, `left`, or `right` (spatial arrangement)

Ports are connected by **edges** (wires) that carry information between nodes.

### Graph Representation: .mol Format

Chemlambda graphs are represented in `.mol` file format:

```
L a b c
A d e f
FO g h i
...
```

Where:
- Each line represents a node
- Letters represent port variables
- Port variables appear exactly twice (connecting two ports) or once (free port)

### Free Port Nodes

- **FRIN** (`middle.out`) - Free input node for edges with free source
- **FROUT** (`middle.in`) - Free output node for edges with free target

## Reaction Families

Chemlambda reactions (moves) are organized into families:

### 1. BETA and FAN-IN Family

These are the core computational reactions.

#### BETA Move
```
L 1 2 c, A c 4 3 → Arrow 1 3, Arrow 4 2
```

**What it does**: Implements lambda calculus beta reduction. When a lambda abstraction (L) is applied to an argument (A), it substitutes the argument into the lambda body.

**Why important**: 
- Core mechanism for function application
- Enables lambda calculus computation
- Foundation for all higher-level computation

**Visual representation**:
```
    L          A
   /|\        /|\
  1 2 c      c 4 3
     |        |
     +--------+
     
     becomes
     
  Arrow    Arrow
   1 3      4 2
```

#### FAN-IN Move
```
FI 1 4 c, FOE c 2 3 → Arrow 1 3, Arrow 4 2
```

**What it does**: Combines fan-in and fan-out-extra nodes, similar to beta reduction but for fan operations.

**Why important**: 
- Handles fan operations in parallel reduction
- Enables distribution of computations
- Works alongside beta reduction

### 2. DIST Family (Distribution Moves)

These moves distribute operations over fan-out nodes, enabling parallel reduction.

#### FO-FOE Distribution
```
FO 1 2 c, FOE c 3 4 → FI j i 2, FO k i 3, FO l j 4, FOE 1 k l
```

**What it does**: Distributes fan-out over fan-out-extra, creating multiple fan-out nodes.

**Why important**:
- Enables parallel duplication of computations
- Critical for efficient reduction
- Allows multiple paths to be processed simultaneously

#### FI-FO Distribution
```
FI 1 4 c, FO c 2 3 → FO 1 i j, FI i k 2, FI j l 3, FO 4 k l
```

**What it does**: Distributes fan-in over fan-out, creating a network of fan operations.

**Why important**:
- Enables complex parallel operations
- Handles multiple inputs and outputs
- Essential for non-linear computation

#### L-FO/FOE Distribution
```
L 1 2 c, FOE c 3 4 → FI j i 2, L k i 3, L l j 4, FOE 1 k l
L 1 2 c, FO c 3 4 → FI j i 2, L k i 3, L l j 4, FOE 1 k l
```

**What it does**: Distributes lambda abstraction over fan-out, duplicating the lambda.

**Why important**:
- Enables parallel lambda reductions
- Handles cases where lambda is used multiple times
- Critical for efficient computation

#### A-FO/FOE Distribution
```
A 1 4 c, FOE c 2 3 → FOE 1 i j, A i k 2, A j l 3, FOE 4 k l
A 1 4 c, FO c 2 3 → FOE 1 i j, A i k 2, A j l 3, FOE 4 k l
```

**What it does**: Distributes application over fan-out, creating multiple applications.

**Why important**:
- Enables parallel application reductions
- Handles multiple uses of an argument
- Essential for efficient computation

### 3. PRUNING Family

These moves handle unused variables and garbage collection.

#### Application Pruning
```
A 1 2 3, T 3 → T 1, T 2
FI 1 2 3, T 3 → T 1, T 2
```

**What it does**: When an application or fan-in is connected to a termination node, both inputs are terminated.

**Why important**:
- Garbage collection for unused computations
- Prevents unnecessary computation
- Cleans up dead branches

#### Lambda Pruning
```
L 1 2 3, T 3 → T 1, T c, FRIN c
```

**What it does**: When a lambda's bound variable is unused, the lambda is pruned and a free input is created.

**Why important**:
- Handles unused lambda variables
- Enables optimization
- Cleans up unnecessary abstractions

#### Fan-Out Pruning
```
FO 1 2 3, T 2 → Arrow 1 3
FOE 1 2 3, T 2 → Arrow 1 3
FO 1 2 3, T 3 → Arrow 1 2
FOE 1 2 3, T 3 → Arrow 1 2
```

**What it does**: When one output of a fan-out is unused, it's eliminated and the input connects directly to the used output.

**Why important**:
- Optimizes fan-out operations
- Removes unnecessary duplication
- Simplifies the graph

### 4. COMB Move

#### COMB (Combination)
```
M 1, Arrow 1 2 → M 2
```

**What it does**: Eliminates Arrow nodes by connecting the node directly to its target.

**Why important**:
- Simplifies intermediate representations
- Removes temporary connections
- Cleans up after other moves
- Applied in a "COMB cycle" until no more arrows can be eliminated

**COMB Cycle**: Rapidly applies COMB moves wherever possible until no more can be applied.

## Reduction Algorithm

The chemlambda reduction algorithm:

1. **Identify patterns**: Find all locations where moves can apply
2. **Prioritize moves**: 
   - First: FO-FOE moves
   - Second: DIST moves with free nodes
   - Third: BETA and FAN-IN moves
   - Fourth: PRUNING moves
3. **Apply moves**: Either deterministically or randomly (coin flip)
4. **COMB cycle**: Eliminate all possible Arrow nodes
5. **Repeat**: Until no more moves apply or termination condition met

### Properties

- **Local**: Each move involves only a small, bounded part of the graph
- **Geometrical**: Results don't depend on node numbering or naming
- **Asynchronous**: Moves can be applied in parallel
- **Decentralized**: No global coordination needed

## Key Differences from Lambda Calculus

1. **No eta reduction**: Pure lambda beta, no extensionality
2. **Intermediate graphs**: May not correspond to lambda terms
3. **Signal transduction**: Uses signal-like propagation instead of variable passing
4. **Massively parallel**: Many reductions happen simultaneously
5. **No correctness**: All graphs are valid, not just those from lambda terms

## Applications

- **Lambda calculus reduction**: Can reduce lambda terms
- **Parallel computation**: Natural parallelism through DIST moves
- **Decentralized systems**: No central control needed
- **Molecular computing**: Potential implementation in real chemistry
- **Artificial life**: Quine graphs exhibit life-like properties

## References

- See [BETA Move](reactions/chemlambda/beta.md) for detailed BETA reaction
- See [DIST Moves](reactions/chemlambda/dist.md) for detailed distribution reactions
- See [PRUNING Moves](reactions/chemlambda/pruning.md) for detailed pruning reactions
- See [COMB Move](reactions/chemlambda/comb.md) for detailed combination reaction

