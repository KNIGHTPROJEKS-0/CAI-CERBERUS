from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(title="CAI-CERBERUS API")

class TaskRequest(BaseModel):
    task: str
    target: str
    agent_type: str = "reconnaissance"

@app.get("/")
def root():
    return {"message": "CAI-CERBERUS API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/execute")
async def execute_task(request: TaskRequest):
    return {
        "task_id": f"task_{hash(request.task)}",
        "status": "completed",
        "target": request.target,
        "findings": f"Reconnaissance completed for {request.target}"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)