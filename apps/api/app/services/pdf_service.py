import os
import tempfile
from datetime import datetime
from typing import Optional, List, Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from app.services.storage_service import storage_service

class PdfService:
    """Service for generating PDF documents and uploading to storage"""

    @staticmethod
    def generate_receipt(
        application_number: str,
        applicant_name: str,
        payment_id: str,
        amount: float,
        payment_date: datetime,
        program_name: Optional[str] = None
    ) -> str:
        """
        Generate PDF Receipt for Application Fee
        Returns: S3 URL or relative path to generated PDF
        """
        try:
            filename = f"Receipt_{application_number}_{payment_id}.pdf"
            temp_path = os.path.join(tempfile.gettempdir(), filename)
            
            doc = SimpleDocTemplate(temp_path, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle('Title', parent=styles['Heading1'], alignment=1, spaceAfter=20)
            elements.append(Paragraph("Payment Receipt", title_style))
            elements.append(Spacer(1, 12))
            
            # Info Table
            data = [
                ["Receipt No:", f"REC-{payment_id}"],
                ["Date:", payment_date.strftime("%d-%b-%Y %H:%M")],
                ["Application No:", application_number],
                ["Applicant Name:", applicant_name],
                ["Program:", program_name or "N/A"],
                ["Payment Mode:", "Online"],
                ["Transaction ID:", payment_id],
                ["Amount Paid:", f"INR {amount:.2f}"],
                ["Status:", "SUCCESS"]
            ]
            
            table = Table(data, colWidths=[150, 300])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (0, 0), (1, -1), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 20))
            
            # Footer
            footer_text = "This is a computer generated receipt and does not require a signature."
            elements.append(Paragraph(footer_text, styles['Normal']))
            
            doc.build(elements)
            
            # Upload to Storage (S3/MinIO)
            with open(temp_path, "rb") as f:
                content = f.read()
                file_url = storage_service.upload_bytes(
                    file_content=content,
                    filename=filename,
                    content_type="application/pdf",
                    prefix="receipts"
                )
            
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return file_url
            
        except Exception as e:
            print(f"Error generating receipt PDF: {str(e)}")
            return ""

pdf_service = PdfService()
