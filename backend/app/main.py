from fastapi import FastAPI
from app.db.session import engine, Base
from app.api import auth, habits, logs, groups, analytics
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(habits.router)
app.include_router(logs.router)
app.include_router(groups.router)
app.include_router(analytics.router)

@app.get("/health")
def root():
    return {"message" : "welcom to our habit tracker app"}
