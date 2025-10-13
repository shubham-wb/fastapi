from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from enum import Enum 

# Import Enum and create a sub-class that inherits from str and from Enum.

class ModelName(str , Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

class Item(BaseModel):
    name : str
    price: float
    is_offer:Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.get("/items/{item_id}")
def read_item(item_id:int, q:Union[str,None] = None):
    return {"item_id":item_id, "q":q}


@app.put("/items/{item_id}")
def update_item(item_id:int, item:Item):
    return {"item_price":item.price, "item_id":item_id}

@app.get("/models/{model_name}")
async def get_model(model_name:ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message":"Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message":"LeCNN all the images"}
    return {"model_name": model_name, "message":"Have some residuals"}

@app.get("/hello")
def say_hello():
    return {"message":"Hello World"}