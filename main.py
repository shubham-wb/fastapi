from http.client import HTTPException
from typing import Optional, Union

from fastapi import Body, FastAPI, Response, status
from pydantic import BaseModel
from random import randrange
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


class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None
    published: bool = True

my_posts = [{"title":"title of post 1","content":"content of post 1", "id":1}]


@app.get("/hello") 
# decorator
def say_hello():
    return {"message":"Hello World"}

@app.get("/posts")
def get_posts():
    return {"data":"This is your posts"}

@app.get("/posts/{id}")
def get_post(id:int,response:Response):
    for post in my_posts:
        if post['id'] == id:
            return {"post_detail":post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND 
    # return {"message": "post not found"}

@app.post("/create-posts")
def create_posts(payload:Post):
    post_dict = payload.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    
    return {"message":"Successfully created post!", "data":post_dict}    

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"post_detail":post}

@app.delete("/posts/{id}")
def delete_post(id:int):
    for i, post in enumerate(my_posts):  #enumerate gives a tuple  (index, post)
        if post['id'] == id:
            my_posts.pop(i)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")