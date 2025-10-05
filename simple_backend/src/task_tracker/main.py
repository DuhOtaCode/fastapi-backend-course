from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json, os

app = FastAPI()
FILE = "tasks.json"

class Task(BaseModel):
    id: int
    title: str
    status: str

class TaskCreate(BaseModel):
    title: str
    status: str = "todo"


def load():
    if not os.path.exists(FILE) or os.path.getsize(FILE) == 0:
        save([])
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            save([]); return []

def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.get("/tasks")
def get_tasks():
    return load()


@app.post("/tasks")
def create_task(task: TaskCreate):
    data = load()
    new_id = max((t["id"] for t in data), default=0) + 1
    item = {"id": new_id, **task.dict()}
    data.append(item)
    save(data)
    return item


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate):
    data = load()
    for t in data:
        if t["id"] == task_id:
            t.update(task.dict())
            save(data)
            return t
    raise HTTPException(404, "Задача не найдена")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    data = load()
    for i, t in enumerate(data):
        if t["id"] == task_id:
            data.pop(i)
            save(data)
            return {"message": "Задача удалена"}
    raise HTTPException(404, "Задача не найдена")