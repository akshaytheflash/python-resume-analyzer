from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from analyzer import analyzeResume

app = FastAPI()

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_methods=["*"],
allow_headers=["*"],
)

@app.post("/upload")
async def uploadPdf(file: UploadFile = File(...)):
      tempPath = "temp_" + file.filename
      with open(tempPath, "wb") as meow:
            shutil.copyfileobj(file.file, meow)

      try:
            result = analyzeResume(tempPath)
      except Exception as e:
            print("something went wrong:", e)
            result = "error happened during analyzing"

      os.remove(tempPath)
      return result
