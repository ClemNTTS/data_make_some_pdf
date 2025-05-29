from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import io


class Element(BaseModel):
    element_type: str
    content: str
    x: float
    y: float
    width: float
    height: float


class JSONData(BaseModel):
    file_name: str
    font: str
    font_size: int
    content: list[Element]


def create_pdf_template(json_data: JSONData):
    """Creates a PDF template file in memory and returns it as a streaming response."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont(json_data.font, json_data.font_size)
    c = add_elements_to_canvas(c, json_data.content)
    c.save()
    buffer.seek(0)
    return StreamingResponse(buffer, media_type='application/pdf', headers={
        'Content-Disposition': f'attachment; filename="{json_data.file_name}.pdf"'
    })


def add_elements_to_canvas(c: canvas.Canvas, elements: list[Element]) -> canvas.Canvas:
    """Adds elements to the canvas.
    """
    for element in elements:
        if element.element_type == "text":
            c.drawString(element.x, element.y, element.content)
        elif element.element_type == "image":
            c.drawImage(element.content, element.x, element.y,
                        width=element.width, height=element.height)
    return c
