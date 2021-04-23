"""
Разбор графических файлов

Форматы данных: PFD JPEG
Шаблоны разные N штук
Искомое поле: 2 вариант
"""
import typing
from pathlib import Path
import PyPDF2
from PyPDF2.utils import PdfReadError
import pytesseract
#import PIL
from PIL import Image
import re


# PDF to Image

def pdf_image_extract(pdf_path: Path, image_path: Path) -> typing.List[Path]:
    result = []
    with pdf_path.open('rb' ) as file:
        try:
            pdf_file = PyPDF2.PdfFileReader(file)
        except PdfReadError:
            # запись в БД о кривом файле
            return result
        # print(1)
        for page_num, page in enumerate(pdf_file.pages, 1):
            image_file_name = f{pdf_path.name}_{page_num}
            image_data = page['/Resorces']['/XObject']['/Im0'].data
            image_path = images_path.joinpath(image_file_name)
            images_path.write_bytes(image_data)
            result.append(images_path)
    return result

# Iamge to Txt
def get_serial_number(image_path:Path) -> typing.List[str]:
    result = []
    image = Image.open(image_path)
    text_rus = pytesseract.image_to_string(image, 'rus')
    pattern = re.compile(r"(заводской.*[номер|№])")
    matches = len(re.findall(pattern, text_rus))

    if matches:
        text_eng = pytesseract.image_to_string(image, "eng").split('\n')
        for idx, line in enumerate(text_rus.split('\n')):
            if re.match(pattern, line):
                result.append(text_eng[idx].split()[-1])
    return result

if __name__ == '__main__':
    images_path = Path(__file__).parent.joinpath("images")
    if not images_path.exists():
        images_path.mkdir()

    pdf_file = Path(__file__).parent.joinpath("8416_4.pdf")
    images = pdf_image_extract(pdf_file, images_path)
    numbers = list(map(get_serial_number, images))
    print(1)
