from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from bson import Binary
import os
import PyPDF2
from io import BytesIO

#Initialize the FastAPI app
app = FastAPI() #IMPORTANT: This is the name of the FastAPI app

app.version = "1.0.0"

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB URI
db = client['CurriculumsDB']
pdfs_collection = db['PDFs']

# Check if the PDF index exists in the database and create it if it doesn't
if not pdfs_collection.find_one({"_id": "pdf_index"}):
    pdfs_collection.insert_one({"_id": "pdf_index", "pdf_index": 0})

# Define the endpoint to upload the PDF
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Read the uploaded PDF file
    file_content = await file.read()
    
    # Read the PDF content
    pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
    pdf_text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_text += page.extract_text()
    print(pdf_text)

    # Print the PDF content to the console
    print(pdf_text)
    
    # Get the next PDF index
    counter = pdfs_collection.find_one_and_update(
        {"_id": "pdf_index"},
        {"$inc": {"pdf_index": 1}},
        return_document=True
    )
    
    # Generate the profile name based on the PDF index example: Profilepdf_index as Profile1, Profile2, Profile3 etc.
    profile_pdf_name = f"Profile{counter['pdf_index']}"

    name = "Juan"
    
    # Store the PDF in MongoDB as binary data
    pdf_data = {
        "filename": profile_pdf_name + ".pdf",
        "name": name,
        "file_content": Binary(file_content)
    }

    # Insert the data into MongoDB
    result = pdfs_collection.insert_one(pdf_data)

    # Return success message with inserted ID
    return {"message": "PDF uploaded successfully", "file_id": str(result.inserted_id)}

