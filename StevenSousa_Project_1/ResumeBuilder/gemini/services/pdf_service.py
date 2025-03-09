import markdown2
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from bs4 import BeautifulSoup


def convert_markdown_to_pdf(markdown_content):
    """Convert markdown content to a PDF file"""
    html_content = markdown2.markdown(markdown_content)

    # Parse HTML to extract text elements
    soup = BeautifulSoup(html_content, 'html.parser')

    # Set up styles for the PDF
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(name='CustomNormal', fontSize=10, leading=12, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='CustomHeading1', fontSize=16, leading=20, alignment=TA_LEFT, spaceAfter=12))
    styles.add(ParagraphStyle(name='CustomHeading2', fontSize=14, leading=18, alignment=TA_LEFT, spaceAfter=10))

    # Create a PDF buffer
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)

    # Build the document elements
    elements = []

    # Process each HTML tag and map to ReportLab elements
    for element in soup.children:
        if element.name == 'h1':
            elements.append(Paragraph(element.get_text(), styles['CustomHeading1']))
            elements.append(Spacer(1, 12))
        elif element.name == 'h2':
            elements.append(Paragraph(element.get_text(), styles['CustomHeading2']))
            elements.append(Spacer(1, 10))
        elif element.name == 'p':
            elements.append(Paragraph(element.get_text(), styles['CustomNormal']))
            elements.append(Spacer(1, 6))
        elif element.name == 'ul':
            for li in element.find_all('li'):
                elements.append(Paragraph(f"• {li.get_text()}", styles['CustomNormal']))
                elements.append(Spacer(1, 4))
        elif element.name == 'ol':
            for idx, li in enumerate(element.find_all('li'), 1):
                elements.append(Paragraph(f"{idx}. {li.get_text()}", styles['CustomNormal']))
                elements.append(Spacer(1, 4))

        # Build the PDF
    doc.build(elements)

    # Get the PDF content
    pdf_content = pdf_buffer.getvalue()
    pdf_buffer.close()

    return pdf_content
