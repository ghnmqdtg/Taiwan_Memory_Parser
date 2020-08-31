import os
from fpdf import FPDF


def img_to_pdf_convert(title):
    img_dir = f"./img/{title}"

    imagelist = [i for i in os.listdir(img_dir) if i.endswith(".jpg")]

    pdf = FPDF()
    # imagelist is the list with all image filenames
    for image in imagelist:
        img_path = img_dir + "/" + image
        pdf.add_page()
        pdf.image(img_path, 0, 0, 210, 297)

    print("Picture loaded, Start Converting")
    pdf.output(f"./pdf/{title}.pdf", "F")
    print("PDF Generated Successfully")


if __name__ == "__main__":
    title = "臺灣文化志"
    img_to_pdf_convert(title)
