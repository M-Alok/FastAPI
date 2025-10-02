from fastapi import FastAPI
from .import models, database
from .routes import blog, user, auth

app = FastAPI()

get_db = database.get_db

models.Base.metadata.create_all(database.engine)

app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(user.router)