import pdfriend.classes.wrappers as wrappers


def invert(pdf: wrappers.PDFWrapper, outfile: str):
    pdf.invert()

    pdf.write(outfile)
