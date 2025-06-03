import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.internal.templates import JSONData, create_pdf_template
from app.internal.pdf_filler import handle_merge
from app.internal.data_template import create_data_template

app = FastAPI()

# Ajout du middleware CORS pour autoriser les requêtes du front
app.add_middleware(
    CORSMiddleware,
    # Pour la prod, restreindre à ["http://127.0.0.1:3000"]
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello, World! Let's create a PDF template!"}


@app.post("/template")
def create_template(template: JSONData):
    return create_pdf_template(template)


@app.post("/merge")
async def merge_pdfs_excel(
    template: UploadFile = File(...),
    excel_file: UploadFile = File(...),
):
    return handle_merge(template, excel_file)


@app.post("/data_template")
def data_template_endpoint(
    template: UploadFile = File(...),
):
    return create_data_template(template)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
