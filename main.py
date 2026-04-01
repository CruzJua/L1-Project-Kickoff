from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    name: str
    id: int
    description: Optional[str] = None

    def __str__(self):
        return f"Item: {self.name}\nDescription: {self.description}"


# In-memory storage
items_db: dict[int, Item] = {}
next_id: int = 1


@app.get("/items")
def get_items() -> list[Item]:
    items = []
    for value in items_db.values():
        items.append(value)
    return items
    

@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = items_db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items")
def create_item(item: Item):
    global next_id
    items_db[next_id] = item
    next_id += 1
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return item
    

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return item


# Run with: uvicorn main:app --reload
