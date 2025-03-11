from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse, RedirectResponse
from pydantic import BaseModel
import os, io, vercel_blob

router = APIRouter()

@router.get('/')
async def home():
    return {"message": "Welcome to New API!"}

from typing import Union

class CalculationRequest(BaseModel):
    operation: str
    num1: Union[int, float]
    num2: Union[int, float]

@router.post("/calculate")
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Union

app = FastAPI()

class CalculationRequest(BaseModel):
    operation: str
    num1: Union[int, float, None] = None
    num2: Union[int, float, None] = None

@app.post("/calculate")
async def calculate(request: CalculationRequest):
    if request.num1 is None or request.num2 is None:
        return JSONResponse(status_code=418, content={
            "operation": request.operation,
            "num1": request.num1,
            "num2": request.num2,
            "success": False,
            "message": "Missing number(s)"
        })

    operations = {
        "add": lambda x, y: x + y,
        "sub": lambda x, y: x - y,
        "mul": lambda x, y: x * y,
        "div": lambda x, y: x / y if y != 0 else None,
        "pow": lambda x, y: x ** y,
        "mod": lambda x, y: x % y if y != 0 else None,
    }

    if request.operation not in operations:
        return JSONResponse(status_code=418, content={
            "operation": request.operation,
            "num1": request.num1,
            "num2": request.num2,
            "success": False,
            "message": "Invalid operation"
        })

    if request.operation in ["div", "mod"] and request.num2 == 0:
        return JSONResponse(status_code=418, content={
            "operation": request.operation,
            "num1": request.num1,
            "num2": request.num2,
            "success": False,
            "message": "Division by zero is not allowed"
        })

    try:
        result = operations[request.operation](request.num1, request.num2)

        if result is None:
            raise ValueError("Mathematical error")

        if isinstance(result, float) and result.is_integer():
            result = int(result)

    except Exception as e:
        return JSONResponse(status_code=418, content={
            "operation": request.operation,
            "num1": request.num1,
            "num2": request.num2,
            "success": False,
            "message": f"Mathematical error: {str(e)}"
        })

    return JSONResponse(content={
        "operation": request.operation,
        "num1": request.num1,
        "num2": request.num2,
        "result": result,
        "success": True
    })
