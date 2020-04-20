#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
Created Date:       2020-04-17 00:28:19
Author:             Pagliacii
Last Modified By:   Pagliacii
Last Modified Date: 2020-04-17 23:37:57
Copyright © 2020-Pagliacii-MIT License
"""

import os
import sys
from threading import Event
from typing import Dict

import requests
from bs4 import BeautifulSoup

from threadpool import Pool


ROOTDIR = "documents"


class FetchFailed(Exception):
    pass


def get_html_content(url: str, headers: Dict, fname: str = "page.html") -> str:
    if not os.path.isfile(fname):
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise FetchFailed(f"Failed to get page from {url}")
        with open(fname, "w") as f:
            f.write(response.text)

    with open(fname) as f:
        return f.read()


def work(url: str, headers: Dict, fpath: str):
    if os.path.isfile(fpath):
        return
    response = requests.get(url, stream=True, headers=headers)
    if response.status_code != 200:
        raise FetchFailed(f"Failed to get content from {url}")
    temp_file = f"{fpath}.temp"
    with open(temp_file, "wb") as f:
        for chunk in response.iter_content(128):
            f.write(chunk)
    os.rename(temp_file, fpath)
    Event().wait(1)


def fetch():
    url = "http://pages.cs.wisc.edu/~remzi/OSTEP/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    try:
        content = get_html_content(url, headers)
    except FetchFailed:
        print(f"Error: failed to get response from {url=}", file=sys.stderr)
        exit(1)
    except Exception as e:
        print(f"Error: failed to run, caused by \"{e}\"", file=sys.stderr)
        exit(1)

    root_dir = ROOTDIR
    if not os.path.isdir(root_dir):
        os.mkdir(root_dir)

    soup = BeautifulSoup(content, "lxml")
    background_colors = ["yellow", "#f88017", "#00aacc", "#4CC417", "#3EA99F"]
    number = 0
    sub_dir = root_dir
    pool = Pool(10)
    pool.run()

    for idx, color in enumerate(background_colors):
        for td in soup.find_all("td", bgcolor=color):
            if (b := td.b) and b.text:
                sub_dir = f"{root_dir}/{idx}-{b.text}"
                if not os.path.isdir(sub_dir):
                    os.mkdir(sub_dir)
            if s := td.small:
                number = int(s.text) + 1
            if a := td.a:
                name = f"{str(number).zfill(2)} {a['href']}"
                fpath = f"{sub_dir}/{name}"
                file_url = f"{url}{a['href']}"
                pool.submit(work, url=file_url, headers=headers, fpath=fpath)
                number += 1

    pool.join()
