from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse, RedirectResponse
import os, io, vercel_blob

router = APIRouter()

@router.get('/')
async def home():
    return {"message": "Welcome to New API!"}