from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()



'''
For storage api (Speedathon 2025 Prelims Q7)
'''

UPLOAD_FOLDER = 'uploads'
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

