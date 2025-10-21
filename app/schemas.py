from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 

class PostCreate(PostBase):
    pass


"""The pass keyword means "do nothing" — it's simply a placeholder indicating that the class has no additional fields or logic beyond what it inherits from the parent class."""


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    
