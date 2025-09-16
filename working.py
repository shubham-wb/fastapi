from typing import Optional
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name : str
    price: float
    brand : Optional[str] = None


class UpdateItem(BaseModel):
    name : Optional[str] = None
    price: Optional[float] = None
    brand : Optional[str] = None


inventory = {
    1: {
        "name":"Milk",
        "price":3.99,
        "brand":"Amul"
    }
}


# Get item by ID
@app.get("/items/{item_id}")
def get_item_by_id(item_id: int = Path(..., description="The ID of the item to retrieve")):
    item = inventory.get(item_id)
    if item:
        return item
    return {"error": "Item not found"}


# Get item by name (query param)
@app.get("/items/")
def get_item_by_name(name: Optional[str] = None):
    if name is None:
        return {"error": "Name parameter is required"}
    for item in inventory.values():
        if item["name"].lower() == name.lower():
            return item
    return {"error": "Item not found"}


# Create a new item
@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"error": "Item ID already exists"}
    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id:int, item:UpdateItem):
    if item_id not in inventory:
        return {"Error":"Item ID does not exists."}
    inventory[item_id].update(item)
    return inventory[item_id]


@app.delete("/delete-item")
def delete_item(item_id:int = Query(...,description="The ID of the item to delete")):
    if item_id not in inventory:
        return {"Error":"ID does not exist."}
    
    del inventory[item_id]
    return {"Success":"Item deleted successfully."}