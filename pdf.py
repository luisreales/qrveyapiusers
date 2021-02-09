from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, Image, PageBreak, Paragraph
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import TableStyle
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor


def generate_pdf_new(data_users):

    # List of users  
    logo = Image('logo.jpg', 1 * inch, 1 * inch)
    logo.hAlign = 'LEFT'
    
    

    data = data_users
   
    buf = BytesIO()

    pdf = SimpleDocTemplate(
        buf,       
        pagesize=letter
    )
  

    table = Table(data)

    # add style

    style = TableStyle([
        ('BACKGROUND', (0, 0), (3, 0),  HexColor('#C7D4DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),

        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),

        ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])
    table.setStyle(style)

    # 2) Alternate backgroud color
    rowNumb = len(data)
    for i in range(1, rowNumb):
        bc = colors.white

        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        table.setStyle(ts)

    # 3) Add borders
    ts = TableStyle(
        [
            ('BOX', (0, 0), (-1, -1), -1, HexColor('#e7eaed')),

            ('LINEBEFORE', (2, 1), (2, -1), -1, colors.red),
            ('LINEABOVE', (0, 2), (-1, 2), -1, colors.green),

            ('GRID', (0, 0), (-1, -1), -1, HexColor('#e7eaed')),
        ]
    )
    table.setStyle(ts)

    elems = []
    
    elems.append(logo)
    elems.append(table)
   
  
    pdf.multiBuild(elems)
    pdf = buf.getvalue()
   
    return pdf