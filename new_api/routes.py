from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse, RedirectResponse
from pydantic import BaseModel
import os, io, vercel_blob

router = APIRouter()

@router.get('/')
async def home():
    return {"message": "Welcome to New API!"}

class CalculationRequest(BaseModel):
    operation: str
    num1: float
    num2: float

@router.post("/calculate")
async def calculate(request: CalculationRequest):
    operations = {
        "add": lambda x, y: x + y,
        "sub": lambda x, y: x - y,
        "mul": lambda x, y: x * y,
        "div": lambda x, y: x / y if y != 0 else None,
        "pow": lambda x, y: x ** y,
        "mod": lambda x, y: x % y if y != 0 else None,
    }
    
    if request.operation not in operations:
        raise HTTPException(status_code=418, detail={
            "operation": request.operation,
            "num1": request.num1,
            "num2": request.num2,
            "success": False,
            "message": "Invalid operation"
        })
    
    try:
        result = operations[request.operation](request.num1, request.num2)
        if result is None:
            raise HTTPException(status_code=418, detail={
                "operation": request.operation,
                "num1": request.num1,
                "num2": request.num2,
                "success": False,
                "message": "Division by zero is not allowed"
            })
    except Exception as e:
        raise HTTPException(status_code=418, detail={
            "operation": request.operation,
            "num1": request.num1,
            "num2": request.num2,
            "success": False,
            "message": f"Mathematical error: {str(e)}"
        })
    
    return {
        "operation": request.operation,
        "num1": request.num1,
        "num2": request.num2,
        "result": result,
        "success": True
    }