from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(
    title="Prose Agent",
    description="Drafts scenes based on a provided bundle of inputs.",
    version="0.1.0"
)

class TaskEnvelope(BaseModel):
    # A simplified version of the contract for now
    task_id: str
    goal: str
    inputs: Dict[str, Any]

@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "ok"}

@app.post("/v1/draft")
async def draft_scene(task: TaskEnvelope):
    """
    (Placeholder) Receives a task envelope and drafts a scene.

    In a real implementation, this would:
    1. Use the openrouter-client to call an LLM.
    2. Pass the inputs (lore, voice, outline) to the LLM.
    3. Use the prompt template from the blueprint.
    4. Return an AgentReport with the generated artifact.
    """
    print(f"Prose agent received task: {task.goal}")

    # Placeholder for the generated markdown
    scene_md = f"---\nscene_id: placeholder\n---\n\nThis is a placeholder scene for goal: {task.goal}"

    # Placeholder for the AgentReport
    report = {
        "type": "report.v1",
        "task_id": task.task_id,
        "artifact": {
            "type": "scene_draft",
            "content": scene_md, # In reality, this would be a path to S3
            "meta": { "agent_role": "prose" }
        },
        "logs": ["Drafted scene using placeholder logic."],
        "needs": []
    }
    return report
