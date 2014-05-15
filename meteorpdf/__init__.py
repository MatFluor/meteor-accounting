"""
    __init__.py "

    Author: H.C. v. Stockhausen < hc at vst.io >
    Date:    2012-10-14

"""

import cStringIO
import urllib
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus.flowables import Image
from reportlab.platypus import Paragraph, Spacer, KeepTogether, PageBreak
from reportlab.lib import colors
from reportlab.platypus.tables import Table, TableStyle

from theme import DefaultTheme
from util import calc_table_col_widths
from common import *

class Pdf(object):

    story = []    
    theme = DefaultTheme
    
    def __init__(self, title, author):
        self.title = title
        self.author = author
    
    def set_theme(self, theme):
        self.theme = theme
        
    def add(self, flowable):
        self.story.append(flowable)
    
    def add_header(self, text, level=H1):
        p = Paragraph(text, self.theme.header_for_level(level))
        self.add(p)
    
    def add_spacer(self, height_inch=None):
        height_inch = height_inch or self.theme.spacer_height
        self.add(Spacer(1, height_inch)) # magic 1? no, first param not yet implemented by rLab guys
        
    def add_paragraph(self, text, style=None):
        style = style or self.theme.paragraph
        p = Paragraph(text, style)
        self.add(p)
    
    def add_list(self, items, list_style=UL):
        raise NotImplementedError
    
    def add_table_auszug(self, rows, width=None, col_widths=None, align=CENTER,
            extra_style=[]):
        style = self.theme.auszug_style + extra_style
        if width and col_widths is None: # one cannot spec table width in rLab only col widths
            #col_widths = calc_table_col_widths(rows, width) # this helper calcs it for us
            col_widths = [50,50,190,60,50,50,50]
        table = Table(rows, col_widths, style=style, hAlign=align)
        self.add(table)

    def add_table_bilanz(self, rows, width=None, col_widths=None, align=CENTER,
            extra_style=[]):
        style = self.theme.bilanz_style + extra_style
        if width and col_widths is None: # one cannot spec table width in rLab only col widths
            #col_widths = calc_table_col_widths(rows, width) # this helper calcs it for us
            col_widths = [80,150,80,80,80,80,80]
        table = Table(rows, col_widths, style=style, hAlign=align)
        self.add(table)
        
    def add_bilanz_header(self, rows, width=None, col_widths=None, align=CENTER,
            extra_style=[]):
        style = self.theme.bilanz_header_style + extra_style
        if width and col_widths is None: # one cannot spec table width in rLab only col widths
            #col_widths = calc_table_col_widths(rows, width) # this helper calcs it for us
            col_widths = [80,78]
        table = Table(rows, col_widths, style=style, hAlign=align)
        self.add(table)
    
    def add_image(self, src, width, height, align=CENTER):
        img = Image(src, width, height)
        img.hAlign = align
        self.add(img)
        
    def add_qrcode(self, data, size=150, align=CENTER):
        "FIXME: ReportLib also supports QR-Codes. Check it out."
        
        src = "http://chart.googleapis.com/chart?"
        src += "chs=%sx%s&" % (size, size)
        src += "cht=qr&"
        src += "chl=" + urllib.quote(data)
        self.add_image(src, size, size, align)
    
    def render(self):
        buffer = cStringIO.StringIO()
        doc_template_args = self.theme.doc_template_args()
        doc = SimpleDocTemplate(buffer, title=self.title, author=self.author,
            **doc_template_args)
        doc.build(self.story)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf 
