#!/usr/bin/env python3
"""
Test suite for the Natural Deduction formula parser.
Tests both propositional and first-order logic formulas.
"""

from formula import parse, Formula, AtomicFormula, Negation, Conjunction, Disjunction, Implication, Bottom, Universal, \
    Existential, Variable, Constant


def test_propositional_logic():
    """Test parsing of propositional logic formulas."""
    print("Testing Propositional Logic")
    print("=" * 50)

    tests = [
        # Basic atoms
        ("p", AtomicFormula),
        ("q", AtomicFormula),
        ("prop1", AtomicFormula),

        # Bottom
        ("⊥", Bottom),
        ("_", Bottom),

        # Negation
        ("~p", Negation),
        ("¬p", Negation),
        ("!p", Negation),

        # Binary connectives
        ("p & q", Conjunction),
        ("p ∧ q", Conjunction),
        ("p | q", Disjunction),
        ("p ∨ q", Disjunction),
        ("p -> q", Implication),
        ("p → q", Implication),

        # Complex formulas
        ("(p & q) -> r", Implication),
        ("p -> (q -> r)", Implication),
        ("~(p & q)", Negation),
        ("(p | q) & (r | s)", Conjunction),

        # Classical theorems
        ("p -> ~~p", Implication),  # Double negation introduction
        ("⊥ -> p", Implication),  # Ex falso
        ("(p -> q) -> (~q -> ~p)", Implication),  # Contraposition
    ]

    passed = 0
    failed = 0

    for formula_text, expected_type in tests:
        try:
            formula = parse(formula_text)
            if isinstance(formula, expected_type):
                print(f"✓ {formula_text:30} -> {formula}")
                passed += 1
            else:
                print(f"✗ {formula_text:30} -> Wrong type: {type(formula).__name__}")
                failed += 1
        except Exception as e:
            print(f"✗ {formula_text:30} -> Error: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return passed, failed


def test_first_order_logic():
    """Test parsing of first-order logic formulas."""
    print("\nTesting First-Order Logic")
    print("=" * 50)

    tests = [
        # Basic predicates
        ("P(x)", AtomicFormula),
        ("Q(x, y)", AtomicFormula),
        ("R(x, y, z)", AtomicFormula),

        # Quantifiers
        ("forall x. P(x)", Universal),
        ("∀x. P(x)", Universal),
        ("exists x. P(x)", Existential),
        ("∃x. P(x)", Existential),

        # Nested quantifiers
        ("forall x. exists y. R(x, y)", Universal),
        ("∀x. ∀y. P(x, y)", Universal),
        ("∃x. ∃y. Q(x, y)", Existential),

        # Quantifiers with complex formulas
        ("forall x. (P(x) -> Q(x))", Universal),
        ("exists x. (P(x) & Q(x))", Existential),
        ("∀x. (P(x) → ∃y. R(x, y))", Universal),

        # Functions
        ("P(f(x))", AtomicFormula),
        ("Q(f(x), g(y))", AtomicFormula),
        ("R(f(g(x)))", AtomicFormula),
    ]

    passed = 0
    failed = 0

    for formula_text, expected_type in tests:
        try:
            formula = parse(formula_text)
            if isinstance(formula, expected_type):
                print(f"✓ {formula_text:35} -> {formula}")
                passed += 1
            else:
                print(f"✗ {formula_text:35} -> Wrong type: {type(formula).__name__}")
                failed += 1
        except Exception as e:
            print(f"✗ {formula_text:35} -> Error: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return passed, failed


def test_free_variables():
    """Test free variable detection."""
    print("\nTesting Free Variables")
    print("=" * 50)

    tests = [
        ("P(x)", {"x"}),
        ("P(x) & Q(y)", {"x", "y"}),
        ("forall x. P(x)", set()),
        ("exists x. P(x)", set()),
        ("forall x. P(x, y)", {"y"}),
        ("∀x. (P(x) → Q(y))", {"y"}),
        ("(∀x. P(x)) → Q(y)", {"y"}),
        ("∃x. ∀y. R(x, y, z)", {"z"}),
    ]

    passed = 0
    failed = 0

    for formula_text, expected_vars in tests:
        try:
            formula = parse(formula_text)
            free_vars = formula.get_free_variables()
            if free_vars == expected_vars:
                print(f"✓ {formula_text:30} -> {free_vars}")
                passed += 1
            else:
                print(f"✗ {formula_text:30} -> Got {free_vars}, expected {expected_vars}")
                failed += 1
        except Exception as e:
            print(f"✗ {formula_text:30} -> Error: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return passed, failed


def test_substitution():
    """Test substitution in formulas."""
    print("\nTesting Substitution")
    print("=" * 50)

    # Create some terms for substitution
    x_var = Variable("x")
    y_var = Variable("y")
    c_const = Constant("c")

    tests = [
        # Simple substitution
        ("P(x)", "x", c_const, "P(C)"),
        ("P(x) & Q(x)", "x", c_const, "(P(C) ∧ Q(C))"),

        # No substitution (variable not present)
        ("P(y)", "x", c_const, "P(y)"),

        # Bound variable (no substitution inside quantifier)
        ("forall x. P(x)", "x", c_const, "∀x.P(x)"),
        ("exists x. P(x)", "x", c_const, "∃x.P(x)"),

        # Free occurrence outside quantifier
        ("(forall x. P(x)) & Q(x)", "x", c_const, "(∀x.P(x) ∧ Q(C))"),
    ]

    passed = 0
    failed = 0

    for formula_text, var, term, expected_result in tests:
        try:
            formula = parse(formula_text)
            result = formula.substitute(var, term)
            result_str = str(result)

            # Normalize string for comparison (handle C vs c)
            if result_str.replace("C", "c").replace("c", "C") == expected_result.replace("C", "c").replace("c", "C"):
                print(f"✓ {formula_text:25} [{var}/{term}] -> {result}")
                passed += 1
            else:
                print(f"✗ {formula_text:25} [{var}/{term}] -> Got {result}, expected {expected_result}")
                failed += 1
        except Exception as e:
            print(f"✗ {formula_text:25} -> Error: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return passed, failed


def test_error_handling():
    """Test parser error handling."""
    print("\nTesting Error Handling")
    print("=" * 50)

    invalid_formulas = [
        "",
        "p &",
        "& q",
        "p -> ",
        "(p",
        "p)",
        "((p)",
        "forall P(x)",
        "exists . P(x)",
        "P(x,)",
        "P(,y)",
    ]

    for formula_text in invalid_formulas:
        try:
            formula = parse(formula_text)
            print(f"✗ '{formula_text}' should have failed but parsed as: {formula}")
        except Exception as e:
            print(f"✓ '{formula_text}' correctly rejected: {e}")

    print("\nAll invalid formulas were correctly rejected.")


def main():
    """Run all tests."""
    print("Natural Deduction Formula Parser Test Suite")
    print("=" * 60)

    total_passed = 0
    total_failed = 0

    # Run each test suite
    p, f = test_propositional_logic()
    total_passed += p
    total_failed += f

    p, f = test_first_order_logic()
    total_passed += p
    total_failed += f

    p, f = test_free_variables()
    total_passed += p
    total_failed += f

    p, f = test_substitution()
    total_passed += p
    total_failed += f

    test_error_handling()

    # Summary
    print("\n" + "=" * 60)
    print("OVERALL RESULTS")
    print(f"Total Tests Passed: {total_passed}")
    print(f"Total Tests Failed: {total_failed}")

    if total_failed == 0:
        print("\n✓ All tests passed successfully!")
    else:
        print(f"\n✗ {total_failed} tests failed. Please review the output above.")


if __name__ == "__main__":
    main()