import fitz
import logging
import os

logger = logging.getLogger(__name__)

class CVExtractorService:

    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """
        Extracts text from a PDF file using PyMuPDF (fitz).

        :param file_path: Path to the PDF file.
        :return: Extracted text as a string.
        """

        logger.info(f"Extracting text from PDF: {file_path}")

        # Check if the file exists
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        extracted_text = ""
        try:
            # Open the PDF file using fitz (PyMuPDF)
            with fitz.open(file_path) as pdf_document:
                # Loop through each page and extract text
                for page_number in range(pdf_document.page_count):
                    page_text = pdf_document.load_page(page_number).get_text()
                    extracted_text += page_text + "\n"

            logger.info(f"Successfully extracted text from PDF: {file_path}")
            # Return the extracted text, stripping any leading/trailing whitespace
            return extracted_text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {file_path}. Error: {e}")
            raise e
