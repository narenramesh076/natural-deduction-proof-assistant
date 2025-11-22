#!/usr/bin/env python3
"""
Natural Deduction Proof Assistant
Main entry point and command-line interface

This proof assistant validates formal proofs in propositional and first-order logic
following van Dalen's natural deduction system.
"""

import sys
from formula import parse, Formula


class ProofAssistant:
    """Main proof assistant application."""

    def __init__(self):
        self.current_proof = None
        self.formulas = {}  # Store parsed formulas by name

    def run(self):
        """Run the interactive proof assistant."""
        self.print_welcome()

        while True:
            try:
                command = input("\n> ").strip().lower()

                if command in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                elif command in ['help', 'h', '?']:
                    self.print_help()
                elif command.startswith('parse '):
                    self.parse_formula(command[6:])
                elif command == 'list':
                    self.list_formulas()
                elif command == 'clear':
                    self.clear_formulas()
                elif command.startswith('test'):
                    self.run_tests()
                else:
                    print(f"Unknown command: {command}")
                    print("Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\nUse 'quit' to exit.")
            except Exception as e:
                print(f"Error: {e}")

    def print_welcome(self):
        """Print welcome message."""
        print("=" * 60)
        print("Natural Deduction Proof Assistant")
        print("Based on van Dalen's Logic and Structure")
        print("=" * 60)
        print("\nType 'help' for available commands.")

    def print_help(self):
        """Print help message."""
        print("\nAvailable Commands:")
        print("-" * 40)
        print("  parse <formula>  - Parse and display a formula")
        print("  list            - List all stored formulas")
        print("  clear           - Clear all stored formulas")
        print("  test            - Run example formulas")
        print("  help            - Show this help message")
        print("  quit            - Exit the program")
        print("\nFormula Syntax:")
        print("-" * 40)
        print("Propositional:")
        print("  Atoms:        p, q, r, ...")
        print("  Negation:     ~p or ¬p or !p")
        print("  Conjunction:  p & q or p ∧ q")
        print("  Disjunction:  p | q or p ∨ q")
        print("  Implication:  p -> q or p → q")
        print("  Bottom:       ⊥ or _")
        print("\nFirst-Order:")
        print("  Predicates:   P(x), Q(x,y), ...")
        print("  Universal:    forall x. P(x) or ∀x. P(x)")
        print("  Existential:  exists x. P(x) or ∃x. P(x)")
        print("  Functions:    f(x), g(x,y), ...")

    def parse_formula(self, formula_text: str):
        """Parse and display a formula."""
        if not formula_text:
            print("Please provide a formula to parse.")
            return

        try:
            formula = parse(formula_text)

            # Store the formula with a generated name
            name = f"f{len(self.formulas) + 1}"
            self.formulas[name] = formula

            print(f"\nParsed successfully as {name}:")
            print(f"  Formula:  {formula}")
            print(f"  Type:     {type(formula).__name__}")

            # Show additional information for formulas with variables
            free_vars = formula.get_free_variables()
            if free_vars:
                print(f"  Free vars: {', '.join(sorted(free_vars))}")

            # Show structure for complex formulas
            if hasattr(formula, 'left') and hasattr(formula, 'right'):
                print(f"  Left:     {formula.left}")
                print(f"  Right:    {formula.right}")
            elif hasattr(formula, 'formula'):
                print(f"  Subformula: {formula.formula}")

        except Exception as e:
            print(f"Parse error: {e}")

    def list_formulas(self):
        """List all stored formulas."""
        if not self.formulas:
            print("No formulas stored.")
            return

        print("\nStored Formulas:")
        print("-" * 40)
        for name, formula in self.formulas.items():
            print(f"  {name}: {formula}")

    def clear_formulas(self):
        """Clear all stored formulas."""
        self.formulas.clear()
        print("All formulas cleared.")

    def run_tests(self):
        """Run example formulas to demonstrate the parser."""
        print("\nRunning Example Formulas...")
        print("=" * 50)

        # Propositional logic examples
        prop_examples = [
            ("Simple atom", "p"),
            ("Negation", "~p"),
            ("Conjunction", "p & q"),
            ("Disjunction", "p | q"),
            ("Implication", "p -> q"),
            ("Modus ponens", "(p & (p -> q)) -> q"),
            ("De Morgan", "~(p & q) -> (~p | ~q)"),
            ("Contraposition", "(p -> q) -> (~q -> ~p)"),
            ("Bottom elimination", "⊥ -> p"),
            ("Double negation", "p -> ~~p")
        ]

        print("\nPropositional Logic:")
        print("-" * 40)
        for name, formula_text in prop_examples:
            try:
                formula = parse(formula_text)
                print(f"{name:20} {formula_text:25} ✓")
            except Exception as e:
                print(f"{name:20} {formula_text:25} ✗ ({e})")

        # First-order logic examples
        fol_examples = [
            ("Predicate", "P(x)"),
            ("Binary relation", "R(x, y)"),
            ("Universal", "forall x. P(x)"),
            ("Existential", "exists x. P(x)"),
            ("Universal conditional", "forall x. (P(x) -> Q(x))"),
            ("Existential conjunction", "exists x. (P(x) & Q(x))"),
            ("Nested quantifiers", "forall x. exists y. R(x, y)"),
            ("Function application", "P(f(x))"),
            ("Complex", "forall x. (P(x) -> exists y. R(x, y))"),
            ("Unicode quantifiers", "∀x. ∃y. R(x, y)")
        ]

        print("\nFirst-Order Logic:")
        print("-" * 40)
        for name, formula_text in fol_examples:
            try:
                formula = parse(formula_text)
                print(f"{name:20} {formula_text:35} ✓")
            except Exception as e:
                print(f"{name:20} {formula_text:35} ✗ ({e})")


def main():
    """Main entry point."""
    assistant = ProofAssistant()

    # If arguments provided, parse them as formulas
    if len(sys.argv) > 1:
        formula_text = ' '.join(sys.argv[1:])
        print(f"Parsing: {formula_text}")
        assistant.parse_formula(formula_text)
    else:
        # Run interactive mode
        assistant.run()


if __name__ == "__main__":
    main()