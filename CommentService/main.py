from datetime import datetime
from http.client import HTTPException

import requests


from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

import models
from database import SessionLocal, engine
from pydanticModels import CommentPydantic, User
from utils import get_token_authorization

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create-comment")
async def create_comment(comment: CommentPydantic, token: str = Depends(get_token_authorization), db: Session = Depends(get_db)):
    user_url = "http://host.docker.internal:8080/api/getUser"

    response = requests.get(user_url, headers={"Authorization": token})

    if response.status_code == 200:
        user_data = response.json()
        user = User.parse_obj(user_data)

        blog = db.query(models.Blog).filter(models.Blog.id == comment.blog_id).first()

        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        new_comment = models.Comment(
            blog_id=comment.blog_id,
            user_id=user.id,
            comment_text=comment.comment_text,
            date_created=datetime.now()
        )

        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch user information")

    return JSONResponse(status_code=200, content={"message": "Comment added successfully"})


@app.post("/delete-comment")
async def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.comment_id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Blog not found")

    db.delete(comment)
    db.commit()

    return JSONResponse(status_code=200, content={"message": "Comment deleted successfully"})
