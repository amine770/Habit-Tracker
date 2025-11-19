from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def root():
    return {"message" : "welcom to our habit tracker app"}
