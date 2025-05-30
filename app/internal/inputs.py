from reportlab.pdfgen import canvas
from app.internal.struct import Element


def handle_input_element(c: canvas.Canvas, element: Element) -> canvas.Canvas:
    """

    Draw an input element on the canvas.

    Args:
        c (canvas.Canvas): canva to draw on
        element (Element): Element to draw on the canvas

    Returns:
        canvas.Canvas: _description_
    """
    if not element.input_type:
        raise ValueError("Input type is required for input elements")

    form = c.acroForm
    if element.input_type == "text":
        form.textfield(
            name=element.content,
            tooltip=element.content,
            x=element.x,
            y=element.y,
            width=element.width,
            height=element.height,
            value="",
            borderStyle="solid",
            forceBorder=True,
        )
    elif element.input_type == "checkbox":
        form.checkbox(
            name=element.content,
            tooltip=element.content,
            x=element.x,
            y=element.y,
            buttonStyle="check",
            borderStyle="solid",
        )

    return c
