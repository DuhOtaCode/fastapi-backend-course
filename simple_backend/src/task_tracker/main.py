from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from storage import JsonBinStorage

app = FastAPI(title="Task Tracker — Stateless (jsonbin.io)")
store = JsonBinStorage()

class Task(BaseModel):
    id: int
    title: str
    status: str

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
    new_task = {"id": new_id, **task.dict()}
    data.append(new_task)
    store.save(data)
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate):
    data = store.load()
    for t in data:
        if t["id"] == task_id:
            t.update(task.dict())
            store.save(data)
            return t
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