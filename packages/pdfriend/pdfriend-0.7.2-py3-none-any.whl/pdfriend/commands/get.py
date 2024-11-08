import pdfriend.classes.wrappers as wrappers
import pathlib

def get(pdf: wrappers.PDFWrapper, slice: str | list[int], outfile: str | pathlib.Path):
    pdf.subset(slice).write(outfile)

