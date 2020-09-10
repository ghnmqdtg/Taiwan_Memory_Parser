import os
from fpdf import FPDF


def img_to_pdf_convert(self):
    if(self.output_path):
        path = self.output_path
    else:
        path = "./img/"

    path = f"./img/{self.title}"

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

    # print("Picture loaded, Start Converting")
    pdf.output(f"./pdf/{self.title}.pdf", "F")
    return "PDF 轉換完成"
