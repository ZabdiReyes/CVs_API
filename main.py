from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from pymongo import MongoClient

app = FastAPI()

app.version = "0.0.1"

@app.post('/cargar/', tags=['Push'])

def post_cv_in_pdf(cv : int):
    
    return JSONResponse(content={"cv": cv}, status_code=200)

@app.exception_handler(404)
async def not_found(request, exc):
    return HTMLResponse(content='<h1>¡Error, Page not found!</h1>', status_code=404)