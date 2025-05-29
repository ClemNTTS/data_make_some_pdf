"""
  # Tests for scripts in the scripts directory.
"""

import os
import tempfile
import script
import script.create_blank_pdf


def test_create_blank_pdf_creates_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "test_blank.pdf")
        script.create_blank_pdf.create_blank_pdf(output_path)
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0


def test_create_blank_pdf_wrong_extension():
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "test_blank.txt")
        try:
            script.create_blank_pdf.create_blank_pdf(output_path)
        except ValueError:
            pass
        else:
            assert False, "Expected ValueError for wrong file extension"


def test_create_blank_pdf_invalid_path():
    with tempfile.TemporaryDirectory() as tmpdir:
        nested_dir = os.path.join(tmpdir, "nested1", "nested2")
        output_path = os.path.join(nested_dir, "test_blank.pdf")
        script.create_blank_pdf.create_blank_pdf(output_path)
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
