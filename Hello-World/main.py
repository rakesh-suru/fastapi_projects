from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {'message' : "HELLO WORLD!!!..."}

@app.get("/about")
def about():
    return {'message' : "This is my first application using FastAPI"}