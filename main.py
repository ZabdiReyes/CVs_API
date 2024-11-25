from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from bson import Binary
import os
import PyPDF2
from io import BytesIO
from pdftotext import *

#Initialize the FastAPI app
app = FastAPI() #IMPORTANT: This is the name of the FastAPI app

app.version = "1.0.0"

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB URI
db = client['CurriculumsDB']
pdfs_collection = db['PDFs']
txts_collection = db['TXTs']

# Check if the PDF index exists in the database and create it if it doesn't
if not pdfs_collection.find_one({"_id": "pdf_index"}):
    pdfs_collection.insert_one({"_id": "pdf_index", "pdf_index": 0})

# Define the endpoint to upload the PDF
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Read the uploaded PDF file
    file_content = await file.read()
    
    # Get the next PDF index
    counter = pdfs_collection.find_one_and_update(
        {"_id": "pdf_index"},
        {"$inc": {"pdf_index": 1}},
        return_document=True
    )
    
    # Read the PDF content
    #pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
    file_name = f"Profile{counter['pdf_index']}"
    
    name, mongodic1,mongodic2= pdf_to_txt_from_bytes(file_content, file_name+".pdf", file_name+".txt")
    
    
    # Generate the profile name based on the PDF index example: Profilepdf_index as Profile1, Profile2, Profile3 etc.
    profile_pdf_name = f"Profile{counter['pdf_index']}"
    
    # Store the PDF in MongoDB as binary data
    pdf_data = {
        "filename": profile_pdf_name + ".pdf",
        "name": name,
        "file_content": Binary(file_content)
    }
    txt_data = {
        "filename": profile_pdf_name + ".txt",
        "name": name,
        "columna_content": mongodic1,
        "columna_content2": mongodic2
    }

    # Insert the data into MongoDB
    
    from bson import json_util
        
    result = pdfs_collection.insert_one(pdf_data)
    result = txts_collection.insert_one(txt_data)

    # Return success message with inserted ID
    return {"message": "PDF uploaded successfully", "file_id": str(result.inserted_id)}

