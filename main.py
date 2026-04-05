# main.py (snippet)
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

logger = logging.getLogger(__name__)

import db.config_db as config_db
from router.goldRoutes import router as gold_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await config_db.init_db()
    try:
        yield
    finally:
        await config_db.engine.dispose()


app = FastAPI(lifespan=lifespan)

# CORS - allow your frontend (adjust origins)
app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:5000", "https://api-get-away.krishnarajthadesar.in/"],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"], )

# Mount router under /api so frontend's API_BASE_URL + paths match
app.include_router(gold_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    body = await request.body()
    logger.warning(
        "Request validation failed: method=%s path=%s errors=%s body=%s",
        request.method,
        request.url.path,
        exc.errors(),
        body.decode("utf-8", errors="replace"),
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


# basic healthcheck
@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/ready")
async def readiness_check():
    try:
        async with config_db.engine.connect() as conn:
            await conn.exec_driver_sql("SELECT 1")
        return {"status": "ready"}
    except Exception:
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=503, content={"status": "not ready"})


@app.get("/auth_check")
async def auth_check(request: Request):
    # Headers in FastAPI are case-insensitive
    user_email = request.headers.get("x-user-email")
    user_sub = request.headers.get("x-user-sub")
    user_name = request.headers.get("x-user-name")

    return {"status": "ok", "user_email": user_email, "user_sub": user_sub, "user_name": user_name,
            "all_headers": dict(request.headers)  # optional: helps debug
            }
# things to do next
# 1. do some check that we trust the user email only when its coming from our api-gateway
# 2. deny any request without that private key from api-gateway
# 3. use the user sub or email in our db queries and stuff
# 4. refreshing tokens periodically without notifying frontend.
