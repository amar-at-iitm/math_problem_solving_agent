import sympy

def verify_step(before_expr: str, after_expr: str) -> dict:
    """
    Verifies if the transformation from before_expr to after_expr is valid.

    Args:
        before_expr: The mathematical expression before the step.
        after_expr: The mathematical expression after the step.

    Returns:
        A dictionary with verification status and a reason.
    """
    try:
        # Use sympify to convert string expressions to SymPy objects
        before = sympy.sympify(before_expr)
        after = sympy.sympify(after_expr)

        # The core verification logic:
        # If the simplified difference between the two expressions is zero,
        # they are symbolically equivalent.
        # We use .expand() and .simplify() to handle more cases robustly.
        if sympy.simplify(before - after) == 0:
            return {"verified": True, "reason": "Expressions are symbolically equivalent."}
        
        # Check for derivative correctness if applicable
        # This is a simple heuristic; a more advanced version would parse the rationale.
        if isinstance(before, sympy.Derivative):
             if before.doit() == after:
                 return {"verified": True, "reason": "Correct derivative calculation."}
                 
        # Check for integral correctness
        if isinstance(before, sympy.Integral):
            # Antiderivative check
            if sympy.diff(after) == before.function:
                return {"verified": True, "reason": "Correct antiderivative (integral)."}

        # If the above checks fail, the step is not verified.
        # A numeric check could be added here as a fallback.
        return {
            "verified": False,
            "reason": "Expressions are not symbolically equivalent. Could be a simplification step the verifier doesn't understand or an error."
        }

    except (sympy.SympifyError, TypeError, Exception) as e:
        return {"verified": False, "reason": f"Error during verification: {e}"}

# Example Usage:
if __name__ == '__main__':
    # Test case 1: Verified algebraic expansion
    step1 = verify_step("(x+1)**2", "x**2 + 2*x + 1")
    print(f"Step 1: (x+1)**2 -> x**2 + 2*x + 1 | Verification: {step1}")

    # Test case 2: Unverified/incorrect step
    step2 = verify_step("sin(x)", "cos(x)")
    print(f"Step 2: sin(x) -> cos(x) | Verification: {step2}")

    # Test case 3: Verified derivative
    step3 = verify_step("Derivative(x**2, x)", "2*x")
    print(f"Step 3: d(x**2)/dx -> 2*x | Verification: {step3}")