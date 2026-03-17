from fastapi import Request, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.datastructures import MutableHeaders
import jwt
from database import SUPABASE_JWT_SECRET, supabase_connection

security = HTTPBearer()

async def auth_middleware(request: Request, call_next):
    path = request.url.path
    if path in ["/login", "/signup"] or path.startswith("/static"):
        return await call_next(request)
    token = request.cookies.get("access_token")
    if token:
        clean_token = token.replace("Bearer ", "")
        new_headers = MutableHeaders(request._headers)
        new_headers["authorization"] = f"Bearer {clean_token}"
        request._headers = new_headers
        request.scope.update(headers=request.headers.raw)

    '''
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]
        request.headers.__dict__['_list'].append(
            (b"authorization", f"Bearer {token}".encode())   
        )'''
    try:
        response = await call_next(request)
        return response
    except Exception as err:
        print(err)
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        payload = jwt.decode(token, SUPABASE_JWT_SECRET.encode('utf-8'), algorithms=["HS256"], options={"verify_aud": False})
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth credentials")
        supabase_connection.postgrest.auth(token)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.PyJWKError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validade user")
