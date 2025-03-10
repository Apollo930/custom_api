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
        vercel_blob.put(f"uploads/{file.filename}", file_content )
        return {"message": f"File uploaded successfully as {file.filename}"}
    except Exception as e:
        return {"error": str(e)}

@app.get('/d7/retrieve/{filename}')
async def retrieve_file(filename: str):
    try:
        resp = vercel_blob.list()
        blobs = resp.get("blobs", [])
        url = [blob["url"] for blob in blobs if blob["pathname"].endswith(filename)]

        if not url:
            raise HTTPException(status_code=404, detail="File not found")

        download_url = vercel_blob.head(url[0]).get("downloadUrl")
        print(download_url)

        return RedirectResponse(url=download_url)
    
    except Exception as e:
        print("couldn't even do anything")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.delete('/d7/delete/{filename}')
async def delete_file(filename: str):
    try:
        resp = vercel_blob.list()
        blobs = resp.get("blobs", [])
        url = [blob["url"] for blob in blobs if blob["pathname"].endswith(filename)]

        if not url:
            raise HTTPException(status_code=404, detail="File not found")
        url=url[0]

        vercel_blob.delete(url)
        return RedirectResponse("/?messsage=Download Successful")
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
