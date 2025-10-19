from typing import Optional, Union
import os
 
from fastapi import Body, FastAPI, Response, status, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from random import randrange
from enum import Enum 
import psycopg2
import time 
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from . import models
from sqlalchemy.orm import Session 
from .database import engine, SessionLocal, get_db
# Import Enum and create a sub-class that inherits from str and from Enum.

models.Base.metadata.create_all(bind=engine)


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
def get_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data":posts}

@app.get("/posts/{id}")
def get_post(id: int):
    print("ID is ", id)
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    return {"post_detail": post}

@app.post("/posts")
def create_posts(post: Post, db:Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *""", 
    #                (payload.title, payload.content, payload.published))
    # new_post = cursor.fetchone()
    # conn.commit()
   new_post = models.Post(title=post.title, content=post.content, published=post.published)
   db.add(new_post)
   db.commit() 
   db.refresh(new_post) 
   return {"message": "Successfully created post!", "data": new_post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    deleted_post = cursor.fetchone()
    
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, payload: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s 
                      WHERE id = %s RETURNING *""", 
                   (payload.title, payload.content, payload.published, id))
    updated_post = cursor.fetchone()
    
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    conn.commit()
    return {"message": "Successfully updated post!", "data": updated_post}


#database integration