import os
from fpdf import FPDF
from PyQt5 import (QtWidgets)


def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def img_to_pdf_convert(self):
    if not self.title:
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Choose the target folder", "./")
        self.title = os.path.basename(path)
    else:
        if self.output_path != '':
            root = self.output_path
        else:
            root = "img"

        path = f"./{root}/{self.title}"
        if not os.path.exists(path):
            return

    create_path("./pdf")

    try:
        imagelist = [i for i in os.listdir(path) if i.endswith(".jpg")]
    except FileNotFoundError:
        return "圖檔路徑為空，請確認是否有下載圖檔"

    pdf = FPDF()
    # imagelist is the list with all image filenames
    for image in imagelist:
        img_path = f"{path}/{image}"
        pdf.add_page()
        pdf.image(img_path, 0, 0, 210, 297)

    # Remove the file if it exists
    if os.path.exists(f"./pdf/{self.title}.pdf"):
        os.remove(f"./pdf/{self.title}.pdf")

    # print("Picture loaded, Start Converting")
    pdf.output(f"./pdf/{self.title}.pdf", "F")
    return "PDF 轉換完成"
