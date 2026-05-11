from fastapi import APIRouter, UploadFile, File
import shutil

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    path = f"uploads/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}