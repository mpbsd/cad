#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

wschar = re.compile(r"\xa0")

doc_url = (
    "https://docs.google.com/document/d/e/"
    "2PACX-1vTh8sOz5qjNOK_zXUFtnAnn3pgNmBv"
    "wQMCFWvxKh9TxjBvgqmllpakoITbAeBPHe6Lv"
    "kqnek5-MceZ1/pub?landscape=true"
)


def main():
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)

    driver.get(doc_url)

    driver.implicitly_wait(0.5)

    beautiful_soup = BeautifulSoup(driver.page_source, "lxml")

    driver.implicitly_wait(0.5)

    driver.quit()

    for table in beautiful_soup.find_all("table"):
        for row in table.find_all("tr"):
            data = [wschar.sub(r"", col.text) for col in row.find_all("td")]
            print(data)


if __name__ == "__main__":
    main()
