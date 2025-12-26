# Batch Analysis for High-Order Entropy Evaluation

## Why Many Simulations Are Needed

High-order entropy analysis requires **statistical significance** because:

1. **Random Variation**: Each simulation follows a different reduction path
2. **Stochastic Processes**: Random reaction selection creates variability
3. **Graph Diversity**: Different initial graphs lead to different behaviors
4. **Emergent Properties**: High-order effects emerge probabilistically
5. **Statistical Measures**: Mean, variance, and confidence intervals need many samples

## The Batch Analysis System

The `batch_entropy_analysis.py` module provides:

- **BatchEntropyAnalyzer**: Runs many simulations and aggregates statistics
- **Statistical aggregation**: Mean, standard deviation, min, max, median
- **Evolution tracking**: Average entropy during reduction
- **Comparison tools**: Sequential vs parallel analysis

## Usage

### Basic Usage

```bash
# Run 100 simulations with default settings
python3 examples/batch_entropy_analysis.py

# Run 500 simulations for better statistics
python3 examples/batch_entropy_analysis.py --runs 500

# Run with more steps per simulation
python3 examples/batch_entropy_analysis.py --runs 200 --steps 100

# Larger graphs
python3 examples/batch_entropy_analysis.py --runs 100 --pairs 20
```

### Programmatic Usage

```python
from batch_entropy_analysis import BatchEntropyAnalyzer

analyzer = BatchEntropyAnalyzer(num_runs=100)

def create_graph(seed=None):
    # Your graph creation function
    graph = Graph()
    # ... create graph ...
    return graph

# Run batch analysis
stats = analyzer.run_batch(create_graph, num_runs=100, max_steps=50)

# Print results
analyzer.print_statistics(stats)
```

## What Statistics Are Collected

### Initial State
- Node entropy (Shannon entropy of node types)
- High-order interaction entropy
- Synergistic information

### Final State
- Same measures after reduction

### Evolution Statistics
- Mean entropy during reduction
- Standard deviation of entropy
- Maximum entropy reached

### Simulation Statistics
- Number of steps taken
- Final graph size

## Interpreting Results

### Mean ± Standard Deviation
- **Mean**: Typical behavior across all runs
- **Std Dev**: Variability in results
- **Large std dev**: High variability (may need more runs)

### Changes (Final - Initial)
- **Positive**: Entropy increased (more information/complexity)
- **Negative**: Entropy decreased (less information/complexity)
- **Near zero**: Stable entropy

### Maximum Values
- Shows peak entropy reached
- Reveals potential for high-order effects
- Useful for understanding system capacity

## Recommended Number of Runs

| Purpose | Minimum Runs | Recommended Runs |
|---------|-------------|------------------|
| Quick test | 10-20 | 50 |
| Basic analysis | 50 | 100-200 |
| Publication quality | 200 | 500-1000 |
| High precision | 500 | 1000+ |

## Example: Evaluating High-Order Entropy

```python
# Run many simulations
analyzer = BatchEntropyAnalyzer(num_runs=500)

stats = analyzer.run_batch(create_graph, num_runs=500, max_steps=100)

# Check if high-order entropy is significant
high_order_mean = stats['final']['high_order_entropy']['mean']
high_order_std = stats['final']['high_order_entropy']['std']

if high_order_mean > 2 * high_order_std:
    print("High-order entropy is statistically significant!")
else:
    print("Need more runs or different graph structure")
```

## Comparing Sequential vs Parallel

The batch system can compare sequential and parallel reduction:

```python
compare_sequential_vs_parallel_batch(num_runs=100)
```

This shows:
- Whether parallel systems have higher high-order entropy
- Whether synergistic information is greater in parallel systems
- Statistical significance of differences

## Key Insights

1. **Many runs needed**: High-order entropy requires statistical analysis
2. **Variability matters**: Standard deviation shows reliability
3. **Evolution tracking**: Mean entropy during reduction reveals dynamics
4. **Maximum values**: Show system capacity for high-order effects
5. **Comparison**: Sequential vs parallel reveals unique advantages

## Performance Considerations

- **100 runs**: ~1-2 minutes (depending on graph size)
- **500 runs**: ~5-10 minutes
- **1000 runs**: ~10-20 minutes

For faster analysis:
- Reduce `max_steps` per simulation
- Use smaller graphs (`--pairs` parameter)
- Run in parallel (modify code to use multiprocessing)

## Output Interpretation

```
Initial State:
  Node Entropy:      1.4083 ± 0.0954
  High-Order Entropy: 0.0000 ± 0.0000
  Synergistic Info:   0.0000 ± 0.0000

Final State:
  Node Entropy:      1.6714 ± 0.7433
  High-Order Entropy: 0.0000 ± 0.0000
  Synergistic Info:   0.0000 ± 0.0000
```

Interpretation:
- **Node Entropy**: Increased from 1.41 to 1.67 (more diversity)
- **High-Order Entropy**: Still 0 (may need different graph structure)
- **Synergistic Info**: Still 0 (no synergistic effects detected)

If high-order entropy is 0:
- Try larger graphs
- Create more interconnected structures
- Use parallel rewrites (not sequential)
- Increase number of interaction sites

## Next Steps

1. **Run batch analysis** with appropriate number of runs
2. **Check statistics** for significance
3. **Modify graph structure** if high-order effects not detected
4. **Compare** sequential vs parallel
5. **Iterate** to find structures with high-order entropy

## References

- Aguera's work on high-order entropy
- Statistical analysis of complex systems
- Information theory and entropy measures

