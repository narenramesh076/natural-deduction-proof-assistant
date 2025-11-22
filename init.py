"""
Natural Deduction Proof Assistant

A command-line proof assistant for validating formal proofs in
propositional and first-order logic following van Dalen's natural deduction system.
"""

from .formula import (
    Formula, Term,
    Variable, Constant, FunctionApplication,
    AtomicFormula, Bottom, Negation, Conjunction,
    Disjunction, Implication, Universal, Existential,
    FormulaParser, parse
)

__version__ = "0.1.0"
__author__ = "Natural Deduction Project"

__all__ = [
    'Formula', 'Term',
    'Variable', 'Constant', 'FunctionApplication',
    'AtomicFormula', 'Bottom', 'Negation', 'Conjunction',
    'Disjunction', 'Implication', 'Universal', 'Existential',
    'FormulaParser', 'parse'
]