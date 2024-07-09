# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.stackauth import router as stackauth_router
from api.routers.user import router as user_router
# from api.middleware.refresh_token import TokenRefreshMiddleware
from api.middleware.refresh_token_new import TokenRefreshMiddleware
from depends.auth import settings


app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


# Initialize middleware
app.add_middleware(
    TokenRefreshMiddleware,
    refresh_url=f"{settings.server_url}/realms/{settings.realm}/protocol/openid-connect/token",
    client_id=settings.client_id,
    client_secret=settings.client_secret
)

app.include_router(stackauth_router)
app.include_router(user_router)