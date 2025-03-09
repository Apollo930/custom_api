from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/first")
def first():
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer token123"
    }
    return Response(status_code=200, headers=headers)

@app.get("/second")
def second():
    data = {
        "param1": "value1",
        "param2": "value2"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer token123"
    }
    return JSONResponse(content=data, status_code=400, headers=headers)
