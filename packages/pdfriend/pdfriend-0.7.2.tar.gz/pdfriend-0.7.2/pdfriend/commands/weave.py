import pdfriend.classes.wrappers as wrappers

def weave(pdf_0: wrappers.PDFWrapper, pdf_1: wrappers.PDFWrapper, outfile: str):
    weaved_pdf = pdf_0.weave_with(pdf_1)

    weaved_pdf.write(outfile)
