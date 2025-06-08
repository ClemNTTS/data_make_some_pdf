# Data Make Some PDF

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)  
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> Automate PDF‐form filling from tabular data (e.g., Excel/CSV) at scale, with an optional future web interface.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Command‐Line Interface](#command-line-interface)
  - [Sample Workflow](#sample-workflow)
- [Development](#development)
  - [Running Tests](#running-tests)
  - [Linting](#linting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

---

## Overview

**Data Make Some PDF** is a lightweight Python utility designed to batch‐fill a static PDF form using rows of data from spreadsheet files (Excel, CSV). It was created to address a recurring agency use case: replicating manual PDF‐form‐filling for hundreds of users. This repository includes:

1. A Python script (`fill_pdf.py`) that reads an input data file (Excel/CSV), maps columns to PDF form fields, and outputs individual filled PDFs.
2. A simple configuration file (`config.yml`) to define field mappings and output preferences.
3. Placeholder for a future web‐based front end (e.g., Flask or FastAPI) to offer a “sexy” UI for non‐technical users.

---

## Features

- **Bulk PDF Filling**  
  Read a tabular data source and generate one filled PDF per row.

- **Flexible Input Formats**  
  Support for XLSX, XLS, and CSV input files (via `pandas`).

- **Field Mapping via YAML**  
  Define which spreadsheet column corresponds to which PDF form field in a human‐readable YAML file.

- **Output Customization**  
  Choose output directory, file naming pattern, and whether to flatten form fields.

- **Error Handling & Logging**  
  Log any missing or invalid fields for review; continue processing remaining rows.

---

## Project Structure

```

data\_make\_some\_pdf/
├── config.yml             # YAML configuration for field mappings and options
├── fill\_pdf.py            # Main script: reads data and fills PDF form
├── requirements.txt       # Python dependencies
├── sample\_data/
│   ├── template\_form.pdf  # Blank PDF form with AcroForm fields
│   ├── data.xlsx          # Example Excel file with user data
│   └── data.csv           # Example CSV file (alternative)
├── outputs/               # Default folder where generated PDFs are saved
│   └── (auto‐generated .pdf files)
├── tests/
│   ├── test\_fill\_pdf.py   # Unit tests for `fill_pdf.py` logic
│   └── test\_data.csv      # Minimal test data
├── LICENSE                # Project license (MIT)
└── README.md              # ← You are here

```

---

## Prerequisites

1. **Python 3.8+** (ideally 3.9 or 3.10)
2. **pip** (packaged with Python)
3. **Git** (to clone this repo)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/ClemNTTS/data_make_some_pdf.git
   cd data_make_some_pdf

   ```

2. **Create & activate a virtual environment** (recommended)

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install uv
   uv sync
   ```

---

## Configuration

All field mappings and basic options live in `config.yml`.
Below is a sample configuration:

```yaml
# config.yml

# Path to the template PDF form (AcroForm with named fields)
template_pdf: sample_data/template_form.pdf

# Input data file (XLSX or CSV). The extension determines the parser.
input_data: sample_data/data.xlsx

# Output directory where filled PDFs will be written
output_dir: outputs/

# How to name each output PDF: can reference column names from the sheet.
# For example: "{LastName}_{FirstName}.pdf"
output_filename_pattern: "{UserID}_{LastName}.pdf"

# Should the output be a flattened PDF (non‐editable form)? true/false
flatten: false

# Mapping between spreadsheet columns and PDF form field names
field_mappings:
  FirstName: first_name_field # “FirstName” column → “first_name_field” in PDF
  LastName: last_name_field
  Email: email_field
  Age: age_field
  # ... Add more mappings as needed
```

**Tip:**
– Ensure the keys under `field_mappings:` exactly match the column headers in your Excel/CSV file.
– PDF form field names (right side) must exactly match the AcroForm field names embedded in `template_form.pdf`.

---

## Usage

### Command-Line Interface

Basic invocation:

```bash
python fill_pdf.py --config config.yml
```

**Options:**

```text
--config  Path to YAML configuration (default: config.yml)
--dry‐run Run without writing files; prints what would be generated
--verbose Enable verbose logging to console
--help    Show usage information
```

### Sample Workflow

1. **Prepare your blank PDF form**
   Create a PDF with fillable form fields (e.g., using Adobe Acrobat or LibreOffice). Save it as `template_form.pdf` in `sample_data/`.

2. **Populate your data source**

   - In `sample_data/data.xlsx`, add a header row with column names (e.g., `FirstName, LastName, Email, Age, UserID`).
   - Ensure each row corresponds to one individual’s data.

3. **Edit `config.yml`**

   - Update `template_pdf` to point to your form.
   - Update `input_data` if your file name differs.
   - Adjust `output_filename_pattern` to your desired naming convention.
   - Verify `field_mappings` map each column to the correct PDF field name.

4. **Run the script**

   ```bash
   python fill_pdf.py --config config.yml
   ```

   - Filled PDFs will appear in the `outputs/` directory.
   - If `--flatten true`, the PDF fields will be merged into static text (uneditable).

5. **Verify output**

   - Open any generated PDF in a PDF viewer to confirm fields populated correctly.

---

## Development

### Running Tests

This project uses `pytest` for unit tests. To run the test suite:

```bash
pytest --maxfail=1 --disable-warnings -q
```

- **Unit tests:** Located in `tests/test_fill_pdf.py`.
- The tests cover core functionality such as reading data, mapping fields, and generating in‐memory PDF objects.

### Linting

We use `flake8` for static analysis. To check code style:

```bash
flake8 fill_pdf.py tests/
```

Adjust the `.flake8` config (if present) to modify line‐length or ignore rules.

---

## Contributing

Contributions are welcome! To contribute:

1. **Fork** the repository.
2. **Create a new branch** (`git checkout -b feature/your-feature`).
3. **Make your changes** (code, tests, documentation).
4. **Run tests** to ensure nothing is broken.
5. **Submit a pull request**, describing your changes in detail.

Please follow these guidelines:

- Write clear, descriptive commit messages.
- Add new unit tests or update existing ones when adding functionality or fixing bugs.
- Ensure all existing tests pass before requesting a review.

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## Acknowledgments

- **pandas** – for data file parsing (XLSX/CSV).
- **PyPDF2** (or similar library) – for reading/writing PDF forms.
- Inspiration and guidance from various open‐source PDF‐filling scripts.
- Agency team members who identified the original use case.

---

## Contact

**Maintainer:**
ClemNTTS ([https://github.com/ClemNTTS](https://github.com/ClemNTTS))

Email: [karmaclem@gmail.com](mailto:karmaclem@gmail.com)

Feel free to open issues or reach out with questions about using or extending this tool.
