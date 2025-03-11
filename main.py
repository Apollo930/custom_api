from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse, RedirectResponse
import os, io, vercel_blob

from storage_api.routes import router as storage_router

app = FastAPI()
BLOB_URL = os.getenv("BLOB_URL")
PROJECT_LINK = os.getenv("PROJECT_LINK")

@app.get("/", response_class=FileResponse)
def home():
    file_path = os.path.join("templates", "index.html")
    return FileResponse(file_path)

app.include_router(storage_router, prefix="/d7", tags=["Storage_api"])

