import io
import logging
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
from application import app

logger = logging.getLogger(__name__)

class PDFGenerationError(Exception):
    """Base exception for PDF generation errors"""
    pass

class PDFService:
    def __init__(self):
        self.config = app.config
        self.storage_path = Path(self.config['PDF_STORAGE_PATH'])
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def generate_quote_pdf(self, quote, product, logo_path=None):
        """Generate a quote PDF document with validated content"""
        try:
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            
            # Set up document styles
            self._setup_styles(pdf)
            
            # Add header with logo
            if logo_path and Path(logo_path).exists():
                self._add_header(pdf, logo_path)
            
            # Add quote information
            self._add_quote_details(pdf, quote, product)
            
            # Add product information
            y_position = self._add_product_details(pdf, product)
            
            # Add pricing tables
            self._add_pricing_tables(pdf, quote, y_position)
            
            # Add footer
            self._add_footer(pdf)
            
            pdf.save()
            return buffer.getvalue()
        except Exception as e:
            logger.error(f"PDF generation failed: {str(e)}")
            raise PDFGenerationError("Failed to generate PDF document") from e

    def _setup_styles(self, pdf):
        pdf.setTitle("Product Quote")
        pdf.setFont("Helvetica", 12)
        # Add more style configurations as needed

    def _add_header(self, pdf, logo_path):
        try:
            img = self._validate_and_resize_image(logo_path)
            pdf.drawImage(ImageReader(img), 50, 750, width=100, preserveAspectRatio=True)
        except Exception as e:
            logger.warning(f"Header image error: {str(e)}")
            # Fallback to text header
            pdf.drawString(50, 760, "Company Logo")

    def _validate_and_resize_image(self, image_path):
        """Validate and resize image to meet PDF requirements"""
        with Image.open(image_path) as img:
            if img.format.lower() not in ['jpeg', 'png', 'webp']:
                raise ValueError(f"Unsupported image format: {img.format}")
                
            max_width, max_height = self.config['PDF_MAX_IMAGE_DIMENSIONS']
            img.thumbnail((max_width, max_height))
            return img

    # Additional private methods for PDF sections would follow...
