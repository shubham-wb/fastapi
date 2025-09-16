from fastapi import FastAPI, Path

app = FastAPI()

inventory = {
    1: {
        "name":"Milk",
        "price":3.99,
        "brand":"Amul"
    }
}


@app.get("/get-item/{item_id}/{name}")
def get_item(item_id:int = Path( description="The ID of the item to retrieve"), name:str = Path(description="The name of the item to retrieve")):
    item = inventory.get(item_id, {"error": "Item not found"})
    if item.get("name") == name:
        return item
    return {"error": "Item not found"}


@app.get("/get-by-name")
def get_item(name:str):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    return {"error": "Item not found"}