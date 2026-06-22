from fastapi import FastAPI 
from routers import filtercanvas
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


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

# Routers
app.include_router(filtercanvas.router)
