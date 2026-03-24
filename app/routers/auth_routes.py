from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import Response, RedirectResponse
from database import supabase_connection as supabase
from supabase import AuthError
from schemas import UserLogin, UserRegister, UserException

router = APIRouter(tags=['Authentication'])

templates = Jinja2Templates(directory="templates")

@router.get('/register')
async def register(request: Request):
    return templates.TemplateResponse(request, "register.html", context={"login": False})

@router.post('/register')
async def signup(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    try:
        user = UserRegister(email=email, password=password, confirm_password=confirm_password)
        auth_response = supabase.auth.sign_up({
            'email': user.email,
            'password': user.password
        })
        if auth_response.user is None:
            raise HTTPException(status_code=400, detail="Signup failed")
        if len(auth_response.user.identities) == 0:
            raise HTTPException(status_code=400, detail='User already exists')
        return RedirectResponse('/login', status_code=303)
    except UserException as err:
        return templates.TemplateResponse(request, "register.html", context={"login": False, "error": err, "email": email})

    except Exception as err:
        print(err)
        return templates.TemplateResponse(request, "register.html", context={"login": False, "error": 'Ocorreu uma falha no cadastro'})

@router.post('/login')
async def login(
    response: Response,
    request: Request,
    email: str = Form(...),
    password: str = Form(...)):
    try:
        user = UserLogin(email=email, password=password)
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

    except AuthError as err:
        return templates.TemplateResponse(request, "login.html", context={"login": True, "error": err})

    except Exception as err:
        print(err)
        return templates.TemplateResponse(request, "login.html", context={"login": True, "error": "Ocorreu uma falha no login"})

@router.get('/login')
async def login(request: Request):
    return templates.TemplateResponse(request, "login.html", context={"login": True})


@router.get('/logout')
async def logout(response: Response):
    response = RedirectResponse('/login', status_code=303)
    response.delete_cookie(key='access_token', path='/')
    return response
