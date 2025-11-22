"""
Formula representation and parsing for Natural Deduction Proof Assistant.

This module implements the formula structure for propositional and first-order logic
following van Dalen's formal system. It includes:
- Abstract formula classes for both logics
- A recursive descent parser
- String representation methods for pretty printing
"""

from abc import ABC, abstractmethod
from typing import Set, List, Optional, Union
import re


class Formula(ABC):
    """Abstract base class for logical formulas."""

    @abstractmethod
    def __str__(self) -> str:
        """Return string representation of the formula."""
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        """Check equality of formulas."""
        pass

    @abstractmethod
    def __hash__(self) -> int:
        """Return hash for use in sets/dicts."""
        pass

    @abstractmethod
    def get_free_variables(self) -> Set[str]:
        """Return set of free variables in the formula."""
        pass

    @abstractmethod
    def substitute(self, var: str, term: 'Term') -> 'Formula':
        """Substitute term for variable in formula."""
        pass

    @abstractmethod
    def is_free_for(self, term: 'Term', var: str) -> bool:
        """Check if term is free for substitution of var."""
        pass


class Term(ABC):
    """Abstract base class for terms in first-order logic."""

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @abstractmethod
    def get_variables(self) -> Set[str]:
        """Return set of all variables in the term."""
        pass

    @abstractmethod
    def substitute(self, var: str, term: 'Term') -> 'Term':
        """Substitute term for variable."""
        pass


# TERMS

class Variable(Term):
    """Variable term."""

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        return isinstance(other, Variable) and self.name == other.name

    def __hash__(self) -> int:
        return hash(('Variable', self.name))

    def get_variables(self) -> Set[str]:
        return {self.name}

    def substitute(self, var: str, term: Term) -> Term:
        if self.name == var:
            return term
        return self


class Constant(Term):
    """Constant term."""

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        return isinstance(other, Constant) and self.name == other.name

    def __hash__(self) -> int:
        return hash(('Constant', self.name))

    def get_variables(self) -> Set[str]:
        return set()

    def substitute(self, var: str, term: Term) -> Term:
        return self


class FunctionApplication(Term):
    """Function application f(t1, ..., tn)."""

    def __init__(self, function: str, args: List[Term]):
        self.function = function
        self.args = args

    def __str__(self) -> str:
        args_str = ', '.join(str(arg) for arg in self.args)
        return f"{self.function}({args_str})"

    def __eq__(self, other) -> bool:
        return (isinstance(other, FunctionApplication) and
                self.function == other.function and
                self.args == other.args)

    def __hash__(self) -> int:
        return hash(('FunctionApplication', self.function, tuple(self.args)))

    def get_variables(self) -> Set[str]:
        variables = set()
        for arg in self.args:
            variables.update(arg.get_variables())
        return variables

    def substitute(self, var: str, term: Term) -> Term:
        new_args = [arg.substitute(var, term) for arg in self.args]
        return FunctionApplication(self.function, new_args)


# FORMULAS

class AtomicFormula(Formula):
    """Atomic proposition or predicate."""

    def __init__(self, predicate: str, args: List[Term] = None):
        self.predicate = predicate
        self.args = args if args is not None else []

    def __str__(self) -> str:
        if not self.args:
            return self.predicate
        args_str = ', '.join(str(arg) for arg in self.args)
        return f"{self.predicate}({args_str})"

    def __eq__(self, other) -> bool:
        return (isinstance(other, AtomicFormula) and
                self.predicate == other.predicate and
                self.args == other.args)

    def __hash__(self) -> int:
        return hash(('AtomicFormula', self.predicate, tuple(self.args)))

    def get_free_variables(self) -> Set[str]:
        variables = set()
        for arg in self.args:
            variables.update(arg.get_variables())
        return variables

    def substitute(self, var: str, term: Term) -> Formula:
        new_args = [arg.substitute(var, term) for arg in self.args]
        return AtomicFormula(self.predicate, new_args)

    def is_free_for(self, term: Term, var: str) -> bool:
        # Atomic formulas have no bound variables, so substitution is always free
        return True


