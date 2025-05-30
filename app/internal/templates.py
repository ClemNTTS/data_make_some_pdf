from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from fastapi.responses import StreamingResponse
from app.internal.struct import JSONData, Element
from app.internal import inputs
import io
import base64


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
            image_data = base64.b64decode(element.content)
            image_data = ImageReader(io.BytesIO(image_data))
            c.drawImage(image_data, element.x, element.y,
                        width=element.width, height=element.height)
        elif element.element_type == "input":
            try:
                c = inputs.handle_input_element(c, element)
            except Exception as e:
                raise ValueError(f"Error handling input element: {e}")

    return c
