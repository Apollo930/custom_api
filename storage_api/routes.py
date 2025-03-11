from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse, RedirectResponse
import os, io, vercel_blob


router = APIRouter()

'''
For storage api (Speedathon 2025 Prelims Q7)
'''

@router.post('/store')
async def store_file(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        vercel_blob.put(f"uploads/{file.filename}", file_content )
        return {"message": f"File uploaded successfully as {file.filename}"}
    except Exception as e:
        return {"error": str(e)}

@router.get('/retrieve/')
async def retrieve_file(filename: str):
    try:
        resp = vercel_blob.list()
        blobs = resp.get("blobs", [])
        url = [blob["url"] for blob in blobs if blob["pathname"].endswith(filename)]

        if not url:
            raise HTTPException(status_code=404, detail="File not found")

        download_url = vercel_blob.head(url[0]).get("downloadUrl")

        return RedirectResponse(url=download_url)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get('/delete/')
async def delete_file(filename: str):
    try:
        resp = vercel_blob.list()
        blobs = resp.get("blobs", [])
        url = [blob["url"] for blob in blobs if blob["pathname"].endswith(filename)]

        if not url:
            raise HTTPException(status_code=404, detail="File not found")
        url=url[0]

        vercel_blob.delete(url)
        html_content = """
<script>
    alert("File deleted successfully!");
    window.location.href = "/";
</script>
"""
        return HTMLResponse(content=html_content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/listfiles")
async def listfiles():
    try:
        resp = vercel_blob.list()
        filenames = [blob["pathname"].split("/")[-1] for blob in resp.get("blobs", [])]
        return JSONResponse(content={"files": filenames}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": "Failed to list files", "details": str(e)}, status_code=400)