class Bottom(Formula):
    """The bottom (false) formula ⊥."""

    def __str__(self) -> str:
        return "⊥"

    def __eq__(self, other) -> bool:
        return isinstance(other, Bottom)

    def __hash__(self) -> int:
        return hash('Bottom')

    def get_free_variables(self) -> Set[str]:
        return set()

    def substitute(self, var: str, term: Term) -> Formula:
        return self

    def is_free_for(self, term: Term, var: str) -> bool:
        return True


class Negation(Formula):
    """Negation ¬φ."""

    def __init__(self, formula: Formula):
        self.formula = formula

    def __str__(self) -> str:
        # Add parentheses for binary connectives
        if isinstance(self.formula, (Conjunction, Disjunction, Implication)):
            return f"¬({self.formula})"
        return f"¬{self.formula}"

    def __eq__(self, other) -> bool:
        return isinstance(other, Negation) and self.formula == other.formula

    def __hash__(self) -> int:
        return hash(('Negation', self.formula))

    def get_free_variables(self) -> Set[str]:
        return self.formula.get_free_variables()

    def substitute(self, var: str, term: Term) -> Formula:
        return Negation(self.formula.substitute(var, term))

    def is_free_for(self, term: Term, var: str) -> bool:
        return self.formula.is_free_for(term, var)


class Conjunction(Formula):
    """Conjunction φ ∧ ψ."""

    def __init__(self, left: Formula, right: Formula):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f"({self.left} ∧ {self.right})"

    def __eq__(self, other) -> bool:
        return (isinstance(other, Conjunction) and
                self.left == other.left and
                self.right == other.right)

    def __hash__(self) -> int:
        return hash(('Conjunction', self.left, self.right))

    def get_free_variables(self) -> Set[str]:
        return self.left.get_free_variables() | self.right.get_free_variables()

    def substitute(self, var: str, term: Term) -> Formula:
        return Conjunction(
            self.left.substitute(var, term),
            self.right.substitute(var, term)
        )

    def is_free_for(self, term: Term, var: str) -> bool:
        return (self.left.is_free_for(term, var) and
                self.right.is_free_for(term, var))


class Disjunction(Formula):
    """Disjunction φ ∨ ψ."""

    def __init__(self, left: Formula, right: Formula):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f"({self.left} ∨ {self.right})"

    def __eq__(self, other) -> bool:
        return (isinstance(other, Disjunction) and
                self.left == other.left and
                self.right == other.right)

    def __hash__(self) -> int:
        return hash(('Disjunction', self.left, self.right))

    def get_free_variables(self) -> Set[str]:
        return self.left.get_free_variables() | self.right.get_free_variables()

    def substitute(self, var: str, term: Term) -> Formula:
        return Disjunction(
            self.left.substitute(var, term),
            self.right.substitute(var, term)
        )

    def is_free_for(self, term: Term, var: str) -> bool:
        return (self.left.is_free_for(term, var) and
                self.right.is_free_for(term, var))


class Implication(Formula):
    """Implication φ → ψ."""

    def __init__(self, antecedent: Formula, consequent: Formula):
        self.antecedent = antecedent
        self.consequent = consequent

    def __str__(self) -> str:
        return f"({self.antecedent} → {self.consequent})"

    def __eq__(self, other) -> bool:
        return (isinstance(other, Implication) and
                self.antecedent == other.antecedent and
                self.consequent == other.consequent)

    def __hash__(self) -> int:
        return hash(('Implication', self.antecedent, self.consequent))

    def get_free_variables(self) -> Set[str]:
        return self.antecedent.get_free_variables() | self.consequent.get_free_variables()

    def substitute(self, var: str, term: Term) -> Formula:
        return Implication(
            self.antecedent.substitute(var, term),
            self.consequent.substitute(var, term)
        )

    def is_free_for(self, term: Term, var: str) -> bool:
        return (self.antecedent.is_free_for(term, var) and
                self.consequent.is_free_for(term, var))


