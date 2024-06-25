import os

import pika
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

import requests

import models
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

rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def send_email_message(email, header, message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port)
    )
    channel = connection.channel()

    channel.queue_declare(queue='like_events', durable=True)

    email_string = f"{email}|{header}|{message}"

    channel.basic_publish(exchange='',
                          routing_key='like_events',
                          body=email_string,
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))

    connection.close()


@app.post("/like")
def like_post(blog_id: int, token: str = Depends(get_token_authorization), db: Session = Depends(get_db)):
    user_url = "http://host.docker.internal:8090/api/getUser"

    response = requests.get(user_url, headers={"Authorization": token})

    if response.status_code == 200:
        user_data = response.json()
        user = User.parse_obj(user_data)

        blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        existing_like = db.query(models.Like).filter(models.Like.blog_id == blog_id,
                                                     models.Like.user_id == user.id).first()
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

            send_email_message(recipient_email, email_header, email_message)

        return JSONResponse(status_code=200, content={"message": "Blog liked successfully"})

    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch user information")
