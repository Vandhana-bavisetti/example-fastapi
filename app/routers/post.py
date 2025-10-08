from .. import models,schemas
from  fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import engine,get_db
from typing import List,Optional
from . import oauth2
from sqlalchemy import func


router = APIRouter(prefix="/posts",tags=['posts'])

@router.get("/")
def get_posts(db:Session=Depends(get_db),current_user:dict=Depends(oauth2.get_current_user),Limit:int =10,skip:int=0,search:Optional[str]=""):
    #cursor.execute(""" SELECT * FROM posts """)
    #cursor.execute(""" SELECT * FROM posts """)
    #posts=cursor.fetchall()
    #print(posts)
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    #posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    results= db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id==models.Post.id,isouter=True).group_by(models.Post.id).all()
    return results

"""@app.get("/sqlalchemy")
def test_posts(db:Session = Depends(get_db)):
    posts= db.query(models.Post).all()
    return{"status":posts}"""


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def createposts(post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

   #cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) returning * """,(post.title,post.content,post.published))
   #new_post=cursor.fetchone()
   #conn.commit()
   
   print(current_user.id)
   new_post= models.Post(owner_id=current_user.id,**post.dict())
   db.add(new_post)
   db.commit()
   db.refresh(new_post)

   return new_post

    #return{"post" : f"title {payload['title']} content : {payload['content']}" }


"""@router.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return{"detail":post} """

#getting induvidual post
@router.get("/{id}",response_model=schemas.Post)
def get_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    
     #cursor.execute(""" SELECT * FROM posts WHERE id= %s """,(str(id),))
     #post =cursor.fetchone()
     #print(post)

     
     post= db.query(models.Post).filter(models.Post.id ==id).first()
     
     
     
     if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} wast not found")
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return{'message':f"post with id:{id} was not found"}
     
     return post

#delete a particular id in the my_posts
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post_id(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """,(str(id),))
    #delete_post=cursor.fetchone()
    #conn.commit()
    post = db.query(models.Post).filter(models.Post.id== id)
    post_query = post.first()

    if post_query == None:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    #  my_posts.pop(index)
    print(current_user.id)
    if post_query.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform action")
    db.delete(post_query)
    db.commit()
    #return does not work when using status code 204
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update the post
@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s,content=%s,published=%s WHERE id=%s returning *""",(post.title,post.content,post.published,str(id),))
    #updated_post=cursor.fetchone()
    #conn.commit()
    post_query= db.query(models.Post).filter(models.Post.id == id)
    post= post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} is not avialable")
    """post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict
    print(post)
    return{"updated post":post_dict}"""
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform action")

    post_query.update(updated_post.dict(),synchronize_session=False)

    db.commit()

    return post_query.first()