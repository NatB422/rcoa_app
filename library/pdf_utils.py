import io
from pandas import DataFrame
from reportlab.platypus import Table, Paragraph, PageTemplate, Frame, BaseDocTemplate, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape

padding = dict(
    leftPadding=72,
    rightPadding=72,
    topPadding=72,
    bottomPadding=18,
)

styles = getSampleStyleSheet()

portrait_template = PageTemplate(
    id='portrait',
    frames=Frame(0, 0, *A4, **padding),
    pagesize=A4,
)

landscape_template = PageTemplate(
    id='landscape',
    frames=Frame(0, 0, *landscape(A4), **padding),
    pagesize=landscape(A4),
)

def dataframe_to_table(df:DataFrame):
    # As suggested by https://nicd.org.uk/knowledge-hub/creating-pdf-reports-with-reportlab-and-pandas
    # Also has code suggestion for adding figures, using matplotlib

    df = df.reset_index().rename(columns = {'index':'date'})
    rows = [[Paragraph(col) for col in df.columns]] + df.values.tolist()
    return Table(
        rows,
        style=[
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('FONTSIZE', (0,1), (-1,-1), 8),
            ('LINEBELOW',(0,0), (-1,0), 1, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.lightgrey, colors.white]),
        ],
        hAlign = 'LEFT',
    )


def create_report():
    output = io.BytesIO()
    doc = BaseDocTemplate(
        output,
        pageTemplates=[
            # portrait_template,
            landscape_template
        ]
    )
    return doc, output


def export_to_pdf(title:str, dataframes:"dict[str, DataFrame]"):

    story = [
        Paragraph(title, styles['Heading1']),
    ]

    for table_title, table_df in dataframes.items():
        story.append(KeepTogether([
            Paragraph(table_title, styles['Heading2']),
            dataframe_to_table(table_df),
        ]))

    doc, output = create_report()

    doc.build(story)

    data = output.getvalue()

    return data
