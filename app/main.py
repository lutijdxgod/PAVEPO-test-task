from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]  # ["*"] for public api
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = []
for router in routers:
    app.include_router(router)


@app.get("/ping")
async def root():
    return {"success": True, "message": " pong"}
