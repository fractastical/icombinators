"""
Artificial Life module for chemlambda
Quine detection, replication measurement, and ALife research tools
"""

from .quine_detector import (
    detect_quine,
    measure_replication_rate,
    QuineAnalyzer,
    find_non_conflicting_matches,
    apply_parallel_rewrites,
    is_isomorphic,
)

__all__ = [
    'detect_quine',
    'measure_replication_rate',
    'QuineAnalyzer',
    'find_non_conflicting_matches',
    'apply_parallel_rewrites',
    'is_isomorphic',
]

