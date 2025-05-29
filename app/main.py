import uvicorn
from fastapi import FastAPI
from app.internal.templates import JSONData, create_pdf_template

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World! Let's create a PDF template!"}


@app.post("/template")
def create_template(template: JSONData):
    return create_pdf_template(template)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
