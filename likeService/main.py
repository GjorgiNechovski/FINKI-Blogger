from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

import requests


import models
from config import GET_USER_URL, EMAIL_URL
from database import engine, SessionLocal
from pydanticModels import User
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


@app.post("/like")
def like_post(blog_id: int, token: str = Depends(get_token_authorization), db: Session = Depends(get_db)):
    user_url = GET_USER_URL
    email_url = EMAIL_URL

    response = requests.get(user_url, headers={"Authorization": token})

    if response.status_code == 200:
        user_data = response.json()
        user = User.parse_obj(user_data)

        blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        existing_like = db.query(models.Like).filter(models.Like.blog_id == blog_id, models.Like.user_id == user.id).first()
        if existing_like:
            db.delete(existing_like)
            blog.number_of_likes = blog.number_of_likes - 1 if blog.number_of_likes > 0 else 0
            db.commit()
            return JSONResponse(status_code=200, content={"message": "Blog unliked successfully"})

        new_like = models.Like(blog_id=blog_id, user_id=user.id)
        db.add(new_like)

        blog.number_of_likes = models.Blog.number_of_likes + 1 if blog.number_of_likes else 1
        db.commit()

        if blog.number_of_likes == 1 or blog.number_of_likes == 10 or blog.number_of_likes == 100:
            email_message = f"Your post has managed to get {blog.number_of_likes} likes"
            email_header = "New Like Notification"
            recipient_email = user.email

            print(recipient_email)

            requests.post(
                email_url + "/email",
                json={
                    "email": recipient_email,
                    "header": email_header,
                    "message": email_message
                }
            )

        return JSONResponse(status_code=200, content={"message": "Blog liked successfully"})

    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch user information")

