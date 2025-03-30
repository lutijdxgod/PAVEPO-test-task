from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.auth.router import router as auth_router
from .api.users.router import router as users_router
from .api.audiofiles.router import router as audiofiles_router

app = FastAPI()

origins = ["*"]  # ["*"] for public api
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = [auth_router, users_router, audiofiles_router]
for router in routers:
    app.include_router(router)


@app.get("/ping")
async def root():
    return {"success": True, "message": " pong"}
