from fastapi import FastAPI, Request
from routers import filtercanvas
from fastapi.middleware.cors import CORSMiddleware
from core.rate_limiter import limiter
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

app = FastAPI(
    docs_url=None,
    redoc_url=None
)

origins = [
    "https://digit-sorter-ai.vercel.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests, wait a bit"}
    )
# Routers
app.include_router(filtercanvas.router)
