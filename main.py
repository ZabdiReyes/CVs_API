from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from bson import Binary
import os

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB URI
db = client['CurriculumsBD']
pdfs_collection = db['PDFs']

# Define the endpoint to upload the PDF
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Read the uploaded PDF file
    file_content = await file.read()

    # Store the PDF in MongoDB as binary data
    pdf_data = {
        "filename": file.filename,
        "file_content": Binary(file_content)
    }

    # Insert the data into MongoDB
    result = pdfs_collection.insert_one(pdf_data)

    # Return success message with inserted ID
    return {"message": "PDF uploaded successfully", "file_id": str(result.inserted_id)}