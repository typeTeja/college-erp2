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
    def generate_receipt_bytes(
        application_number: str,
        applicant_name: str,
        payment_id: str,
        amount: float,
        payment_date: datetime,
        program_name: Optional[str] = None
    ) -> bytes:
        """
        Generate PDF Receipt in-memory and return bytes
        """
        try:
            from io import BytesIO
            buffer = BytesIO()
            
            doc = SimpleDocTemplate(buffer, pagesize=letter)
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
            
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            print(f"Error generating receipt PDF bytes: {str(e)}")
            return b""

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
        # ... (Existing implementation kept for backward compatibility if needed)
        # We can implement it using generate_receipt_bytes to avoid duplication
        
        pdf_bytes = PdfService.generate_receipt_bytes(
            application_number, applicant_name, payment_id, amount, payment_date, program_name
        )
        
        if not pdf_bytes:
            return ""
            
        filename = f"Receipt_{application_number}_{payment_id}.pdf"
        
        return storage_service.upload_bytes(
             file_content=pdf_bytes,
             filename=filename,
             content_type="application/pdf",
             prefix="receipts"
        )

pdf_service = PdfService()
