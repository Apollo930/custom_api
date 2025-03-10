from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
import os

app = FastAPI()

@app.get("/", response_class=FileResponse)
def home():
    file_path = os.path.join("templates", "index.html")
    return FileResponse(file_path)


'''
For storage api (Speedathon 2025 Prelims Q7)
'''

UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post('/d7/store')
async def store_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, 'wb') as f:
        f.write(await file.read())
    return {"message": "File uploaded successfully"}

@app.get('/d7/retrieve/{filename}')
async def retrieve_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

@app.delete('/d7/delete/{filename}')
async def delete_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": "File deleted successfully"}
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/d7/listfiles")
async def listfiles():
    try:
        files = os.listdir(UPLOAD_FOLDER)
        return JSONResponse(content={"files": files}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)