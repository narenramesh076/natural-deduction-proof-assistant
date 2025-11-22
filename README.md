# natural-deduction-proof-assistant

A command-line Natural Deduction Proof Assistant in Python that validates formal proofs in propositional and first-order logic following van Dalen's formal system.

## Project Status: Day 1 Complete

### Day 1 Achievements: Formula Representation and Parsing

Successfully implemented a robust formula parser for propositional and first-order logic with the following features:

#### Formula Classes Implemented

**Propositional Logic:**
- `AtomicFormula`: Propositional atoms (p, q, r, ...) and predicates
- `Bottom`: The false formula (⊥)
- `Negation`: Negation of formulas (¬φ)
- `Conjunction`: Conjunction (φ ∧ ψ)
- `Disjunction`: Disjunction (φ ∨ ψ)
- `Implication`: Material implication (φ → ψ)

**First-Order Logic:**
- `Universal`: Universal quantification (∀x.φ)
- `Existential`: Existential quantification (∃x.φ)
- `Variable`: Individual variables (x, y, z, ...)
- `Constant`: Individual constants (C, D, ...)
- `FunctionApplication`: Function terms f(t₁, ..., tₙ)

#### Parser Features

- **Recursive descent parser** with proper precedence handling
- **Multiple notation support**:
  - Negation: `~`, `¬`, `!`
  - Conjunction: `&`, `∧`
  - Disjunction: `|`, `∨`
  - Implication: `->`, `→`
  - Bottom: `⊥`, `_`
  - Quantifiers: `forall`/`∀`, `exists`/`∃`
- **Free variable detection**: Correctly identifies free variables in formulas
- **Substitution**: Implements proper substitution with variable capture avoidance
- **Error handling**: Comprehensive error messages for invalid syntax

#### Usage Examples

**Propositional Logic:**
```
p                     → p
~p                    → ¬p
p & q                 → (p ∧ q)
p | q                 → (p ∨ q)
p -> q                → (p → q)
(p & q) -> r          → ((p ∧ q) → r)
```

**First-Order Logic:**
```
P(x)                  → P(x)
forall x. P(x)        → ∀x.P(x)
exists x. P(x)        → ∃x.P(x)
forall x. exists y. R(x, y)  → ∀x.∃y.R(x, y)
```

### Running the Application

**Interactive mode:**
```bash
python3 natural_deduction/main.py
```

**Parse a single formula:**
```bash
python3 natural_deduction/main.py "p -> q"
```

**Run tests:**
```bash
python3 natural_deduction/test_formula.py
```

### Test Results

**51 tests passed** covering:
- 21 propositional logic formulas
- 16 first-order logic formulas  
- 8 free variable detection tests
- 6 substitution tests
- Multiple error handling cases

### File Structure

```
natural_deduction/
├── __init__.py         # Package initialization
├── formula.py          # Formula classes and parser
├── main.py            # CLI entry point
├── test_formula.py    # Comprehensive test suite
└── README.md          # This file
```

### Next Steps (Day 2)

Tomorrow's task: Implement Natural Deduction Rules
- Introduction and elimination rules for all connectives
- Proper handling of assumptions and scope
- Variable conditions for quantifier rules
- Rule precondition checking

### Technical Notes

The implementation follows van Dalen's "Logic and Structure" closely:
- Using a minimal set of connectives (∧, →, ⊥, ∀) as the core
- Additional connectives (∨, ∃, ¬) added for convenience
- Proper precedence: quantifiers > negation > conjunction > disjunction > implication
- Right-associative implication, left-associative conjunction/disjunction

### Dependencies

- Python 3.8+
- No external libraries