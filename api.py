from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse
import os, io
import httpx

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

UPLOAD_FOLDER = os.path.join(PROJECT_LINK,'uploads')

@app.post('/d7/store')
async def store_file(file: UploadFile = File(...)):
    try:
        file_content = await file.read()

        headers = {"Authorization": f"Bearer {VERCEL_BLOB_READ_WRITE_TOKEN}"}
        files = {"file": (file.filename, file_content, file.content_type)}

        async with httpx.AsyncClient() as client:
            response = await client.post(VERCEL_BLOB_API, headers=headers, files=files, params = {"path": "uploads/"})

        if response.status_code == 200:
            blob_url = response.json().get("url")
            return {"message": "File uploaded successfully"}
        else:
            return {"error": "Failed to upload file", "details": response.json()}

    except Exception as e:
        return {"error": str(e)}

@app.get('/d7/retrieve/{filename}')
async def retrieve_file(filename: str):
    file_url = os.path.join(UPLOAD_FOLDER, filename)

    async with httpx.AsyncClient() as client:
        response = await client.get(file_url)

    if response.status_code == 200:
        file_stream = io.BytesIO(response.content)
        return StreamingResponse(
            file_stream, 
            media_type="application/octet-stream", 
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    else:
        return {"error": "File not found"}

@app.delete('/d7/delete/{filename}')
async def delete_file(filename: str):
    file_url = os.path.join(UPLOAD_FOLDER, filename)
    headers = {
        "Authorization": f"Bearer {VERCEL_BLOB_READ_WRITE_TOKEN}"
    }
    payload = {"url": file_url}

    async with httpx.AsyncClient() as client:
        response = await client.post(VERCEL_BLOB_DELETE_API, headers=headers, json=payload)

    if response.status_code == 200:
        return {"message": "File deleted successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())


@app.get("/d7/listfiles")
async def listfiles():
    headers = {"Authorization": f"Bearer {VERCEL_BLOB_READ_WRITE_TOKEN}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(VERCEL_BLOB_LIST_API, headers=headers)

    if response.status_code == 200:
        data = response.json()
        filenames = [blob["url"].split("/")[-1] for blob in data.get("blobs", [])]
        return JSONResponse(content={"files": filenames}, status_code=200)
    else:
        return JSONResponse(content={"error": "Failed to list files", "details": response.json()}, status_code=response.status_code)