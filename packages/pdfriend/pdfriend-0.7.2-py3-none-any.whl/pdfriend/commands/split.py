import pdfriend.classes.wrappers as wrappers
import pdfriend.classes.platforms as platforms
import pathlib

def split(
    pdf: wrappers.PDFWrapper,
    split_indices: list[int],
    outdir: str
):
    if 1 not in split_indices:
        split_indices = [1] + split_indices
    if pdf.len() not in split_indices:
        split_indices.append(pdf.len())

    outdir_path = pathlib.Path(outdir)
    platforms.ensuredir(outdir_path)
    outfile = outdir_path.joinpath(pdf.source.stem)

    ndigits = len(str(len(split_indices) - 1))

    for i, (lower, upper) in enumerate(zip(
        split_indices[:-1], split_indices[1:]
    )):
        pdf_slice = wrappers.PDFWrapper(pages = pdf.pages[(lower-1):(upper-1)])
        pdf_slice.write(f"{outfile}-{i:0{ndigits}}.pdf")
