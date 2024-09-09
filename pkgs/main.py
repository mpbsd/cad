#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from unidecode import unidecode

spc_dash_spc_word = re.compile(r"^((i{1,3}|i?v) - ([0-9]+)?)([a-z -]+)")
spc_dash = re.compile(r"^(i{1,3}|i?v) -$")
spc_dash_spc = re.compile(r"^(i{1,3}|i?v) - ([0-9]+)$")

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

    with webdriver.Chrome(options=options) as driver:
        driver.get(doc_url)
        driver.implicitly_wait(0.5)
        beautiful_soup = BeautifulSoup(driver.page_source, "lxml")
        with open("brew/A2RC182017.csv", "w") as csvfile:
            for table in beautiful_soup.find_all("table"):
                for row in table.find_all("tr"):
                    info = [
                        unidecode(col.text.lower()).strip()
                        for col in row.find_all("td")
                    ]
                    if len(info) == 1:
                        info = [
                            spc_dash_spc_word.search(info[0]).group(1).strip(),
                            spc_dash_spc_word.search(info[0]).group(4).strip(),
                        ]
                        if spc_dash.search(info[0]):
                            info[0] = spc_dash.search(info[0]).group(1)
                        elif spc_dash_spc.search(info[0]):
                            info[0] = spc_dash_spc.sub(r"\1-\2", info[0])
                        pr = "{};{};;;;".format(info[0], info[1])
                    else:
                        pr = ";{};{};{};{};{}".format(
                            info[0], info[1], info[2], info[3], info[4]
                        )
                    print(pr, file=csvfile)


if __name__ == "__main__":
    main()
