from bs4 import BeautifulSoup
import requests
from urllib.parse import urlsplit
import os
import time

URL = 'https://www.nro.gov/FOIA/Major-NRO-Programs-and-Projects/EOI-Documents/'
FOLDER = 'EOI-Documents'


def get_base_url(url):
    split_url = urlsplit(url)
    return split_url.scheme + '://' + split_url.netloc


def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def download_files(file_links, url):
    base_url = get_base_url(url)
    for link in file_links:
        url = base_url + link['href']
        print(url)
        filename = url.split('/')[-1]
        file_path = FOLDER + '/' + filename
        if os.path.exists(file_path):
            print('File exists:', file_path)
            continue
        response = requests.get(url)
        print('Writing:', file_path)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        time.sleep(1)



create_folder(FOLDER)
r = requests.get(URL)
soup = BeautifulSoup(r.text, 'html.parser')
files = soup.find("div", {"id": "dnn_ctr29001_HtmlModule_lblContent"})
links = files.findAll('a')
download_files(links, URL)
