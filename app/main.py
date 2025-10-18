from http.client import HTTPException
from typing import Optional, Union
import os

from fastapi import Body, FastAPI, Response, status
from pydantic import BaseModel
from random import randrange
from enum import Enum 
import psycopg2
import time 
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


# Import Enum and create a sub-class that inherits from str and from Enum.

# Load environment variables
load_dotenv()


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello":"World"}


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

my_posts = [{"title":"title of post 1","content":"content of post 1", "id":1}]

while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("connected to database")
        break
    except Exception as error:
        print("Error while connecting to database", error)
        time.sleep(2)

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":posts}

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
    cursor.execute("""INSERT INTO posts(title,content,published,created_at) VALUES(%s,%s,%s,%s)""", (post_dict['title'], post_dict['content'], post_dict['published'], time.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    return {"message":"Successfully created post!", "data":post_dict}

@app.get("/posts/{id}")
def get_post(id:int):
    print("ID is ", id)
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    post = cursor.fetchone()
    return {"post_detail":post}

@app.delete("/posts/{id}")
def delete_post(id:int):
    for i, post in enumerate(my_posts):  #enumerate gives a tuple  (index, post)
        if post['id'] == id:
            my_posts.pop(i)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")


@app.put("/posts/{id}")
def update_post(id:int, payload:Post):
    for i, post in enumerate(my_posts):  #enumerate gives a tuple  (index, post)
        if post['id'] == id:
            post_dict = payload.dict()
            post_dict['id'] = id
            my_posts[i] = post_dict
            return {"message":"Successfully updated post!", "data":post_dict}    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")


#database integration