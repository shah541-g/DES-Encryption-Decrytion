from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
import os
from io import BytesIO
import textwrap

class PDFHandler:
    @staticmethod
    def readPdf(filePath):
        reader = PdfReader(filePath)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text

        # reader = PdfReader(file)
        # text = ""
        
        # # Loop through each page and append text
        # for page in reader.pages:
        #     text += page.extract_text() or ""  # Append page text (or empty if None)
        
        # return text

    @staticmethod
    

    def writePdf(filePath, text, width=612, height=792):
        try:
            # Create a PDF canvas at the specified file path
            c = canvas.Canvas(filePath, pagesize=(width, height))
        
            # Font settings
            font_name = "Helvetica"
            font_size = 12
            c.setFont(font_name, font_size)
    
            # Wrap text to fit within the page width
            wrapped_text = textwrap.wrap(text, width=80)
    
            # Starting position on the first page
            y_position = 750  
    
            for line in wrapped_text:
                # Calculate centered position
                text_width = c.stringWidth(line, font_name, font_size)
                x_position = (width - text_width) / 2  
                
                # Draw the string on the canvas
                c.drawString(x_position, y_position, line)
                
                # Adjust y-position for the next line
                y_position -= 15
                
                # If the y-position reaches near the bottom, start a new page
                if y_position < 50:
                    c.showPage()
                    y_position = 750  # Reset for the new page
                    c.setFont(font_name, font_size)  
    
            # Save the canvas to finalize the PDF
            c.save()
    
            print(f"PDF successfully written to {filePath}")
        except Exception as e:
            print(f"Error while writing PDF: {e}")
    