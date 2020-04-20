#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
Created Date:       2020-04-17 00:02:16
Author:             Pagliacii
Last Modified By:   Pagliacii
Last Modified Date: 2020-04-20 16:19:22
Copyright © 2020-Pagliacii-MIT License
"""

import os
from typing import Generator, Tuple

from PyPDF2 import PdfFileReader as Reader, PdfFileWriter as Writer
from PyPDF2.pdf import PageObject as Page

from fetch import fetch, ROOTDIR


def get_references_page_range(reader: Reader) -> Tuple[int, int]:
    low_bound = high_bound = -1
    for p in range(reader.getNumPages() - 1, -1, -1):
        page = reader.getPage(p)
        text = page.extractText()
        if "Homework" in text:
            high_bound = p
            continue
        if "References" in text:
            low_bound = p
            if high_bound == -1:
                high_bound = p + 1
            break

    return low_bound, high_bound


def get_all_references_pages(path: str) -> Generator[Page, None, None]:
    for dpath, _, filenames in os.walk(path):
        if not filenames:
            continue
        for name in filenames:
            file_path = f"{dpath}/{name}"
            reader = Reader(open(file_path, "rb"))
            low, high = get_references_page_range(reader)
            if low != -1 and high != -1:
                for p in range(low, high):
                    page = reader.getPage(p)
                    yield page


def main():
    # check if the folder named documents exist
    if not os.path.isdir(ROOTDIR):
        print("Downloading PDF files...")
        fetch()
        print("Download finished")

    writer = Writer()
    for page in get_all_references_pages(ROOTDIR):
        writer.addPage(page)

    with open("references.pdf", "wb") as output:
        writer.write(output)


if __name__ == "__main__":
    main()