class Universal(Formula):
    """Universal quantification ∀x.φ."""

    def __init__(self, variable: str, formula: Formula):
        self.variable = variable
        self.formula = formula

    def __str__(self) -> str:
        return f"∀{self.variable}.{self.formula}"

    def __eq__(self, other) -> bool:
        return (isinstance(other, Universal) and
                self.variable == other.variable and
                self.formula == other.formula)

    def __hash__(self) -> int:
        return hash(('Universal', self.variable, self.formula))

    def get_free_variables(self) -> Set[str]:
        free_vars = self.formula.get_free_variables()
        return free_vars - {self.variable}

    def substitute(self, var: str, term: Term) -> Formula:
        if var == self.variable:
            # Variable is bound, no substitution
            return self
        elif self.variable in term.get_variables():
            # Need to rename bound variable to avoid capture
            new_var = self._fresh_variable(term.get_variables() |
                                           self.formula.get_free_variables())
            renamed_formula = self.formula.substitute(self.variable, Variable(new_var))
            return Universal(new_var, renamed_formula.substitute(var, term))
        else:
            return Universal(self.variable, self.formula.substitute(var, term))

    def is_free_for(self, term: Term, var: str) -> bool:
        if var == self.variable:
            return True
        if self.variable in term.get_variables():
            # The term contains the bound variable, check if var occurs free
            # in the scope where the variable is bound
            return var not in self.formula.get_free_variables()
        return self.formula.is_free_for(term, var)

    def _fresh_variable(self, used_vars: Set[str]) -> str:
        """Generate a fresh variable name."""
        base = self.variable
        counter = 0
        while f"{base}{counter}" in used_vars:
            counter += 1
        return f"{base}{counter}"


class Existential(Formula):
    """Existential quantification ∃x.φ."""

    def __init__(self, variable: str, formula: Formula):
        self.variable = variable
        self.formula = formula

    def __str__(self) -> str:
        return f"∃{self.variable}.{self.formula}"

    def __eq__(self, other) -> bool:
        return (isinstance(other, Existential) and
                self.variable == other.variable and
                self.formula == other.formula)

    def __hash__(self) -> int:
        return hash(('Existential', self.variable, self.formula))

    def get_free_variables(self) -> Set[str]:
        free_vars = self.formula.get_free_variables()
        return free_vars - {self.variable}

    def substitute(self, var: str, term: Term) -> Formula:
        if var == self.variable:
            # Variable is bound, no substitution
            return self
        elif self.variable in term.get_variables():
            # Need to rename bound variable to avoid capture
            new_var = self._fresh_variable(term.get_variables() |
                                           self.formula.get_free_variables())
            renamed_formula = self.formula.substitute(self.variable, Variable(new_var))
            return Existential(new_var, renamed_formula.substitute(var, term))
        else:
            return Existential(self.variable, self.formula.substitute(var, term))

    def is_free_for(self, term: Term, var: str) -> bool:
        if var == self.variable:
            return True
        if self.variable in term.get_variables():
            return var not in self.formula.get_free_variables()
        return self.formula.is_free_for(term, var)

    def _fresh_variable(self, used_vars: Set[str]) -> str:
        """Generate a fresh variable name."""
        base = self.variable
        counter = 0
        while f"{base}{counter}" in used_vars:
            counter += 1
        return f"{base}{counter}"


