import requests
from bs4 import BeautifulSoup
import threading
import random
import os
import time
import datetime
import urllib3


def get_resources(url):
    response = requests.get(url, headers=headers_1, proxies=proxies)
    if response.status_code == requests.codes.ok:
        soup = BeautifulSoup(response.content, features='html.parser')
        # get title of the book
        title = soup.select(
            "#div-to-print > div:nth-child(2) > div.detail-td")[0].text
        # store the title into the list
        path.append(title)
        # fetch the url of all pages
        table = soup.find("table", {"class": "table table-hover table-responsive"})
        for idx, ref in enumerate(table.find_all('a')):
            # print(str(idx), ref.get('href'))  # for debugging
            url_list.append(ref.get('href'))


def creat_directory():
    try:
        os.mkdir("./img/" + path[0])
    except OSError:
        print("Directory already exists.")


def save_pictures(order):
    # time.sleep(random.randint(1, 10))
    try:
        source_url = "https://tm.ncl.edu.tw/" + url_list[order]
        data = requests.get(source_url, headers=headers_2, proxies=proxies)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if(data.status_code == requests.codes.ok):
            filename = str(order + 1).zfill(4)
            open((f"./img/{path[0]}/{filename}.jpg"), "wb").write(data.content)
            print(f"{current_time} Page {order + 1} is captured")
            data.close()
        else:
            print(f"Connection Error Occurred at page {order}, status: {data.status_code}")
    except ConnectionResetError:
        print(f"ConnectionResetError Occurred at page {order}, status: {data.status_code}")
    except urllib3.exceptions.ProtocolError:
        print(f"ConnectionResetError Occurred at page {order}, status: {data.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"ConnectionResetError Occurred at page {order}, status: {data.status_code}")


if __name__ == '__main__':
    url = "https://tm.ncl.edu.tw/article?u=008_001_0000350939&lang=chn"
    url_list = []
    path = []

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

    headers_1 = {
        "Accept-Language": "en-GB,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Host": "tm.ncl.edu.tw",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "user-agent": random.choice(random_user)
    }

    headers_2 = {
        "Accept-Language": "en-GB,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Host": "tm.ncl.edu.tw",
        "Referer": url,
        "Accept": "*/*",
        # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "user-agent": random.choice(random_user)
    }

    proxies = {
        "http": random.choice(random_proxies)
    }

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + "Start Running")
    get_resources(url)
    creat_directory()
    num_pages = len(url_list)
    print(f"Resources fetched, {num_pages} pages exists")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + "Start Downloading")

    threads = []
    for i in range(len(url_list)):
        threads.append(threading.Thread(target=save_pictures, args=(i,)))
        threads[i].start()
        time.sleep(0.4)

    for i in range(len(url_list)):
        threads[i].join()

    print("Pictures collected!")
