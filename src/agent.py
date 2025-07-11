import os
from openai import OpenAI
import json
from src.verifier import verify_step
from src.latex_renderer import render_to_latex

# Ensure you have OPENAI_API_KEY in your environment variables
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_solution_steps(problem: str) -> list:
    """Calls the LLM to break down the problem into structured steps."""
    
    # This JSON schema guides the LLM to produce the desired output format.
    function_schema = {
        "name": "log_solution_steps",
        "description": "Log the steps taken to solve a math problem.",
        "parameters": {
            "type": "object",
            "properties": {
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "rationale": {"type": "string", "description": "The reasoning for this step."},
                            "expression": {"type": "string", "description": "The resulting SymPy-parsable mathematical expression for this step."}
                        },
                        "required": ["rationale", "expression"]
                    }
                }
            },
            "required": ["steps"]
        }
    }

    prompt = f"""
    Solve the following math problem step-by-step. For each step, provide the reasoning (rationale) and the resulting mathematical expression.
    The final expression should be the solution. Ensure all expressions are SymPy-parsable.
    Problem: "{problem}"
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo", # Or another capable model
        messages=[{"role": "user", "content": prompt}],
        functions=[function_schema],
        function_call={"name": "log_solution_steps"}
    )
    
    args = json.loads(response.choices[0].message.function_call.arguments)
    return args.get("steps", [])


def solve_problem(problem: str) -> dict:
    """
    Full pipeline: generates, verifies, and renders a solution.

    Returns:
        A dictionary containing the LaTeX doc and verification log.
    """
    print("1. Generating solution steps with LLM...")
    all_steps = generate_solution_steps(problem)
    
    if not all_steps:
        return {"error": "Could not generate solution steps."}

    print("2. Verifying each step...")
    verified_steps = []
    verification_log = []
    
    # The first expression is the starting point
    previous_expr = problem 
    
    for step in all_steps:
        current_expr = step['expression']
        # The verification compares the result of the *previous* step to the *current* one.
        verification_result = verify_step(previous_expr, current_expr)
        
        step_with_verification = step.copy()
        step_with_verification['verification'] = verification_result
        
        verified_steps.append(step_with_verification)
        verification_log.append(verification_result['verified'])
        
        # Update the previous expression for the next iteration
        previous_expr = current_expr

    print("3. Rendering final LaTeX document...")
    latex_output = render_to_latex(problem, verified_steps)

    return {
        "latex_document": latex_output,
        "verification_log": verification_log,
        "verified_steps_ratio": sum(verification_log) / len(verification_log) if verification_log else 0
    }