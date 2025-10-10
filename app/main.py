from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import user


app = FastAPI()

origins = ["localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)

@app.get("/")
async def root():
    return {"success": "API is up and running!"}