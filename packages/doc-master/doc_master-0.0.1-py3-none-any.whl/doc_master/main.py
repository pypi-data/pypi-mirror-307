import base64
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, Union

import chardet
import docx
import magic  # python-magic library for better file type detection
import pandas as pd
import pypdf
import pytesseract
import yaml
from loguru import logger
from PIL import Image


class AutoFileReader:
    """
    Automatically detect and read any file into a string format.
    Handles binary files, text files, documents, images, and more.
    """

    def __init__(self, use_ocr: bool = False):
        """
        Initialize the AutoFileReader.

        Args:
            use_ocr (bool): Whether to use OCR for image files
        """
        self.setup_logger()
        self.use_ocr = use_ocr

    def setup_logger(self):
        """Configure logging with loguru."""
        logger.remove()
        logger.add(
            "file_reader.log",
            rotation="10 MB",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            level="INFO",
        )

    def read_file(self, file_path: Union[str, Path], **kwargs) -> str:
        """
        Read any file and convert it to string format.

        Args:
            file_path: Path to the file
            **kwargs: Additional arguments for specific file types
                encoding: Optional explicit encoding for text files
                sheet_name: Sheet name/index for Excel files
                image_format: Format for image conversion

        Returns:
            str: Content of the file as string

        Raises:
            Exception: If file cannot be read or processed
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(
                    f"File not found: {file_path}"
                )

            # Get MIME type using python-magic
            mime_type = magic.from_file(str(file_path), mime=True)
            logger.info(f"Detected MIME type: {mime_type}")

            # Detect encoding for text files
            encoding = kwargs.get("encoding")
            if not encoding and mime_type.startswith("text/"):
                with open(file_path, "rb") as f:
                    raw = f.read()
                    result = chardet.detect(raw)
                    encoding = result["encoding"]

            # Process based on MIME type
            if mime_type.startswith("text/"):
                return self._read_text(file_path, encoding)
            elif mime_type == "application/pdf":
                return self._read_pdf(file_path)
            elif mime_type in [
                "application/vnd.ms-excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ]:
                return self._read_excel(file_path, **kwargs)
            elif (
                mime_type == "application/msword"
                or mime_type
                == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ):
                return self._read_docx(file_path)
            elif mime_type == "application/json":
                return self._read_text(file_path, encoding)
            elif mime_type == "application/xml":
                return self._read_xml(file_path)
            elif mime_type.startswith("image/"):
                return self._read_image(file_path, **kwargs)
            elif mime_type == "application/x-yaml":
                return self._read_yaml(file_path)
            else:
                # Try to read as text, if fails, return base64
                try:
                    return self._read_text(file_path, encoding)
                except UnicodeDecodeError:
                    return self._read_binary(file_path)

        except Exception as e:
            logger.error(
                f"Error processing file {file_path}: {str(e)}"
            )
            raise

    def _read_text(
        self, file_path: Path, encoding: Optional[str] = None
    ) -> str:
        """Read text files with encoding detection."""
        encoding = encoding or "utf-8"
        with open(file_path, "r", encoding=encoding) as f:
            return f.read()

    def _read_pdf(self, file_path: Path) -> str:
        """Read PDF files."""
        text_content = []
        with open(file_path, "rb") as f:
            pdf = pypdf.PdfReader(f)
            for page in pdf.pages:
                text_content.append(page.extract_text())
        return "\n".join(text_content)

    def _read_excel(self, file_path: Path, **kwargs) -> str:
        """Read Excel files."""
        sheet_name = kwargs.get("sheet_name", 0)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df.to_string()

    def _read_docx(self, file_path: Path) -> str:
        """Read Word documents."""
        doc = docx.Document(file_path)
        return "\n".join(
            [paragraph.text for paragraph in doc.paragraphs]
        )

    def _read_xml(self, file_path: Path) -> str:
        """Read XML files."""
        tree = ET.parse(file_path)
        return ET.tostring(
            tree.getroot(), encoding="unicode", method="xml"
        )

    def _read_yaml(self, file_path: Path) -> str:
        """Read YAML files."""
        with open(file_path, "r") as f:
            return yaml.dump(yaml.safe_load(f))

    def _read_image(self, file_path: Path, **kwargs) -> str:
        """
        Read image files. If OCR is enabled, extract text;
        otherwise, return base64 representation.
        """
        if self.use_ocr:
            try:
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)
                return (
                    text
                    if text.strip()
                    else self._image_to_base64(file_path)
                )
            except Exception as e:
                logger.warning(
                    f"OCR failed: {e}. Falling back to base64"
                )
                return self._image_to_base64(file_path)
        return self._image_to_base64(file_path)

    def _read_binary(self, file_path: Path) -> str:
        """Read binary files as base64."""
        return self._file_to_base64(file_path)

    def _file_to_base64(self, file_path: Path) -> str:
        """Convert any file to base64 string."""
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def _image_to_base64(self, file_path: Path) -> str:
        """Convert image to base64 string with format prefix."""
        mime_type = magic.from_file(str(file_path), mime=True)
        return f"data:{mime_type};base64,{self._file_to_base64(file_path)}"


def read_single_file(file_path: str) -> str:
    reader = AutoFileReader(use_ocr=True)

    try:
        content = reader.read_file(file_path)
        return content
    except Exception as e:
        print(f"Error: {e}")
        return None


def read_all_files_in_folder(
    folder_path: str, output_type: str = "string"
) -> Union[dict, str]:
    """
    Read all files in a specified folder and return their contents.

    Args:
        folder_path (str): Path to the folder containing files.
        output_type (str): Specify the output type. Options are "dict" or "string". Defaults to "dict".

    Returns:
        Union[dict, str]: A dictionary with file names as keys and file contents as values, or a string representation of the files' contents.
    """
    from pathlib import Path
    from loguru import logger

    if output_type not in ["dict", "string"]:
        raise ValueError(
            "Invalid output_type. Expected 'dict' or 'string'."
        )

    results = {}
    folder = Path(folder_path)

    if not folder.is_dir():
        raise NotADirectoryError(
            f"Path is not a directory: {folder_path}"
        )

    for file_path in folder.iterdir():
        if file_path.is_file():
            try:
                content = read_single_file(str(file_path))
                if output_type == "dict":
                    results[file_path.name] = content
                else:
                    results += (
                        content + "\n"
                    )  # Assuming string output should be a concatenation of file contents
            except Exception as e:
                logger.error(
                    f"Error processing file {file_path}: {str(e)}"
                )
                if output_type == "dict":
                    results[file_path.name] = (
                        None  # Store None for untransformable files
                    )
                else:
                    results += f"Error processing file {file_path}: {str(e)}\n"

    if output_type == "dict":
        return results
    else:
        return results.strip()  # Remove trailing newline character


def doc_master(
    file_path: str = None,
    folder_path: str = None,
    output_type: str = "string",
) -> Union[str, dict]:
    """
    Reads a single file or all files in a folder and returns their contents.

    This function acts as a wrapper for `read_single_file` and `read_all_files_in_folder`.
    It allows for reading a single file or all files in a folder, depending on the input parameters.
    The output type can be specified as either "string" or "dict".

    Args:
        file_path (str, optional): Path to the file to be read. Defaults to None.
        folder_path (str, optional): Path to the folder containing files to be read. Defaults to None.
        output_type (str, optional): Specify the output type. Options are "string" or "dict". Defaults to "string".

    Returns:
        Union[str, dict]: The content of the file or files. If `output_type` is "string", it returns a string representation of the file(s) content. If `output_type` is "dict", it returns a dictionary with file names as keys and file contents as values.
    """
    if file_path is not None:
        output = read_single_file(file_path)
    elif (
        folder_path is not None and output_type is not None
    ):  # Changed 'folder_path' to check for None explicitly
        output = read_all_files_in_folder(folder_path, output_type)

    return output
