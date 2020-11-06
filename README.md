# 臺灣記憶電子書下載器
## 簡介 Intro
國家圖書館蒐集典藏了相當豐富的臺灣文獻史，建立了「臺灣記憶 Taiwan Memory」網站，將這些珍貴的文獻分享給大家。然而上頭的歷史書籍電子書是以一張一張的 JPG 圖片組成，沒有提供 PDF 檔，不可能因為想要下載一本書而點擊上千次的下載嘛，太浪費生命了，因此從事古蹟修復的學姊在研究需求下向我求助。我利用 PyQt5 製作該程式，可發送 Request 抓取書籍圖片連結並進行下載，並可以將所有圖片輸出成一份 PDF。

邊練技能還可以叫她請我吃飯，舒服。

## 環境設定 Environment
1. 本程式在 Python 3.8.4 64-bit 環境下開發，中文的安裝教學可以看[打工仔登入助手](https://reurl.cc/5qEWrM)
2. 在 CMD 或 Terminal 中執行 ```pip install -r requirements.txt``` 安裝會使用到的套件

## 架構 Structure
### 使用套件 Packages
* ```PyQt5```: To build the GUI, I designed it in Qt Designer.
* ```BeautifulSoup```: To fetch all the URL of images.
* ```requests```: To send GET requests to download the image.
* ```fpdf```: To convert PNG into PDF.

### 檔案內容 Files
* ```main.py```: the main file of the application.
* ```resourece_parser.py```: the parser to fetch all the resource paths
* ```UI_design.py```: the GUI converted from the ```.ui``` file generated by Qt Designer
* ```PDF_generator```: To convert images into a PDF order by order.

> Threading: I used thread to download images simultaneously. Instead of waiting for one after another, it greatly saved user's time.

## 使用步驟說明 Usage
1. 打開 CMD 或 Terminal 並切換到資料夾路徑，輸入 ```python .\main.py```，執行該工具
    
    ![](https://i.imgur.com/iOaH9HF.png)
3. 輸入欲下載的電子書網頁連結
    > 假如我今天想要下載《臺灣文化志上卷》，那就複製這個網頁的連結
    > 
    > ![](https://i.imgur.com/Fb0jbgN.png)
    > 
    > 很明顯地該網站只有提供一頁一頁的圖檔下載，手動下載的話會弄到往生
    > ![](https://i.imgur.com/GECKCOS.png)
4. 點擊「抓取來源」獲取所有圖片連結，等候完成。

    > 未來會加入自訂路徑，該功能實做很簡單，只是開發階段用不上所已沒有做。

5. 點擊「下載圖檔」，這個步驟所花費的時間與下載的頁數成正比，頁數越多時間越久，完成後底下的狀態列會顯示「抓取完成」，可以到目錄裡的 ```img``` 確認。
    > 可以到 ```img``` 資料夾裡面檢查有沒有順利下載
    > 
    > ![](https://i.imgur.com/liZShFx.png)
    > 
    > 未來在中間的 Message Box 會顯示已下載哪一份圖檔，底下的進度條會顯示目前進度，不過這個功能還在開發中。
6. 點擊「輸出 PDF」會將目前所有下載好的圖片依照檔名順序轉換成 PDF。
    > ![](https://i.imgur.com/avKUgF9.png)

7. 香噴噴的文獻可以列印出來讀囉！


