import os
 
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Depends
import psycopg2
import time 
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from . import models
from sqlalchemy.orm import Session 
from .database import engine, get_db
# Import Enum and create a sub-class that inherits from str and from Enum.
from .schemas import Post,PostCreate,PostBase
models.Base.metadata.create_all(bind=engine)


# Load environment variables
load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello":"World"}
 
  
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
    posts = db.query(models.PostBase).all()
    return {"data":posts}

@app.get("/posts/{id}")
def get_post(id: int,db:Session = Depends(get_db)):
    print("ID is ", id)
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()
    
    post = db.query(models.PostBase).filter(models.PostBase.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    return {"post_detail": post}

@app.post("/posts",response_model=Post)
def create_posts(post: PostBase, db:Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *""", 
    #                (payload.title, payload.content, payload.published))
    # new_post = cursor.fetchone()
    # conn.commit()
#    new_post = models.PostBase(title=post.title, content=post.content, published=post.published)
   new_post = models.PostBase(**post.dict())
   db.add(new_post)
   db.commit() 
   db.refresh(new_post) 
   return {"message": "Successfully created post!", "data": new_post}

@app.delete("/posts/{id}")
def delete_post(id: int, db:Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    
    post = db.query(models.PostBase).filter(models.PostBase.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post.delete(synchronize_session=False)

    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, payload: PostBase,db:Session=Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s 
    #                   WHERE id = %s RETURNING *""", 
    #                (payload.title, payload.content, payload.published, id))
    # updated_post = cursor.fetchone()
    
    post_query = db.query(models.PostBase).filter(models.PostBase.id == id)

    post = post_query.first()
    
    if  post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    post_query.update(payload.dict(),synchronize_session=False)
    # conn.commit()
    db.commit()
    return {"message": "Successfully updated post!", "data": post_query.first()}


#database integration