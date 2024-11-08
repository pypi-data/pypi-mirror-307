import os

import uvicorn
from fastapi import FastAPI
from poetry_fastapi_demo.routers import user_router

app = FastAPI()
app.include_router(router=user_router, prefix="/api/v1/user", tags=["users"])
if __name__ == "__main__":
    log_conf_path = os.environ.get("LOG_CONFIG")
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_config=log_conf_path)
