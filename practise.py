from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
class post(BaseModel):
    title: str
    content :str
    published:bool=True
    rating:Optional[int] = None

app = FastAPI()

@app.post('/posts1')
def createposts(payload:post):
    print(payload.title)
    print(payload.rating)
    return{"data":payload}