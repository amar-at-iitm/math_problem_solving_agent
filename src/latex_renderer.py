def render_to_latex(problem: str, steps: list) -> str:
    """
    Renders the problem and its verified steps into a LaTeX document string.

    Args:
        problem: The original problem statement.
        steps: A list of step dictionaries, each including a verification status.

    Returns:
        A string containing a complete LaTeX document.
    """
    # LaTeX document preamble
    preamble = r"""
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{xcolor}
\usepackage{geometry}
\geometry{a4paper, margin=1in}

\newcommand{\verified}{\marginpar{\textcolor{green!70!black}{\checkmark \text{ Verified}}}}
\newcommand{\unverified}{\marginpar{\textcolor{red!80!black}{\textbf{?} \text{ Unverified}}}}

\begin{document}
"""

    # Problem title
    title = f"\\section*{{Problem: {problem}}}\n\\hrule\n"

    # Format each step
    body = ""
    for i, step in enumerate(steps):
        rationale = step.get('rationale', '').replace('_', '\\_')
        expression = step.get('expression', '')
        
        # Add verification status as a margin note
        verification_status = step.get('verification', {})
        status_cmd = r"\verified" if verification_status.get('verified') else r"\unverified"
        
        body += f"\\subsection*{{Step {i+1}: {rationale}}}\n"
        body += f"$$ {sympy.latex(sympy.sympify(expression))} {status_cmd} $$\n\n"
        if not verification_status.get('verified'):
            reason = verification_status.get('reason', 'No reason given.').replace('_', '\\_')
            body += f"\\textit{{\\textcolor{{red!80!black}}{{Note: {reason}}}}}\n\n"

    # Document ending
    end = r"\end{document}"

    return preamble + title + body + end

# Example Usage:
if __name__ == '__main__':
    import sympy
    # Dummy data for demonstration
    sample_problem = "Differentiate $x^2 + 3x$"
    sample_steps = [
        {
            "rationale": "Applying the sum rule for derivatives",
            "expression": "Derivative(x**2, x) + Derivative(3*x, x)",
            "verification": {"verified": True}
        },
        {
            "rationale": "Calculating the individual derivatives",
            "expression": "2*x + 3",
            "verification": {"verified": True}
        },
        {
             "rationale": "Incorrect simplification for demonstration",
             "expression": "2*x",
             "verification": {"verified": False, "reason": "Terms do not cancel."}
        }
    ]
    latex_doc = render_to_latex(sample_problem, sample_steps)
    print("--- LaTeX Output ---")
    print(latex_doc)