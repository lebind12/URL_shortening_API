from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

### router code space
from domain.URL import url_router
###

app = FastAPI()

### cors middleware space
origins = [
    "http://127.0.0.1:5173"
    "http://localhost:8000"
    "*"
]

###

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(url_router.router)