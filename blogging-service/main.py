from datetime import datetime

import requests

from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, joinedload
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

import zookeeper
from database import engine, SessionLocal

import models
from pydanticModels import User, BlogPydantic, BlogDetails
from utils import get_token_authorization

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


zk_client = None
service_port = None


@app.on_event("startup")
async def startup_event():
    global zk_client, service_port
    zk_client = zookeeper.connect_to_zookeeper()
    service_port = zookeeper.register_service(zk_client)
    app.port = service_port


@app.on_event("shutdown")
async def shutdown_event():
    if zk_client:
        zk_client.stop()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=service_port)


@app.get("/getBlogs")
async def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return JSONResponse(content=jsonable_encoder(blogs))


@app.post("/createBlog")
async def create_blog(blog: BlogPydantic, token: str = Depends(get_token_authorization), db: Session = Depends(get_db)):
    user_url = "http://host.docker.internal:8090/api/getUser"

    response = requests.get(user_url, headers={"Authorization": token})

    if response.status_code == 200:
        user_data = response.json()
        user = User.parse_obj(user_data)

        new_blog = models.Blog(
            user_id=user.id,
            title=blog.title,
            blog_text=blog.blog_text,
            date_created=datetime.now(),
            number_of_likes=0
        )

        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)

        blog_dict = jsonable_encoder(new_blog)

        return JSONResponse(content=blog_dict)

    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch user information")


@app.get("/blogDetails/{blog_id}", response_model=BlogDetails)
async def get_blog_details(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    blog_dict = blog.__dict__

    blog_dict.pop('_sa_instance_state')

    comments = db.query(models.Comment).filter(models.Comment.blog_id == blog_id).all()

    comments_list = []
    for comment in comments:
        comment_dict = comment.__dict__
        comment_dict.pop('_sa_instance_state')
        comments_list.append(comment_dict)

    blog_dict['comments'] = comments_list

    return blog_dict


@app.post("/deleteBlog/{blog_id}")
async def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog)
    db.commit()

    return JSONResponse(status_code=200, content={"message": "Blog deleted successfully"})
