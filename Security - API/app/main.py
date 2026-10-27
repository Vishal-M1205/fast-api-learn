from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


from app.routers.auth_routes import route as auth_router

app = FastAPI(title="API Security Practice")


@app.get("/")
def root():
    return {"app": "Security Practice"}


app.include_router(auth_router)


@app.exception_handler(Exception)
def raise_expcetion(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"ERROR : {request.url} | {exc} | {request.method} "},
    )