class FormulaParser:
    """Recursive descent parser for formulas."""

    def __init__(self):
        self.text = ""
        self.pos = 0
        self.constants = set()  # Track encountered constants

    def parse(self, text: str) -> Formula:
        """Parse a formula from text string."""
        self.text = text.strip()
        self.pos = 0
        formula = self._parse_formula()
        if self.pos < len(self.text):
            raise ValueError(f"Unexpected characters after formula: {self.text[self.pos:]}")
        return formula

    def _current(self) -> Optional[str]:
        """Get current character without consuming."""
        if self.pos < len(self.text):
            return self.text[self.pos]
        return None

    def _consume(self, expected: Optional[str] = None) -> Optional[str]:
        """Consume and return current character."""
        if self.pos >= len(self.text):
            if expected:
                raise ValueError(f"Expected '{expected}' but reached end of input")
            return None

        char = self.text[self.pos]
        if expected and char != expected:
            raise ValueError(f"Expected '{expected}' but got '{char}' at position {self.pos}")

        self.pos += 1
        return char

    def _skip_whitespace(self):
        """Skip whitespace characters."""
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def _parse_identifier(self) -> str:
        """Parse an identifier (variable, constant, predicate, or function name)."""
        self._skip_whitespace()
        start = self.pos

        # Handle special bottom symbol
        if self.text[self.pos:self.pos + 1] in ['⊥', '_']:
            self.pos += 1
            return self.text[start:self.pos]

        # Regular identifier: letter followed by alphanumerics
        if not self.text[self.pos].isalpha():
            raise ValueError(f"Expected identifier at position {self.pos}")

        while self.pos < len(self.text) and (self.text[self.pos].isalnum() or
                                             self.text[self.pos] in ['_', '\'']):
            self.pos += 1

        return self.text[start:self.pos]

    def _parse_term(self) -> Term:
        """Parse a term."""
        self._skip_whitespace()

        # Parse identifier
        name = self._parse_identifier()
        self._skip_whitespace()

        # Check if it's a function application
        if self._current() == '(':
            # Function application
            self._consume('(')
            args = []

            while True:
                self._skip_whitespace()
                if self._current() == ')':
                    break

                args.append(self._parse_term())
                self._skip_whitespace()

                if self._current() == ',':
                    self._consume(',')
                    self._skip_whitespace()
                    # Check for trailing comma
                    if self._current() == ')':
                        raise ValueError(f"Trailing comma in argument list at position {self.pos}")
                elif self._current() == ')':
                    break
                else:
                    raise ValueError(f"Expected ',' or ')' at position {self.pos}")

            self._consume(')')
            return FunctionApplication(name, args)
        else:
            # Variable or constant
            # Simple heuristic: lowercase = variable, uppercase = constant
            # Can be overridden by tracking quantified variables
            if name[0].islower():
                return Variable(name)
            else:
                self.constants.add(name)
                return Constant(name)

    def _parse_atomic(self) -> Formula:
        """Parse an atomic formula."""
        self._skip_whitespace()

        # Check for bottom
        if self._current() in ['⊥', '_']:
            self._consume()
            return Bottom()

        # Check for negation symbol at the start
        if self._current() in ['~', '¬', '!']:
            return self._parse_negation()

        # Parse identifier (predicate or start of term)
        name = self._parse_identifier()
        self._skip_whitespace()

        # Check if it's a predicate with arguments
        if self._current() == '(':
            self._consume('(')
            args = []

            while True:
                self._skip_whitespace()
                if self._current() == ')':
                    break

                args.append(self._parse_term())
                self._skip_whitespace()

                if self._current() == ',':
                    self._consume(',')
                    self._skip_whitespace()
                    # Check for trailing comma
                    if self._current() == ')':
                        raise ValueError(f"Trailing comma in argument list at position {self.pos}")
                elif self._current() == ')':
                    break
                else:
                    raise ValueError(f"Expected ',' or ')' at position {self.pos}")

            self._consume(')')
            return AtomicFormula(name, args)
        else:
            # Propositional atom (0-ary predicate)
            # Typically lowercase letters like p, q, r
            return AtomicFormula(name, [])

    def _parse_negation(self) -> Formula:
        """Parse a negation."""
        self._skip_whitespace()

        if self._current() in ['~', '¬', '!']:
            self._consume()
            self._skip_whitespace()

            # Parse the negated formula
            formula = self._parse_primary()
            return Negation(formula)

        return self._parse_primary()

    def _parse_primary(self) -> Formula:
        """Parse a primary formula (atomic, quantified, or parenthesized)."""
        self._skip_whitespace()

        # Check for parentheses
        if self._current() == '(':
            self._consume('(')
            formula = self._parse_formula()
            self._skip_whitespace()
            self._consume(')')
            return formula

        # Check for quantifiers
        if self.text[self.pos:self.pos + 6] == 'forall':
            self.pos += 6
            return self._parse_universal()
        elif self.text[self.pos:self.pos + 6] == 'exists':
            self.pos += 6
            return self._parse_existential()
        elif self._current() == '∀':
            self._consume()
            return self._parse_universal()
        elif self._current() == '∃':
            self._consume()
            return self._parse_existential()

        # Otherwise, parse atomic
        return self._parse_atomic()

    def _parse_universal(self) -> Formula:
        """Parse universal quantification."""
        self._skip_whitespace()
        var = self._parse_identifier()

        # Check if the identifier looks like a predicate (uppercase)
        # This would be invalid syntax like "forall P(x)"
        if var[0].isupper():
            # Check if there's a parenthesis following
            self._skip_whitespace()
            if self._current() == '(':
                raise ValueError(f"Invalid quantifier syntax: cannot quantify over predicate '{var}'")

        self._skip_whitespace()

        # Accept either '.' or no separator
        if self._current() == '.':
            self._consume('.')

        formula = self._parse_formula()
        return Universal(var, formula)

    def _parse_existential(self) -> Formula:
        """Parse existential quantification."""
        self._skip_whitespace()
        var = self._parse_identifier()

        # Check if the identifier looks like a predicate (uppercase)
        if var[0].isupper():
            # Check if there's a parenthesis following
            self._skip_whitespace()
            if self._current() == '(':
                raise ValueError(f"Invalid quantifier syntax: cannot quantify over predicate '{var}'")

        self._skip_whitespace()

        # Accept either '.' or no separator
        if self._current() == '.':
            self._consume('.')

        formula = self._parse_formula()
        return Existential(var, formula)

    def _parse_formula(self) -> Formula:
        """Parse a complete formula with binary connectives."""
        # Parse implication (lowest precedence)
        return self._parse_implication()

    def _parse_implication(self) -> Formula:
        """Parse implication (right-associative)."""
        left = self._parse_disjunction()
        self._skip_whitespace()

        # Check for implication operator
        if self.text[self.pos:self.pos + 2] == '->':
            self.pos += 2
            right = self._parse_implication()  # Right-associative
            return Implication(left, right)
        elif self._current() == '→':
            self._consume()
            right = self._parse_implication()  # Right-associative
            return Implication(left, right)

        return left

    def _parse_disjunction(self) -> Formula:
        """Parse disjunction (left-associative)."""
        left = self._parse_conjunction()

        while True:
            self._skip_whitespace()

            if self._current() in ['|', '∨']:
                self._consume()
                right = self._parse_conjunction()
                left = Disjunction(left, right)
            else:
                break

        return left

    def _parse_conjunction(self) -> Formula:
        """Parse conjunction (left-associative)."""
        left = self._parse_negation()

        while True:
            self._skip_whitespace()

            if self._current() in ['&', '∧']:
                self._consume()
                right = self._parse_negation()
                left = Conjunction(left, right)
            else:
                break

        return left


