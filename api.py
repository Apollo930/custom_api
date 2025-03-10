from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse
import os
import io, vercel_blob

app = FastAPI()
VERCEL_BLOB_API = "https://api.vercel.com/v2/blob/put"
VERCEL_BLOB_LIST_API = "https://api.vercel.com/v2/blob/list"
VERCEL_BLOB_DELETE_API = "https://api.vercel.com/v2/blob/delete"

VERCEL_BLOB_READ_WRITE_TOKEN = os.getenv("BLOB_READ_WRITE_TOKEN")
PROJECT_LINK = os.getenv("PROJECT_LINK")

@app.get("/", response_class=FileResponse)
def home():
    file_path = os.path.join("templates", "index.html")
    return FileResponse(file_path)


'''
For storage api (Speedathon 2025 Prelims Q7)
'''

@app.post('/d7/store')
async def store_file(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        blob = vercel_blob.put(f"uploads/{file.filename}", file_content )
        return {"message": "File uploaded successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.get('/d7/retrieve/{filename}')
async def retrieve_file(filename: str):
    file_url = os.path.join(PROJECT_LINK, "uploads", filename)
    try:
        download_url = vercel_blob.head(file_url).get("downloadUrl")
        if not download_url:
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(download_url, media_type="application/octet-stream", filename=filename)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete('/d7/delete/{filename}')
async def delete_file(filename: str):
    try:
        vercel_blob.delete(f"uploads/{filename}")
        return {"message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/d7/listfiles")
async def listfiles():
    try:
        resp = vercel_blob.list()
        return JSONResponse(content=resp, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": "Failed to list files", "details": str(e)}, status_code=400)
