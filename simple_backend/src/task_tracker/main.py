from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from storage import JsonBinStorage
from cf_client import CloudflareLLM


app = FastAPI()
store = JsonBinStorage()
llm = CloudflareLLM()

class Task(BaseModel):
    id: int
    title: str
    status: str = "todo"
    notes: Optional[str] = None

class TaskCreate(BaseModel):
    title: str
    status: str = "todo"

@app.get("/tasks")
def get_tasks():
    return store.load()

@app.post("/tasks")
def create_task(task: TaskCreate):
    data = store.load()
    new_id = max((t["id"] for t in data), default=0) + 1
    notes = llm.explain(task.title)
    new_task = {"id": new_id, "title": task.title, "status": task.status, "notes": notes}
    data.append(new_task)
    store.save(data)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    data = store.load()
    for i, t in enumerate(data):
        if t["id"] == task_id:
            if task.notes is None:
                task.notes = t.get("notes")
            data[i] = task.model_dump()
            store.save(data)
            return data[i]
    raise HTTPException(404, "Задача не найдена")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    data = store.load()
    for i, t in enumerate(data):
        if t["id"] == task_id:
            data.pop(i)
            store.save(data)
            return {"message": "Задача удалена"}
    raise HTTPException(404, "Задача не найдена")