# Helper function for easy parsing
def parse(text: str) -> Formula:
    """Parse a formula from a string."""
    parser = FormulaParser()
    return parser.parse(text)


# Example usage and testing
if __name__ == "__main__":
    # Test propositional formulas
    test_cases_prop = [
        "p",
        "~p",
        "p & q",
        "p | q",
        "p -> q",
        "(p & q) -> r",
        "~(p | q)",
        "p -> (q -> r)",
        "⊥",
        "p & ~p -> ⊥"
    ]

    print("Testing Propositional Logic Formulas:")
    print("-" * 50)
    for test in test_cases_prop:
        try:
            formula = parse(test)
            print(f"Input:  {test}")
            print(f"Parsed: {formula}")
            print(f"Type:   {type(formula).__name__}")
            print()
        except Exception as e:
            print(f"Error parsing '{test}': {e}")
            print()

    # Test first-order formulas
    test_cases_fol = [
        "P(x)",
        "Q(x, y)",
        "forall x. P(x)",
        "exists x. P(x)",
        "forall x. (P(x) -> Q(x))",
        "exists x. (P(x) & Q(x))",
        "forall x. exists y. R(x, y)",
        "P(f(x))",
        "forall x. (P(x) -> exists y. Q(x, y))",
        "∀x. ∃y. (P(x) & Q(y) -> R(x, y))"
    ]

    print("\nTesting First-Order Logic Formulas:")
    print("-" * 50)
    for test in test_cases_fol:
        try:
            formula = parse(test)
            print(f"Input:  {test}")
            print(f"Parsed: {formula}")
            print(f"Free:   {formula.get_free_variables()}")
            print()
        except Exception as e:
            print(f"Error parsing '{test}': {e}")
            print()