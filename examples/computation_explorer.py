#!/usr/bin/env python3
"""
Interactive Computation Explorer
Tool to explore what interaction combinators can compute
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chemlambda import Graph, Simulator
from church_encodings import (
    church_numeral, church_boolean, church_add, church_multiply, church_successor
)
from result_extractor import extract_result, graph_structure_summary
from lambda_compiler import compile_lambda_string, parse_lambda_term
from arithmetic_examples import compute_addition, compute_multiplication, compute_successor


class ComputationExplorer:
    """Interactive explorer for computation capabilities"""
    
    def __init__(self):
        self.examples = self._load_examples()
    
    def _load_examples(self) -> dict:
        """Load example computations"""
        return {
            "church_0": {
                "name": "Church Numeral 0",
                "description": "Encode Church numeral 0",
                "func": lambda: church_numeral(0),
            },
            "church_1": {
                "name": "Church Numeral 1",
                "description": "Encode Church numeral 1",
                "func": lambda: church_numeral(1),
            },
            "church_5": {
                "name": "Church Numeral 5",
                "description": "Encode Church numeral 5",
                "func": lambda: church_numeral(5),
            },
            "add_2_3": {
                "name": "Addition: 2 + 3",
                "description": "Compute 2 + 3 using Church numerals",
                "func": lambda: compute_addition(2, 3),
            },
            "mult_2_3": {
                "name": "Multiplication: 2 * 3",
                "description": "Compute 2 * 3 using Church numerals",
                "func": lambda: compute_multiplication(2, 3),
            },
            "succ_5": {
                "name": "Successor: succ(5)",
                "description": "Compute successor of 5",
                "func": lambda: compute_successor(5),
            },
            "church_true": {
                "name": "Church Boolean: true",
                "description": "Encode Church boolean true",
                "func": lambda: church_boolean(True),
            },
            "church_false": {
                "name": "Church Boolean: false",
                "description": "Encode Church boolean false",
                "func": lambda: church_boolean(False),
            },
        }
    
    def show_help(self):
        """Show help message"""
        print("\n" + "=" * 60)
        print("Computation Explorer - Help")
        print("=" * 60)
        print("\nCommands:")
        print("  encode <term>     - Encode a lambda calculus term")
        print("  compute <expr>    - Compute an arithmetic expression")
        print("  show <example>    - Show an example computation")
        print("  list               - List available examples")
        print("  run <example>     - Run an example and show results")
        print("  help               - Show this help message")
        print("  quit / exit        - Exit the explorer")
        print("\nExamples:")
        print("  encode λx.x")
        print("  compute 2+3")
        print("  show church_5")
        print("  run add_2_3")
        print("=" * 60)
    
    def list_examples(self):
        """List all available examples"""
        print("\n" + "=" * 60)
        print("Available Examples")
        print("=" * 60)
        for key, example in self.examples.items():
            print(f"\n  {key}:")
            print(f"    Name: {example['name']}")
            print(f"    Description: {example['description']}")
        print("=" * 60)
    
    def show_example(self, example_key: str):
        """Show an example without running it"""
        if example_key not in self.examples:
            print(f"Unknown example: {example_key}")
            print("Use 'list' to see available examples.")
            return
        
        example = self.examples[example_key]
        print(f"\n{'=' * 60}")
        print(f"Example: {example['name']}")
        print('=' * 60)
        print(f"Description: {example['description']}")
        
        try:
            result = example['func']()
            if isinstance(result, Graph):
                summary = graph_structure_summary(result)
                print(f"\nGraph Structure:")
                print(f"  Nodes: {summary['total_nodes']}")
                print(f"  Edges: {summary['total_edges']}")
                print(f"  Node types: {summary['node_types']}")
            elif isinstance(result, dict):
                print(f"\nComputation Result:")
                print(f"  Operation: {result.get('operation', 'N/A')}")
                print(f"  Steps: {result.get('steps', 'N/A')}")
                print(f"  Result: {result.get('result_value', 'N/A')}")
        except Exception as e:
            print(f"Error: {e}")
    
    def run_example(self, example_key: str):
        """Run an example and show detailed results"""
        if example_key not in self.examples:
            print(f"Unknown example: {example_key}")
            print("Use 'list' to see available examples.")
            return
        
        example = self.examples[example_key]
        print(f"\n{'=' * 60}")
        print(f"Running: {example['name']}")
        print('=' * 60)
        
        try:
            result = example['func']()
            
            if isinstance(result, Graph):
                # It's a graph encoding
                print(f"\nEncoded Graph:")
                summary = graph_structure_summary(result)
                print(f"  Nodes: {summary['total_nodes']}")
                print(f"  Edges: {summary['total_edges']}")
                print(f"  Node types: {summary['node_types']}")
                
                # Try to extract result
                result_type, result_value = extract_result(result)
                if result_type:
                    print(f"\nExtracted Result:")
                    print(f"  Type: {result_type}")
                    print(f"  Value: {result_value}")
                
                # Show graph structure
                print(f"\nGraph (mol format):")
                print(result.to_mol_format())
            
            elif isinstance(result, dict):
                # It's a computation result
                print(f"\nComputation Details:")
                print(f"  Operation: {result.get('operation', 'N/A')}")
                print(f"  Steps taken: {result.get('steps', 'N/A')}")
                
                stats = result.get('stats', {})
                print(f"\nStatistics:")
                print(f"  Total steps: {stats.get('total_steps', 'N/A')}")
                print(f"  Final nodes: {stats.get('final_nodes', 'N/A')}")
                print(f"  Final edges: {stats.get('final_edges', 'N/A')}")
                if stats.get('reaction_counts'):
                    print(f"  Reaction counts: {stats['reaction_counts']}")
                
                result_type = result.get('result_type')
                result_value = result.get('result_value')
                if result_type:
                    print(f"\nResult:")
                    print(f"  Type: {result_type}")
                    print(f"  Value: {result_value}")
        
        except Exception as e:
            print(f"Error running example: {e}")
            import traceback
            traceback.print_exc()
    
    def encode_term(self, term_str: str):
        """Encode a lambda calculus term"""
        print(f"\nEncoding: {term_str}")
        print('=' * 60)
        
        try:
            # Parse term
            term = parse_lambda_term(term_str)
            print(f"Parsed: {term}")
            
            # Compile to graph
            graph = compile_lambda_string(term_str)
            print(f"\nGraph: {graph}")
            
            summary = graph_structure_summary(graph)
            print(f"  Nodes: {summary['total_nodes']}")
            print(f"  Edges: {summary['total_edges']}")
            print(f"  Node types: {summary['node_types']}")
            
            # Show graph structure
            print(f"\nGraph (mol format):")
            print(graph.to_mol_format())
        
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
    def compute_expression(self, expr: str):
        """Compute an arithmetic expression"""
        print(f"\nComputing: {expr}")
        print('=' * 60)
        
        try:
            # Parse expression
            if '+' in expr:
                parts = expr.split('+')
                if len(parts) == 2:
                    m = int(parts[0].strip())
                    n = int(parts[1].strip())
                    result = compute_addition(m, n)
                    self._show_computation_result(result)
                    return
            
            if '*' in expr:
                parts = expr.split('*')
                if len(parts) == 2:
                    m = int(parts[0].strip())
                    n = int(parts[1].strip())
                    result = compute_multiplication(m, n)
                    self._show_computation_result(result)
                    return
            
            print(f"Unsupported expression format: {expr}")
            print("Supported: <number> + <number> or <number> * <number>")
        
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
    def _show_computation_result(self, result: dict):
        """Show computation result details"""
        print(f"\nOperation: {result.get('operation', 'N/A')}")
        print(f"Steps: {result.get('steps', 'N/A')}")
        
        stats = result.get('stats', {})
        print(f"\nStatistics:")
        print(f"  Total steps: {stats.get('total_steps', 'N/A')}")
        print(f"  Final nodes: {stats.get('final_nodes', 'N/A')}")
        print(f"  Final edges: {stats.get('final_edges', 'N/A')}")
        if stats.get('reaction_counts'):
            print(f"  Reaction counts: {stats['reaction_counts']}")
        
        result_type = result.get('result_type')
        result_value = result.get('result_value')
        if result_type:
            print(f"\nResult:")
            print(f"  Type: {result_type}")
            print(f"  Value: {result_value}")
    
    def run(self):
        """Run the interactive explorer"""
        print("=" * 60)
        print("Interaction Combinator Computation Explorer")
        print("=" * 60)
        print("\nExplore what interaction combinators can compute!")
        print("Type 'help' for commands, 'quit' to exit.")
        
        while True:
            try:
                command = input("\n> ").strip()
                
                if not command:
                    continue
                
                parts = command.split(None, 1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                if cmd in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                elif cmd == 'help':
                    self.show_help()
                
                elif cmd == 'list':
                    self.list_examples()
                
                elif cmd == 'show':
                    if args:
                        self.show_example(args)
                    else:
                        print("Usage: show <example_key>")
                        print("Use 'list' to see available examples.")
                
                elif cmd == 'run':
                    if args:
                        self.run_example(args)
                    else:
                        print("Usage: run <example_key>")
                        print("Use 'list' to see available examples.")
                
                elif cmd == 'encode':
                    if args:
                        self.encode_term(args)
                    else:
                        print("Usage: encode <lambda_term>")
                        print("Example: encode λx.x")
                
                elif cmd == 'compute':
                    if args:
                        self.compute_expression(args)
                    else:
                        print("Usage: compute <expression>")
                        print("Example: compute 2+3")
                
                else:
                    print(f"Unknown command: {cmd}")
                    print("Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except EOFError:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()


def main():
    """Main entry point"""
    explorer = ComputationExplorer()
    explorer.run()


if __name__ == "__main__":
    main()

