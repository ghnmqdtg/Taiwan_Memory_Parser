import requests
from bs4 import BeautifulSoup
import random
import os
import datetime

random_user = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 OPR/42.0.2393.94",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.39",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
]

random_proxies = [
    "118.163.83.21",
    "198.199.120.102",
    "50.206.25.104",
    "50.206.25.105",
    "68.188.59.198",
    "168.169.96.14",
    "54.178.4.138"
]


def get_resources(self, url):
    headers_1 = {
        "Accept-Language": "en-GB,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Host": "tm.ncl.edu.tw",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "user-agent": random.choice(random_user)
    }
    proxies = {
        "http": random.choice(random_proxies)
    }
    response = requests.get(url, headers=headers_1, proxies=proxies)
    if response.status_code == requests.codes.ok:
        soup = BeautifulSoup(response.content, features='html.parser')
        # get title of the book
        self.title = soup.select(
            "#div-to-print > div:nth-child(2) > div.detail-td")[0].text
        # store the title into the list
        # fetch the url of all pages
        table = soup.find("table", {"class": "table table-hover table-responsive"})
        for idx, ref in enumerate(table.find_all('a')):
            # print(str(idx), ref.get('href'))  # for debugging
            self.url_list.append(ref.get('href'))


def creat_directory(self):
    if(self.download_path):
        path = self.download_path
    else:
        path = "./img/"
    try:
        if(self.title):
            os.mkdir(path + self.title)
            return f"已建立名為 {self.title} 的資料夾"
        else:
            return "尚未獲取書籍標題，請重新抓取來源"
    except OSError:
        return f"資料夾 {self.title} 已存在，內容將被覆寫"


def save_pictures(self, order):
    headers_2 = {
            "Accept-Language": "en-GB,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,en-US;q=0.6",
            "Cache-Control": "max-age=0",
            "Host": "tm.ncl.edu.tw",
            "Referer": self.source_url,
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "user-agent": random.choice(random_user)
    }
    proxies = {
        "http": random.choice(random_proxies)
    }
    try:
        source_url = "https://tm.ncl.edu.tw/" + self.url_list[order]
        data = requests.get(source_url, headers=headers_2, proxies=proxies)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if(data.status_code == requests.codes.ok):
            filename = str(order + 1).zfill(4)
            open((f"./img/{self.title}/{filename}.jpg"), "wb").write(data.content)
            print(f"{current_time} Page {order + 1} is captured")
            data.close()
        else:
            print(f"Connection Error Occurred at page {order}, status: {data.status_code}")
    except ConnectionResetError:
        print(f"ConnectionResetError Occurred at page {order}, status: {data.status_code}")
