from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def first_get():
    return {"msg": "Hello World"}
