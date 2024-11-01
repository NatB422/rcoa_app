import io
import datetime
from openpyxl import load_workbook

def get_excel_file_creation_time(data:bytes) -> datetime.datetime:
    wb = load_workbook(io.BytesIO(data))
    return wb.properties.created
