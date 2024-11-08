import pypdf
import datetime
import pathlib
import shutil
import pdfriend.classes.exceptions as exceptions
from typing import Self
from PIL import Image
from pdfriend.classes.platforms import Platform

class PDFWrapper:
    def __init__(self,
        source: pathlib.Path = None,
        pages: list[pypdf.PageObject] = None,
        metadata: pypdf.DocumentInformation = None,
        reader: pypdf.PdfReader = None,
    ):
        self.source = source
        self.pages = pages or []
        self.metadata = metadata
        self.reader = reader
        if metadata is not None:
            self.metadata = dict(metadata)

    def __getitem__(self, num: int) -> pypdf.PageObject:
        return self.pages[num - 1]

    def __setitem__(self, num: int, page: pypdf.PageObject):
        self.pages[num - 1] = page

    @classmethod
    def Read(cls, filename: str):
        pdf = pypdf.PdfReader(filename)

        return PDFWrapper(
            source = pathlib.Path(filename),
            pages = list(pdf.pages),
            metadata = pdf.metadata,
            reader = pdf,
        )

    def reread(self, source: pathlib.Path, keep_metadata: bool = True):
        new_pdf = PDFWrapper.Read(source)
        self.pages = new_pdf.pages
        if not keep_metadata:
            self.metadata = new_pdf.metadata

        return self

    def len(self):
        return len(self.pages)

    def slice(self, slice_str: str) -> list[int]:
        if slice_str == "all":
            return list(range(1, self.len()))

        result = []
        for subslice in slice_str.split(","):
            if ":" not in subslice:
                page_num = int(subslice)
                if page_num < 1 or page_num > self.len():
                    continue

                result.append(page_num)
                continue

            split_subslice = subslice.split(":")
            first, last = split_subslice[0], split_subslice[-1]

            # such that n: means n:end and :n means 1:n
            first = 1 if first == "" else int(first)
            last = self.len() if last == "" else int(last)

            # making sure the subrange is within bounds
            lower = max(min(first, last), 1)
            upper = min(max(first, last), self.len())

            result.extend(list(range(lower, upper + 1)))

        return sorted(list(set(result)))

    def subset(self, slice: str | list[str]) -> Self:
        if isinstance(slice, str):
            slice = self.slice(slice)

        return PDFWrapper(
            source = self.source,
            pages = [self.pages[idx - 1] for idx in slice],
            metadata = self.metadata
        )

    def raise_if_out_of_range(self, page_num: int):
        if page_num >= 1 and page_num <= self.len():
            return
        raise exceptions.ExpectedError(
            f"page {page_num} doesn't exist in the PDF (total pages: {self.len()})"
        )

    def rotate_page(self, page_num: int, angle: float) -> Self:
        int_angle = int(angle)
        if int_angle % 90 == 0:
            self[page_num].rotate(int_angle)
            return self

        rotation = pypdf.Transformation().rotate(angle)
        self[page_num].add_transformation(rotation)
        return self

    def pop_page(self, page_num: int) -> pypdf.PageObject:
        return self.pages.pop(page_num - 1)

    def append_page(self, page: pypdf.PageObject) -> Self:
        self.pages.append(page)
        return self

    def extend(self, pages: list[pypdf.PageObject]) -> Self:
        self.pages.extend(pages)
        return self

    def swap_pages(self, page_num_0: int, page_num_1: int) -> Self:
        temp = self[page_num_0]
        self[page_num_0] = self[page_num_1]
        self[page_num_1] = temp

        return self

    def merge_with(self, other: Self) -> Self:
        self.pages.extend(other.pages)

        return self

    def invert(self) -> Self:
        self.pages = self.pages[::-1]

        return self

    def weave_with(self, other: Self) -> Self:
        result = PDFWrapper()
        for odd_page, even_page in zip(self.pages, other.pages):
            result.extend([odd_page, even_page])

        if self.len() > other.len():
            result.extend(self.pages[other.len():])
        elif other.len() > self.len():
            result.extend(other.pages[self.len():])

        return result

    def to_writer(self):
        writer = pypdf.PdfWriter()
        if self.reader is not None and False: # FIXME
            writer.clone_document_from_reader(self.reader)
        else:
            for page in self.pages:
                writer.add_page(page)

        return writer

    def write(self, filename: str = None, keep_metadata = True):
        if filename is None:
            filename = self.source

        writer = self.to_writer()
        if keep_metadata and self.metadata is not None:
            writer.add_metadata(self.metadata)

        writer.write(
            pathlib.Path(filename).with_suffix(".pdf")
        )

    def backup(self, name: str | pathlib.Path = None, copy: bool = True) -> pathlib.Path:
        if name is None:
            name = self.source

        if not isinstance(name, pathlib.Path):
            name = pathlib.Path(name)

        now: str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        backup_file: pathlib.Path = Platform.NewBackup(
            f"{name.stem}_{now}.pdf"
        )

        # prefer to just copy the file from the source if possible
        if copy and self.source.is_file():
            shutil.copyfile(self.source, backup_file)
        else:
            self.write(backup_file)

        return backup_file


def convert_to_rgb(img_rgba: Image.Image):
    try:
        img_rgba.load()
        _, _, _, alpha = img_rgba.split()

        img_rgb = Image.new("RGB", img_rgba.size, (255, 255, 255))
        img_rgb.paste(img_rgba, mask=alpha)

        return img_rgb
    except (IndexError, ValueError):
        return img_rgba


class ImageWrapper:
    def __init__(self, images: list[Image.Image]):
        self.images = [convert_to_rgb(image) for image in images]

    @classmethod
    def FromFiles(cls, filenames: list[str]) -> Self:
        return ImageWrapper([Image.open(filename) for filename in filenames])

    def equalize_widths(self):
        max_width = max([image.size[0] for image in self.images])

        for i, image in enumerate(self.images):
            width, height = image.size

            scale = max_width / width

            self.images[i] = image.resize((max_width, int(height * scale)))

    def write(self, outfile: str, quality: int | float):
        self.images[0].save(
            outfile,
            "PDF",
            optimize=True,
            quality=int(quality),
            save_all=True,
            append_images=self.images[1:],
        )
