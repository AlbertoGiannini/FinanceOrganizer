from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
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

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.middleware("http")(auth_middleware)

app.include_router(auth_routes.router)
app.include_router(items.router)

@app.get("/")
async def read_index(request: Request, current_user: dict = Depends(get_current_user)):
    all_items = await items.get_all(current_user)
    total_amount = await items.total_amount(current_user)
    return templates.TemplateResponse(request, "home.html", context={"items": all_items, "total_amount": total_amount})

@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def auth_exception_handler(request: Request, exe: HTTPException):
    return RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)