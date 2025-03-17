import os

from fpdf import FPDF

from src.config import Config

PDF_TABLE_STYLE = {
    'row_height': 10,
    'title_font':    {'family': 'MyRoboto', 'size': 28},
    'subtitle_font': {'family': 'MyRoboto', 'size': 14},
    'headers_font':  {'family': 'MyRoboto', 'size': 14},
    'rows_font':     {'family': 'MyRoboto', 'size': 14},
    'table_width': 180,
}


class PdfTableGenerator:
    def __init__(self, title: str, subtitle: str, table: list[list], column_weights=None):
        self.title = title
        self.subtitle = subtitle
        self.headers = table[0]
        self.rows = table[1:]
        self.pdf: FPDF = FPDF('portrait', 'mm', 'a4')

        if column_weights is None:
            self.column_weights = [1 for _ in self.headers]
        else:
            assert len(self.headers) == len(column_weights), 'Wrong amount of column weights'
            self.column_weights = column_weights

        self.pdf.add_font('MyRoboto', '', Config.FONTS_DIR, uni=True)

    def generate_fpdf(self) -> FPDF:
        self.pdf.add_page()

        self.pdf.set_font(**PDF_TABLE_STYLE['title_font'])
        self._create_title()

        self.pdf.set_font(**PDF_TABLE_STYLE['subtitle_font'])
        self._create_subtitle()

        self.pdf.set_font(**PDF_TABLE_STYLE['headers_font'])
        self._create_table_row(self.headers)

        self.pdf.set_font(**PDF_TABLE_STYLE['rows_font'])
        for row in self.rows:
            self._create_table_row(row)

        self.pdf.set_author('Chess Organizer')

        return self.pdf

    def _create_title(self):
        self.pdf.cell(0, 15, str(self.title), ln=1, align='C')

    def _create_subtitle(self):
        self.pdf.cell(0, 20, str(self.subtitle), ln=1, align='C')

    def __get_fpdf_width(self):
        return self.pdf.w - self.pdf.l_margin - self.pdf.r_margin

    def __get_table_cell_size_and_offset(self):
        cell_size = PDF_TABLE_STYLE['table_width'] / sum(self.column_weights)
        cell_offset = (self.__get_fpdf_width() - PDF_TABLE_STYLE['table_width']) / 2
        return cell_size, cell_offset

    def _create_table_row(self, row):
        cell_size, cell_offset = self.__get_table_cell_size_and_offset()

        self.pdf.cell(cell_offset, PDF_TABLE_STYLE['row_height'])

        for item, col_weight in zip(row, self.column_weights):
            self.pdf.cell(cell_size * col_weight, PDF_TABLE_STYLE['row_height'], str(item), border=1, align='C')

        self.pdf.ln(PDF_TABLE_STYLE['row_height'])
