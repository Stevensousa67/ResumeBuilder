import re
import markdown2
from io import BytesIO
from xhtml2pdf import pisa


def convert_markdown_to_pdf(markdown_content):
    # Clean up Markdown code block markers (e.g., ```markdown or ```)
    markdown_content = re.sub(r'```(markdown)?', '', markdown_content, flags=re.IGNORECASE)
    markdown_content = re.sub(r"^```(?:markdown)?\n(.*?)\n?```", r"\1", markdown_content,
                              flags=re.DOTALL | re.MULTILINE)

    # Convert Markdown to HTML with markdown2
    html = markdown2.markdown(markdown_content, extras=['tables', 'fenced-code-blocks'])

    # Add custom CSS for better styling
    css = """
    <style>
        body {
            font-family: 'Helvetica', sans-serif;
            font-size: 12pt;
            line-height: 1.5;
            margin: 20px;
        }
        h1, h2, h3, h4, h5, h6 {
            font-weight: bold;
            margin-top: 2px;
            margin-bottom: 2px;
        }
        h1 {
            font-size: 18pt;
        }
        h2 {
            font-size: 16pt;
        }
        p {
            margin-bottom: 2px;
        }
        ul, ol {
            margin-left: 20px;
            margin-bottom: 2px;
        }
        li {
            margin-bottom: 2px;
        }
        strong {
            font-weight: bold;
        }
        a {
            color: #1a3c6d;
            text-decoration: underline;
        }
    </style>
    """

    # Combine CSS and HTML
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        {css}
    </head>
    <body>
        {html}
    </body>
    </html>
    """

    # Create a BytesIO buffer for the PDF
    pdf_buffer = BytesIO()

    # Generate PDF
    try:
        pisa_status = pisa.CreatePDF(full_html, dest=pdf_buffer)
        if pisa_status.err:
            print(f'Error generating PDF: {pisa_status.err}')
            raise Exception(f'Error generating PDF: {pisa_status.err}')
        print("PDF generated successfully")
    except Exception as e:
        print(f'Error generating PDF: {e}')
        raise

    # Get the PDF content
    pdf_content = pdf_buffer.getvalue()
    pdf_buffer.close()

    return pdf_content
