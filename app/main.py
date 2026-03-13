from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from routers import items, auth_routes
from crud import *
from auth import auth_middleware, get_current_user


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

@app.get('/logout')
async def logout(response: Response):
    response = RedirectResponse('/login', status_code=303)
    response.delete_cookie(key='access_token', path='/')
    return response

@app.get("/")
async def read_index(current_user: dict = Depends(get_current_user)):
    return FileResponse('static/index.html')

@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def auth_exception_handler(request: Request, exe: HTTPException):
    return RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)