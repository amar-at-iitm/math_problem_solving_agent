from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from src.agent import solve_problem

app = FastAPI(
    title="Mathematical Problem-Solving Agent",
    description="An API for solving and verifying math problems."
)

class ProblemRequest(BaseModel):
    problem: str

class SolutionResponse(BaseModel):
    latex_document: str
    verification_log: list
    verified_steps_ratio: float

@app.post("/solve", response_model=SolutionResponse)
def solve(request: ProblemRequest):
    """
    Accepts a math problem, solves it, verifies the steps, and returns a LaTeX document.
    
    **Example Problem**: `Expand (x+y)**2`
    """
    result = solve_problem(request.problem)
    if "error" in result:
        return {"error": result["error"]}, 400
    return result

# To run this API, save it as `api.py` in the `src` folder and run:
# uvicorn src.api:app --reload