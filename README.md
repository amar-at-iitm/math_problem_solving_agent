# Mathematical Problem-Solving Agent with Proof Checking

A robust agent that solves mathematical problems and formally verifies each step of its reasoning using a Computer Algebra System (CAS). This project bridges the gap between Large Language Model (LLM) reasoning and formal mathematical correctness.

-----

## Problem Statement

The goal is to build an agent that can:

1.  Accept a mathematical problem in plain text (e.g., algebra, calculus, discrete proofs).
2.  Generate a human-readable, step-by-step solution.
3.  Rigorously verify each step in the solution using symbolic checks with **SymPy**.
4.  Produce a final, verified proof as a polished $\\LaTeX$ document, complete with verification annotations.

The agent must explicitly flag any step it cannot symbolically verify, suggesting alternative numerical checks.

-----

## Key Features

  * **Step-by-Step Solution Generation**: Breaks down complex problems into a logical chain of thought.
  * **Symbolic Verification**: Uses SymPy to check algebraic manipulations, derivatives, integrals, and logical equivalences.
  * **Formal $\\LaTeX$ Output**: Generates a high-quality PDF document of the solution, with verification status noted in the margins for each step.
  * **Machine-Readable Logs**: Outputs a structured log (`True`/`False`) for each verification attempt.
  * **Fallback Checks**: Flags unverified steps and suggests numerical checks as an alternative.
  * **API Access**: Provides a simple FastAPI interface to submit problems and retrieve results.

-----

## Architecture

The agent operates using a two-stage flow designed to separate reasoning from verification.

**Stage A: Generation**
The LLM receives the problem and generates a structured plan. This plan is a JSON object containing a list of steps, where each step includes the mathematical expression and the rationale behind it. This is achieved via structured output or function-calling.

**Stage B: Verification**
The Verifier module parses the structured output from the LLM. For each step, it invokes SymPy to perform the appropriate symbolic check. The result of each check (True/False) is recorded.

This entire process is orchestrated by an agent that manages the flow and compiles the final outputs.

```mermaid
graph TD
    A[Start: User submits problem text] --> B{Agent Orchestrator};
    B --> C[Stage A: LLM generates structured solution steps (JSON)];
    C --> D{Verifier Module};
    D --> E[For each step, run SymPy check];
    E --> F{Verification Result};
    F --> G[Annotate Step: Verified / Unverified];
    G --> B;
    B --> H[Compile Final Outputs];
    H --> I[1. LaTeX Document];
    H --> J[2. Verification Log];
    H --> K[3. Jupyter Notebook (Optional)];
```

-----

## Project Structure

```
/math-agent/
  README.md
  requirements.txt
  /src
    agent.py             # Main agent orchestrator
    verifier.py          # SymPy verification logic
    api.py               # FastAPI application
    latex_renderer.py    # Renders the LaTeX output
  /tests
    problems.json        # Benchmark problem set
  /notebooks/
    symbolic_checks.ipynb # Notebook for development and testing
```

-----

## Getting Started

### Prerequisites

  * Python 3.9+
  * A TeX distribution (like MiKTeX, TeX Live) for rendering $\\LaTeX$ to PDF.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/amar-at-iitm/math_problem_solving_agent
    cd math-agent
    ```

2.  **Create and activate a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory and add your API keys (e.g., for the LLM provider).

    ```
    OPENAI_API_KEY="your_api_key_here"
    ```

### Running the API

Launch the FastAPI server from the `/src` directory:

```bash
uvicorn api:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

-----

## Usage

You can interact with the agent through the API endpoint.

**Endpoint**: `POST /solve`

**Request Body**:

```json
{
  "problem": "Calculate the derivative of x^3 * sin(x) with respect to x."
}
```

**Example `curl` Request**:

```bash
curl -X POST "http://127.0.0.1:8000/solve" \
-H "Content-Type: application/json" \
-d '{"problem": "Calculate the derivative of x^3 * sin(x) with respect to x."}'
```

**Expected Output**:
The API will return a JSON object containing URLs or base64-encoded strings for:

1.  The final $\\LaTeX$ document.
2.  The machine-readable verification log.
3.  (Optional) An executable Jupyter notebook.

-----

## Evaluation & Benchmarks

The agent's performance is evaluated against a curated set of 50 problems from algebra, calculus, and combinatorics, located in `/tests/problems.json`.

### Metrics

1.  **Verified Step Ratio**: The primary metric. Measures the ratio of symbolically verified steps to the total number of steps.
    $$\text{Verified Step Ratio} = \frac{\text{Number of Verified Steps}}{\text{Total Number of Steps}}$$
2.  **Correct Final Answer Rate**: Percentage of problems where the final answer matches the ground truth.
3.  **False Verification Rate**: The rate at which SymPy incorrectly confirms a step (`True` for a false assertion). This should be negligible.
4.  **Human Readability**: Assessed subjectively based on the clarity and logical flow of the generated $\\LaTeX$ output.


