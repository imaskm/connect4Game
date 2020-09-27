from fastapi import FastAPI
from database import  base
from routers import game

base.Base.metadata.create_all(bind=base.engine)

app = FastAPI()


app.include_router(
    game.router,
    tags = ["game"]
)