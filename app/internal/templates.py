from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from fastapi.responses import StreamingResponse
from app.internal.struct import JSONData, Element
from app.internal import inputs
import logging
import io
import base64

# Size front (HTML/CSS)
FRONT_WIDTH = 794
FRONT_HEIGHT = 1123

PDF_WIDTH, PDF_HEIGHT = A4


def convert_x(x):
    return x * PDF_WIDTH / FRONT_WIDTH


def convert_y(y, height):
    return (
        PDF_HEIGHT
        - (y * PDF_HEIGHT / FRONT_HEIGHT)
        - (height * PDF_HEIGHT / FRONT_HEIGHT)
    )


def convert_w(w):
    return w * PDF_WIDTH / FRONT_WIDTH


def convert_h(h):
    return h * PDF_HEIGHT / FRONT_HEIGHT


def create_pdf_template(json_data: JSONData):
    """Creates a PDF template file in memory and returns it as a streaming response."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont(json_data.font, json_data.font_size)
    c = add_elements_to_canvas(c, json_data.content)
    c.save()
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{json_data.file_name}.pdf"'
        },
    )


def process_image(c: canvas.Canvas, element: Element) -> canvas.Canvas:
    """Processes an image element and adds it to the canvas."""
    try:
        if not element.content or len(element.content) < 16:
            logging.warning("Image content is empty or too short, skipping.")
            return c
        image_data = base64.b64decode(element.content)
        image_data = ImageReader(io.BytesIO(image_data))
        c.drawImage(
            image_data,
            element.x,
            element.y,
            width=element.width,
            height=element.height,
        )
    except Exception as e:
        logging.error(f"Error processing image ignored: {e}")
    return c


def process_input(c: canvas.Canvas, element: Element) -> canvas.Canvas:
    """Processes an input element and adds it to the canvas."""
    try:
        element_copy = (
            element.model_copy()
            if hasattr(element, "model_copy")
            else Element(**element.dict())
        )
        element_copy.x = convert_x(element.x)
        element_copy.y = convert_y(element.y, element.height)
        if getattr(element, "input_type", None) == "checkbox":
            element_copy.width = max(element.width, 20)
            element_copy.height = max(element.height, 20)
        else:
            element_copy.width = convert_w(element.width)
            element_copy.height = convert_h(element.height)
        c = inputs.handle_input_element(c, element_copy)
    except Exception as e:
        print(f"Error processing input ignored: {e}")
    return c


def add_elements_to_canvas(c: canvas.Canvas, elements: list[Element]) -> canvas.Canvas:
    """Adds elements to the canvas with coordinate conversion from HTML to PDF."""

    MIN_ELEMENTS_SIZE = 8
    for element in elements:
        x = convert_x(element.x)
        y = convert_y(element.y, element.height)
        w = max(convert_w(element.width), MIN_ELEMENTS_SIZE)
        h = max(convert_h(element.height), MIN_ELEMENTS_SIZE)

        if element.element_type == "text":
            c.drawString(x, y, element.content)
        elif element.element_type == "image":
            c = process_image(c, element)
        elif element.element_type == "input":
            c = process_input(c, element)
    return c
