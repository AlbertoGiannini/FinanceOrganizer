from fastapi import APIRouter, Request, HTTPException
from starlette.responses import Response, RedirectResponse
from database import supabase_connection as supabase
from schemas import User

router = APIRouter(prefix='/auth', tags=['Authentication'])

@router.post('/signup')
async def signup(user: User, response: Response):
    try:
        auth_response = supabase.auth.sign_up({
            'email': user.email,
            'password': user.password
        })
        if auth_response.user is None:
            raise HTTPException(status_code=400, detail="Signup failed")
        return RedirectResponse('/login', status_code=303)
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

@router.post('/login')
async def login(user: User, response: Response):
    try:
        auth_response = supabase.auth.sign_in_with_password({
            'email': user.email,
            'password': user.password
        })
        if auth_response is None:
            raise HTTPException(status_code=400, detail="Login failed")
        access_token = auth_response.access_token
        response =  RedirectResponse('/', status_code=303)
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
        return response

    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))
