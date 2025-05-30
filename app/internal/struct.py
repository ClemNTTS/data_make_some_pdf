from pydantic import BaseModel


class Element(BaseModel):
    element_type: str
    content: str
    x: float
    y: float
    width: float
    height: float
    input_type: str | None = None  # Optional, required for type "input" elements only


class JSONData(BaseModel):
    file_name: str
    font: str
    font_size: int
    content: list[Element]
