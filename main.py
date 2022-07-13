from PyQt5 import (QtWidgets, QtCore)
import sys
import UI_design
import time
import datetime
import threading
# import concurrent.futures
import resource_parser
import PDF_generator


class DownloadResource(QtCore.QThread):
    trigger = QtCore.pyqtSignal(str)

    def __init__(self, title, source_url, url_list):
        QtCore.QThread.__init__(self)
        self.url_list = url_list
        self.source_url = source_url
        self.title = title

    def __del__(self):
        self.wait()

    def run(self):
        self.download_path = ""
        dir_status = resource_parser.create_directory(self)
        # self.trigger.emit(dir_status)

        threads = []

        for i in range(len(self.url_list)):
            threads.append(threading.Thread(
                target=resource_parser.save_pictures, args=(self, i)))
            threads[i].start()
            time.sleep(0.4)

        for i in range(len(self.url_list)):
            threads[i].join()
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            info = f"{current_time} Page {i + 1} is captured"
            self.trigger.emit(info)


class GUI(QtWidgets.QMainWindow, UI_design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.resource_fetch)
        self.pushButton_2.clicked.connect(self.resource_download)
        self.pushButton_3.clicked.connect(self.output_PDF)
        self.url_list = []
        self.title = ""
        self.source_url = ""
        # self.url_list = ['/TM_DO/008/100634896/001028542/a0000001_watered_watered_72dpi.jpg', '/TM_DO/008/100634896/001028542/a0000002_watered_watered_72dpi.jpg', '/TM_DO/008/100634896/001028542/a0000003_watered_watered_72dpi.jpg']
        # self.title = "5456"
        # self.source_url = "https://tm.ncl.edu.tw/article?u=008_001_0000350939&lang=chn"

    def resource_fetch(self):
        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.statusBar().showMessage(f"{start_time} 開始抓取", 5000)
        self.source_url = self.plainTextEdit.toPlainText()

        if(self.source_url):
            # print(self.source_url)
            resource_parser.get_resources(self, self.source_url)
            # print(self.url_list)
            finish_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.statusBar().showMessage(f"{finish_time} 抓取完成", 5000)
        else:
            QtWidgets.QMessageBox.information(
                self, "尚未輸入書籍網址", "請填入書籍網址", QtWidgets.QMessageBox.Ok)

    def resource_download(self):
        self.list_submissions.clear()
        self.progressBar.setMaximum(len(self.url_list))
        self.progressBar.setValue(0)
        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.statusBar().showMessage(f"{start_time} 開始下載圖片...", 10000)
        self.get_thread = DownloadResource(
            self.title, self.source_url, self.url_list)
        self.get_thread.trigger.connect(self.add_info)
        self.get_thread.finished.connect(self.done)
        self.get_thread.start()

    def output_PDF(self):
        self.output_path = ""
        status = PDF_generator.img_to_pdf_convert(self)
        QtWidgets.QMessageBox.information(self, "輸出 PDF", status)

    def add_info(self, info_text):
        self.list_submissions.addItem(info_text)
        self.progressBar.setValue(self.progressBar.value() + 1)

    def done(self):
        QtWidgets.QMessageBox.information(self, "資料已下載", "圖片抓取完成！")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = GUI()
    window.show()
    sys.exit(app.exec_())
