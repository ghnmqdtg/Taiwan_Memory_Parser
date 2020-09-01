from PyQt5 import (QtWidgets)
import sys
import GUI
import time
import datetime
import threading
import resource_parser
import PDF_generator


class main(QtWidgets.QMainWindow, GUI.Ui_MainWindow, ):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.resource_fetch)
        self.pushButton_2.clicked.connect(self.resource_download)
        self.pushButton_3.clicked.connect(self.output_PDF)
        # self.url_list = []
        # self.title = ""
        # self.source_url = ""
        self.url_list = ['/TM_DO/008/100634896/001028542/a0000001_watered_watered_72dpi.jpg', '/TM_DO/008/100634896/001028542/a0000002_watered_watered_72dpi.jpg', '/TM_DO/008/100634896/001028542/a0000003_watered_watered_72dpi.jpg']
        self.title = "123"
        self.source_url = "https://tm.ncl.edu.tw/article?u=008_001_0000350939&lang=chn"

    def resource_fetch(self):
        self.source_url = self.plainTextEdit.toPlainText()

        if(self.source_url):
            print(self.source_url)
            start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.statusBar().showMessage(f"{start_time} 開始抓取", 5000)
            resource_parser.get_resources(self, self.source_url)
            finish_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.statusBar().showMessage(f"{finish_time} 抓取完成", 5000)
            print(self.url_list)
        else:
            self.statusBar().showMessage("請填入書籍網址", 5000)

    def resource_download(self):
        self.download_path = self.plainTextEdit_2.toPlainText()
        dir_status = resource_parser.creat_directory(self)
        self.statusBar().showMessage(dir_status, 5000)
        threads = []

        for i in range(len(self.url_list)):
            threads.append(threading.Thread(
                target=resource_parser.save_pictures(self, i)))
            threads[i].start()
            time.sleep(0.4)
            finish_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.statusBar().showMessage(f"{finish_time} 已下載第 {i + 1} 頁", 5000)

        for i in range(len(self.url_list)):
            threads[i].join()

    def output_PDF(self):
        self.output_path = self.plainTextEdit_3.toPlainText()
        status = PDF_generator.img_to_pdf_convert(self)
        self.statusBar().showMessage(status, 5000)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = main()
    window.show()
    sys.exit(app.exec_())
