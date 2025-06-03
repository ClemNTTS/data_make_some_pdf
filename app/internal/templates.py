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
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{json_data.file_name}.pdf"'
        },
    )


def add_elements_to_canvas(c: canvas.Canvas, elements: list[Element]) -> canvas.Canvas:
    """Adds elements to the canvas with coordinate conversion from HTML to PDF."""
    # Dimensions du front (HTML/CSS)
    FRONT_WIDTH = 794
    FRONT_HEIGHT = 1123
    # Dimensions du PDF (A4 points)
    PDF_WIDTH, PDF_HEIGHT = A4

    def convert_x(x):
        return x * PDF_WIDTH / FRONT_WIDTH

    def convert_y(y, height):
        # Inverser l'axe Y et ajuster pour la hauteur de l'élément
        return PDF_HEIGHT - (y * PDF_HEIGHT / FRONT_HEIGHT) - (height * PDF_HEIGHT / FRONT_HEIGHT)

    def convert_w(w):
        return w * PDF_WIDTH / FRONT_WIDTH

    def convert_h(h):
        return h * PDF_HEIGHT / FRONT_HEIGHT

    MIN_SIZE = 8  # points
    for element in elements:
        x = convert_x(element.x)
        y = convert_y(element.y, element.height)
        w = max(convert_w(element.width), MIN_SIZE)
        h = max(convert_h(element.height), MIN_SIZE)
        if element.element_type == "text":
            c.drawString(x, y, element.content)
        elif element.element_type == "image":
            try:
                if not element.content or len(element.content) < 16:
                    print(
                        f"Image ignorée: base64 absent ou trop court (content={element.content})")
                    continue
                image_data = base64.b64decode(element.content)
                image_data = ImageReader(io.BytesIO(image_data))
                c.drawImage(
                    image_data,
                    x,
                    y,
                    width=w,
                    height=h,
                )
            except Exception as e:
                print(f"Erreur image ignorée: {e}")
                continue
        elif element.element_type == "input":
            try:
                print(
                    f"Input reçu: input_type={getattr(element, 'input_type', None)}, x={x}, y={y}, w={w}, h={h}")
                # Créer une copie de l'élément avec coordonnées converties
                element_copy = element.model_copy() if hasattr(
                    element, 'model_copy') else Element(**element.dict())
                element_copy.x = x
                element_copy.y = y
                # Forcer une taille minimale pour les cases à cocher
                if getattr(element, 'input_type', None) == "checkbox":
                    element_copy.width = max(w, 20)
                    element_copy.height = max(h, 20)
                    print(
                        f"Checkbox at x={element_copy.x}, y={element_copy.y}, w={element_copy.width}, h={element_copy.height}")
                else:
                    element_copy.width = w
                    element_copy.height = h
                c = inputs.handle_input_element(c, element_copy)
            except Exception as e:
                print(f"Erreur case à cocher ou champ input ignoré: {e}")
                continue
    return c
