from fastapi import FastAPI
from pydantic import BaseModel
import httpx # To call other agents/tools

app = FastAPI(
    title="Showrunner",
    description="Orchestrates the novel-writing process by routing tasks to specialized agents.",
    version="0.1.0"
)

# We can re-use the contract definitions later, for now a simple model
class Task(BaseModel):
    task_id: str
    goal: str

@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "ok"}

@app.post("/v1/tasks")
async def process_task(task: Task):
    """
    (Placeholder) Receives a task and orchestrates the workflow.

    In a real implementation, this would:
    1. Look up the project and session.
    2. Freeze the inputs into a "bundle".
    3. Call the appropriate agent (e.g., 'prose' agent) with a TaskEnvelope.
    4. Aggregate reviews and control canon bumps.
    """
    print(f"Showrunner received task: {task.goal}")

    # Example of calling another service (e.g., prose agent)
    # prose_agent_url = "http://prose:8000/v1/draft"
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(prose_agent_url, json=task.dict())
    #     print(f"Prose agent responded: {response.json()}")

    return {"status": "task received", "task_id": task.task_id}
