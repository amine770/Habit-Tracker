from fastapi import FastAPI
from app.db.session import engine, Base
from app.api import auth, user

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)

@app.get("/health")
def root():
    return {"message" : "welcom to our habit tracker app"}
