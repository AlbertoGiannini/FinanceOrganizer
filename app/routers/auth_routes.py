from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import Response, RedirectResponse
from database import supabase_connection as supabase
from schemas import User

router = APIRouter(tags=['Authentication'])

templates = Jinja2Templates(directory="templates")

@router.get('/register')
async def register(request: Request):
    return templates.TemplateResponse(request, "register.html", context={"login": False})

@router.post('/signup')
async def signup(user: User, response: Response):
    try:
        breakpoint()
        auth_response = supabase.auth.sign_up({
            'email': user.email,
            'password': user.password
        })
        if auth_response.user is None:
            raise HTTPException(status_code=400, detail="Signup failed")
        if len(auth_response.user.identities) == 0:
            raise HTTPException(status_code=400, detail='User already exists')
        return RedirectResponse('/login', status_code=303)
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

@router.post('/login')
async def login(
    response: Response,
    request: Request,
    email: str = Form(...),
    password: str = Form(...)):
    try:
        user = User(email=email, password=password)
        auth_response = supabase.auth.sign_in_with_password({
            'email': user.email,
            'password': user.password
        })
        if auth_response is None:
            raise HTTPException(status_code=400, detail="Login failed")
        access_token = auth_response.session.access_token
        response =  RedirectResponse('/', status_code=303)
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
        return response

    except Exception as err:
        return templates.TemplateResponse(request, "login.html", context={"login": True, "error": err})

@router.get('/login')
async def login(request: Request):
    return templates.TemplateResponse(request, "login.html", context={"login": True})


@router.get('/logout')
async def logout(response: Response):
    response = RedirectResponse('/login', status_code=303)
    response.delete_cookie(key='access_token', path='/')
    return response
