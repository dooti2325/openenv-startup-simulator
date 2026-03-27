from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from models import Action
from env import StartupEnv
from baseline import run_baseline
from grader import evaluate
from tasks import get_tasks

app = FastAPI(title="Startup Survival Simulator API")

@app.get("/")
def read_root():
    return RedirectResponse(url='/docs')
    
# Global environment instance for simple stateful API
game_env = StartupEnv()

class ActionRequest(BaseModel):
    action: Action

@app.get("/reset")
def reset():
    state = game_env.reset()
    return state.dict()

@app.post("/step")
def step(req: ActionRequest):
    try:
        new_state, reward, done, info = game_env.step(req.action)
        return {
            "state": new_state,
            "reward": reward,
            "done": done,
            "info": info
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/state")
def get_state():
    return game_env.state().dict()

@app.get("/tasks")
def tasks():
    return get_tasks()

@app.get("/grader")
def grader(task: str = "survival"):
    tasks_list = get_tasks()
    if task not in tasks_list:
        raise HTTPException(status_code=400, detail="Invalid task")
    
    score = evaluate(task, game_env.history)
    return {"score": score}

@app.get("/baseline")
def baseline():
    # Evaluate the baseline agent across all tasks
    history = run_baseline(StartupEnv)
    
    scores = {}
    for task in get_tasks():
        scores[task] = evaluate(task, history)
        
    return scores

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)

if __name__ == "__main__":
    main()
