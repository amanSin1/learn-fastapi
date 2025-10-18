from fastapi import FastAPI, Body,status
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import  models,  schemas, utils, oauth2
from ..database import  engine, get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
   
)










# @app.get("/posts")
# def get_posts():
#     return {"data" : "this is your post"}


# @app.post("/create_posts")
# def create_posts():
#     return {"data" : "post created"}


# @app.post("/create_posts")
# def create_posts(payload: dict = Body(...)): 
#     print(payload)
#     title = payload.get("title")
#     content = payload.get("content")
#     print(title)
#     print(content)
#     return {"data" : "post created"}

# @app.post("/create_posts")
# def create_post(payload: Post):
#     print(payload)
#     print(payload.title)
#     return {"success" : "post created"}

# @app.post("/posts")
# def create_post(payload: Post):
#     print(payload)
#     print(payload.title)
#      # Access nested Author fields
#     print("Author Name:", payload.author.name)
#     print("Author Email:", payload.author.email)
#     data = payload.model_dump() # Convert to dictionary
#     if payload.ispublished:
#         print("Post is published")
#         return{
#             "data" : data,
#             "success" : "post created"
#         }
#     else: 
#         print("Post is not published")

#     return {"failed" : "post not created"}

# @app.get("/posts")
# def get_post():
#     cursor.execute(""" SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     print(posts)
#     return {"data": posts}

@router.get("/", response_model=list[schemas.PostOut])
def get_post(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    result = (
    db.query(
        models.Post ,                    # posts.id
        func.count(models.Vote.post_id).label("votes")  # COUNT(votes.post_id)
    )
    .outerjoin(models.Vote, models.Post.id == models.Vote.post_id)  # LEFT JOIN votes
    .group_by(models.Post.id)              # GROUP BY posts.id
    .all()
)
    print(result)
    
    return result 
    

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(payload : Post):
#     print(payload)
#     # title = payload.title
#     # content = payload.content
#     # id = payload.id
#     post_dict = payload.model_dump()
#     my_posts.append(post_dict)
#     #my_posts.append({"title" : title, "content": content, "id": id})
#     return {"data" : my_posts}

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(payload : Post):
#     cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s,%s) RETURNING * """,(payload.title,payload.content, payload.published))
#     new_post = cursor.fetchone() # fetchone() returns the inserted record
#     conn.commit() # to save the changes in the database
    
#     return {"data" : new_post}

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(payload : Post, db: Session = Depends(get_db)):
#     new_post =  models.Post(title = payload.title, content = payload.content, published = payload.published)
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post) # to get the latest data from the database
#     return {"data" : new_post}

#Instead of manually mapping each field like:title = payload.title,you can unpack the Pydantic model’s dictionary with **:
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(payload: schemas.PostBase, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    post_dict = payload.model_dump()
    print(current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post_dict)  # clean & scalable
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post 


# @app.get("/posts/latest")
# def get_post():
#     post = my_posts[1]
#     return {"data": post}

 
# @app.get("/posts/{id}")
# def get_post(id : int):
#     # for post in my_posts:
#     #     if post["id"] == id:
#     #         return {"data" : post}
#     # return {"message" : "post not found"}
#     post = next((post for post in my_posts if post["id"] == id), None)
#     if post is None:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return {"data": post}

# @app.get("/posts/{id}")
# def get_post(id : int):
#     cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(id,)) # comma is necessary to make it a tuple

#     your_post = cursor.fetchone() # fetchone() returns a single record or None if no record is found
#     if your_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {id} not found")
#     return {"data" : your_post}

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id : int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    #post = db.query(models.Post).filter(models.Post.id == id).first()
     
    post = (db.query(
        models.Post,                    # posts.id
        func.count(models.Vote.post_id).label("votes")  # COUNT(votes.post_id)
    )
    .outerjoin(models.Vote, models.Post.id == models.Vote.post_id)  # LEFT JOIN votes
    .group_by(models.Post.id)
    .filter(models.Post.id == id)
    .first())
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id : {id} not found")
    return  post
     
    

    
# @app.delete("/posts/{id}")
# def delete_post(id : int):
#     # for post in my_posts:
#     #     if post["id"] == id:
#     #         my_posts.remove(post)
#     #         return {"message" : "post deleted successfully"}
#     # return {"message" : "post not found"}
#     post = next((post for post in my_posts if post["id"] == id), None)

#     if post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {id} not found")
#     my_posts.remove(post)
#     raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Post with id : {id} deleted successfully")


# @app.delete("/posts/{id}")
# def delete_post(id : int):
#     cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(id,)) # comma is necessary to make it a tuple
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if deleted_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {id} not found")
#     raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Post with id : {id} deleted successfully")

@router.delete("/{id}")
def delete_post(id : int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    db.delete(post)
    db.commit() 
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Post with id : {id} deleted successfully")


# @app.put("/posts/{id}")
# def update_post(id:int, payload: UpdatePost):
#     post = next((post for post in my_posts if post["id"] == id), None)
#     if post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {id} not found")
    
#     post_index = my_posts.index(post)
#     updated_post = payload.model_dump()
#     updated_post["id"] = id
#     my_posts[post_index] = updated_post
    
   
#     return {"data" : my_posts[post_index]}

# @app.put("/posts/{id}")
# def update_post(id:int, payload: UpdatePost):
#     cursor.execute(""" UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING * """,(payload.title, payload.content, id))
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post is None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id : {id} not found")
#     return {"data" : updated_post}

@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    payload: schemas.UpdatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    # Convert payload into a dict and remove None values
    update_data = payload.model_dump(exclude_unset=True)

    # Update only provided fields
    post_query.update(update_data, synchronize_session=False)
    db.commit()
    return post_query.first()

    # post_query.update(payload.model_dump(), synchronize_session=False)
    # db.commit()
    # return {"data": post_query.first()}