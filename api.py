from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse, RedirectResponse
import os
import io, vercel_blob

app = FastAPI()
BLOB_URL = os.getenv("BLOB_URL")
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
        return {"message": f"File uploaded successfully as {file.filename}"}
    except Exception as e:
        return {"error": str(e)}

@app.get('/d7/retrieve/{filename}')
async def retrieve_file(filename: str):
    try:
        # Fetch the list of files from Vercel Blob
        resp = vercel_blob.list()
        blobs = resp.get("blobs", [])

        # Find the actual file based on filename
        matching_blob = next((blob for blob in blobs if blob["pathname"].endswith(f"/{filename}")), None)

        if not matching_blob:
            raise HTTPException(status_code=404, detail="File not found")

        # Get the correct download URL
        download_url = matching_blob.get("downloadUrl")
        if not download_url:
            raise HTTPException(status_code=404, detail="Download URL not available")

        # Redirect to the file URL
        return RedirectResponse(url=download_url)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

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
        filenames = [blob["pathname"].split("/")[-1] for blob in resp.get("blobs", [])]
        return JSONResponse(content={"files": filenames}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": "Failed to list files", "details": str(e)}, status_code=400)
