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
        if t.get("id") == task_id:
            title_changed = (task.title != t.get("title"))
            new_notes = task.notes if task.notes is not None else t.get("notes")
            if title_changed:
                new_notes = llm.explain(task.title)

            updated = {
                "id": task_id,
                "title": task.title,
                "status": task.status,
                "notes": new_notes,
            }
            data[i] = updated
            store.save(data)
            return updated

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

