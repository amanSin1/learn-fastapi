from fastapi import FastAPI
from . import  models
from .database import  engine
from .routers import post, user,vote
from .routers import auth
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    # "http://www.google.com",
    # "http://www.youtube.com",
    "*"

]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"message": "Hello Worlddd"}  

# @app.get("/sqlalchemy")
# def test_post(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}
     
