from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import items, auth_routes
from crud import *
from auth import auth_middleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.middleware("http")(auth_middleware)

app.include_router(auth_routes.router)
app.include_router(items.router)

@app.get('/login')
async def login():
    return FileResponse('static/login.html')

@app.get('/register')
async def register():
    return FileResponse('static/register.html')

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')
