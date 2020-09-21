import colorama
import os
import sys
import requests

from bs4 import BeautifulSoup
from _collections import deque


def is_url_valid(url):
    return '.' in url


def make_file_name(url):
    url_no_domain = url.rsplit('.')[0]
    return strip_http_protocol_if_needed(url_no_domain)


def save_website_to(path, content):
    with open(path, 'w', encoding='utf-8') as file:
        file.writelines(content)


def is_website_saved(path):
    return os.path.exists(path)


def print_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        print(file.readlines())


def get_content_from(url):
    r = requests.get(url)
    return r.content


def append_https_if_needed_to(url):
    https_str = "https://"
    if url.startswith(https_str):
        return url
    elif url.startswith("http://"):
        url.replace("http://", https_str, 1)
    else:
        return https_str + url


def strip_http_protocol_if_needed(url):
    https_str = "https://"
    http_str = "http://"
    if url.startswith(https_str):
        return url.replace(https_str, "", 1)
    elif url.startswith("http://"):
        url.replace(http_str, "", 1)
    else:
        return url


def extract_all_text(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        link.replace_with(BLUE + link.text)
    return soup.get_text()


directory_name = sys.argv[1]
if not os.path.exists(directory_name):
    os.mkdir(directory_name)

history = deque()

colorama.init(autoreset=True)
BLUE = colorama.Fore.BLUE

while True:
    cmd = input()
    if cmd == 'exit':
        break
    elif cmd == 'back':
        if len(history) >= 2:
            file_name = history[-2]
            history.pop()
            path = f'{directory_name}/{file_name}'
            print_file(path)
    elif not is_url_valid(cmd):
        print('Error: Invalid URL')
    else:
        url = append_https_if_needed_to(cmd)
        file_name = make_file_name(url)
        path = f'{directory_name}/{file_name}'
        if is_website_saved(path):
            print_file(path)
        else:
            text = extract_all_text(get_content_from(url))
            print(text)
            save_website_to(path, text)
        history.append(file_name)
