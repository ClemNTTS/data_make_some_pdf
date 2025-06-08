from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, BooleanObject
from typing import Dict, Any
from io import BytesIO
import pandas as pd
import zipfile


def read_excel(excel_file: UploadFile) -> pd.DataFrame:
    """
    Reads the Excel file and returns its content in data frame.
    """

    if not excel_file.filename or not excel_file.filename.endswith(
        (".xlsx", ".xls", ".csv")
    ):
        raise ValueError("Unsupported file format. Please upload an Excel or CSV file.")

    try:
        if excel_file.filename.endswith(".csv"):
            df = pd.read_csv(excel_file.file)
        else:
            df = pd.read_excel(excel_file.file, engine="openpyxl")
        return df
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {e}") from e


def get_pdf_fields(template: UploadFile) -> tuple[Dict[str, Any], PdfReader]:
    """
    Extracts fields from the PDF template.
    """
    pdf_bytes = template.file.read()
    reader_tempalte = PdfReader(BytesIO(pdf_bytes))
    fields = reader_tempalte.get_form_text_fields()
    if not fields:
        raise ValueError("No form fields found in the PDF template.")
    return fields, reader_tempalte


def correct_fields_values(data_dict: Dict[str, Any]) -> Dict[str, Any]:
    for key in data_dict:
        val = str(data_dict[key]).strip().lower()
        if val in ["yes", "true", "1"]:
            data_dict[key] = "/Yes"
        elif val in ["off", "no", "false", "0", ""]:
            data_dict[key] = "/Off"

    return data_dict


def buffer_process(
    data: pd.DataFrame, fields: Dict[str, Any], reader: PdfReader
) -> BytesIO:
    """
    Processes the data frame and fills the PDF template with the data.
    Returns a BytesIO object containing the filled PDF.
    """
    zip_buffer = BytesIO()

    with zipfile.ZipFile(
        zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED
    ) as zipf:
        # For each row in the data frame:
        for index, row in data.iterrows():
            writer = PdfWriter()
            writer.append_pages_from_reader(reader)
            writer._root_object.update(
                {NameObject("/NeedAppearances"): BooleanObject(True)}
            )

            data_dict = correct_fields_values(row.to_dict())

            # Fill the PDF
            for page in writer.pages:
                writer.update_page_form_field_values(page, data_dict)

            pdf_bytes = BytesIO()
            writer.write(pdf_bytes)
            pdf_bytes.seek(0)

            filename = f"filled_template_row_{index}.pdf"
            zipf.writestr(filename, pdf_bytes.read())
            pdf_bytes.close()

    zip_buffer.seek(0)
    return zip_buffer


def handle_merge(template: UploadFile, excel_file: UploadFile) -> StreamingResponse:
    """
    Handles the merging of a PDF template with an Excel file.
    Reads the Excel file, extracts data, and fills the PDF template for each row.
    Returns a ZIP file containing the generated PDFs.
    """
    data = read_excel(excel_file)
    fields, reader = get_pdf_fields(template)
    buffer = buffer_process(data, fields, reader)

    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=filled_templates.zip"},
    )
