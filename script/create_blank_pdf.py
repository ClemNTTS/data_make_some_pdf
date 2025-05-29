#!/usr/bin/env python3
"""
create_blank_pdf
----------------

Generate a single‐page, blank PDF at a specified output path.

Usage:
    create_blank_pdf OUTPUT_PATH

Example:
    create_blank_pdf ../data/filling_data/empty.pdf
"""
import logging
import sys
import argparse
from pathlib import Path
from typing import Union
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def validate_output_path(output_path: Union[str, Path]) -> bool:
    if isinstance(output_path, str):
        output_path = Path(output_path)
    return output_path.suffix.lower() == '.pdf'


def create_blank_pdf(output_path: Union[str, Path]) -> None:
    """
    Create a one‐page blank PDF at output_path. Overwrites if exists.

    Args:
        output_path: Path to write the PDF file.
    """
    if not validate_output_path(output_path):
        raise ValueError("Output path must end with '<file name>.pdf'")

    output_path = Path(output_path)
    parent = output_path.parent
    if not parent.exists():
        logging.debug(f"Creating directory: {parent}")
        parent.mkdir(parents=True, exist_ok=True)

    logging.info(f"Creating blank PDF at: {output_path}")
    c = canvas.Canvas(str(output_path), pagesize=A4)
    c.showPage()
    c.save()
    logging.info(f"Blank PDF saved successfully at: {output_path}")


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a blank PDF file.")
    parser.add_argument(
        "output_path",
        type=Path,
        help="Path where the blank PDF file will be created.",
    )
    return parser.parse_args()


def main() -> None:
    setup_logging()
    args = parse_arguments()
    logging.debug(f"Parsed arguments: {args}")

    if not args.output_path.suffix == '.pdf':
        logging.error("Output path must end with '<file name>.pdf'")
        sys.exit(1)

    try:
        create_blank_pdf(args.output_path)
    except Exception as exc:
        logging.error(f"Failed to create blank PDF: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
