# Marius Buliga's Work on Interaction Combinators and Chemlambda

A comprehensive documentation and implementation of Marius Buliga's research on graph rewriting systems, interaction combinators, and chemlambda artificial chemistry.

## Overview

This repository documents and implements the key contributions of Marius Buliga to the field of graph rewriting systems and artificial chemistry, including:

1. **Chemlambda** - A graph rewriting system inspired by lambda calculus that enables purely local, distributed computation
2. **Interaction Combinators** - Based on Yves Lafont's foundational work, adapted for directed graphs
3. **Directed Interaction Combinators** - Buliga's adaptation enabling artificial life properties
4. **chemSKI** - A graph rewriting system for SKI combinator calculus
5. **Quine Graphs** - Self-replicating graphs that exhibit metabolism, replication, and death

## Table of Contents

- [Introduction and Background](docs/introduction.md)
- [Chemlambda System](docs/chemlambda.md)
- [Interaction Combinators](docs/interaction_combinators.md)
- [Directed Interaction Combinators](docs/directed_interaction_combinators.md)
- [chemSKI System](docs/chemski.md)
- [Quine Graphs](docs/quine_graphs.md)
- [Applications and Significance](docs/applications.md)

## Key Reactions

### Chemlambda Reactions
- [BETA Move](reactions/chemlambda/beta.md) - Core lambda calculus beta reduction
- [FAN-IN Move](reactions/chemlambda/fan-in.md) - Fan-in operations
- [DIST Moves](reactions/chemlambda/dist.md) - Distribution operations for parallel reduction
- [PRUNING Moves](reactions/chemlambda/pruning.md) - Garbage collection and termination
- [COMB Move](reactions/chemlambda/comb.md) - Arrow elimination

### Interaction Combinators Reactions
- [Commutation Rules](reactions/interaction_combinators/commutation.md) - Interaction between different symbols
- [Annihilation Rules](reactions/interaction_combinators/annihilation.md) - Interaction between same symbols

### chemSKI Reactions
- [SKI Combinator Reductions](reactions/chemski/ski.md) - S, K, I combinator reactions

## Examples

- [Ackermann Function](examples/ackermann.md) - Computing Ackermann(2,2) with chemlambda
- [Ouroboros Quine](examples/ouroboros.md) - Self-replicating graph example
- [9-Quine](examples/9-quine.md) - Another quine graph example

## Key Papers

- [Artificial chemistry experiments with chemlambda, lambda calculus, interaction combinators](https://arxiv.org/abs/2003.14332) (arXiv:2003.14332)
- [Graph rewrites, from graphic lambda calculus, to chemlambda, to directed interaction combinators](https://arxiv.org/abs/2007.10288) (arXiv:2007.10288)
- [Artificial life properties of directed interaction combinators vs. chemlambda](https://arxiv.org/abs/2005.06060) (arXiv:2005.06060)
- [Molecular computers with interaction combinators like graph rewriting systems](https://github.com/chemlambda/molecular)
- [chemSKI with tokens: world building and economy in the SKI universe](https://arxiv.org/abs/2306.00938) (arXiv:2306.00938)

## Resources

- [Chemlambda Project Page](https://chemlambda.github.io/)
- [Marius Buliga's Homepage](https://mbuliga.github.io/)
- [GitHub: chemlambda/molecular](https://github.com/chemlambda/molecular)
- [GitHub: mbuliga/chemski](https://github.com/mbuliga/chemski)

## Motivation

Buliga's work bridges several important areas:

1. **Molecular Computing**: The goal of computing with real chemistry, where molecules transform through chemical reactions to perform computation
2. **Decentralized Computing**: Local, asynchronous, distributed algorithms that require no global coordination
3. **Artificial Life**: Self-replicating structures that exhibit metabolism, replication, and death
4. **Graph Rewriting Universality**: Understanding computation at the structural level, independent of semantics

## Structure-to-Structure Computation

A key insight of Buliga's work is the focus on **structure-to-structure** computation rather than meaning-to-meaning computation. This allows:

- Computation without semantic constraints
- Natural parallel reduction
- Emergence of artificial life properties
- Potential implementation in real chemistry

## License

This documentation is provided for educational and research purposes. Please refer to the original papers and repositories for licensing information.

## Contributing

This is a documentation repository. For implementations and experiments, please refer to the original repositories listed in the Resources section.

