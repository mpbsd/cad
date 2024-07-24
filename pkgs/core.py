#!/usr/bin/env python3

import re
import sys
from pathlib import Path

import pandas as pd
import pdfplumber
from unidecode import unidecode


class Beans:
    def __init__(self, taxnr, siape, years):
        self.taxnr = taxnr
        self.siape = siape
        self.years = years

    def PDFfiles(self):
        PDFfiles = {}
        for year in self.years:
            file = f"pdfs/{self.taxnr}-{self.siape}-{year}.pdf"
            if Path(file).is_file():
                PDFfiles[year] = file
        return PDFfiles

    def collect(self):
        beans = re.compile(
            r"item da resolucao: ([a-z0-9\s.-]+) pontuacao: (\d+(\.\d+)?)"
        )
        pouch = {}
        for year, file in self.PDFfiles().items():
            pouch[year] = {}
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text = unidecode(page.extract_text().lower())
                    for bean in beans.findall(text):
                        thing = bean[0].replace(r" ", r"")
                        point = float(bean[1])
                        if thing in pouch[year].keys():
                            pouch[year][thing].append(point)
                        else:
                            pouch[year][thing] = [point]
        return pouch

    def count(self):
        pouch = self.collect()
        for year in pouch.keys():
            pouch[year] = round(sum(sum(v) for v in pouch[year].values()), 2)
        return pouch

    def tabularize(self):
        pouch = {
            year: {thing: sum(beans) for thing, beans in pocket.items()}
            for year, pocket in self.collect().items()
        }
        beans = self.count()
        ODSfile = f"brew/{self.taxnr}-{self.siape}.ods"
        with pd.ExcelWriter(ODSfile, engine="odf") as writer:
            for year in pouch.keys():
                pouch[year]["Total"] = beans[year]
                df = pd.DataFrame.from_dict(
                    pouch[year], orient="index", columns=["Qtd"]
                )
                df.to_excel(writer, sheet_name=year)

    def __repr__(self):
        taxnr_siape = f"{self.taxnr}-{self.siape}:"
        years = " ".join(self.PDFfiles().keys())
        return taxnr_siape + " " + years


def usage():
    help = """
Exemplo de uso:

python3 -m pkgs.core \
(-t|--taxnr) <taxnr> \
(-s|--siape) <siape> \
(-y|--years) <years> \
<option>

(-t|--taxnr)  11 dígitos consecutivos, sem pontos ou traços
(-s|--siape)  7 dígitos consecutivos, sem pontos ou traços
(-y|--years)  Lista dos em avaliação, separados por espaços em branco
option        Deve ser uma das opções abaixo:
              (-c|--count)  Imprime a contagem de pontos dos anos indicados
              (-e|--excel)  Grava os pontos coletados em planilha segundo o
                            formato aberto de documentos (ODF)
"""
    print(help)


def main():
    re_taxnr = re.compile(r"(-t|--taxnr) (\d{11})\b")
    re_siape = re.compile(r"(-s|--siape) (\d{7})\b")
    re_years = re.compile(r"(-y|--years) (20\d{2}(?: 20\d{2})*)\b")
    re_count = re.compile(r"(-c|--count)")
    re_excel = re.compile(r"(-e|--excel)")
    if len(sys.argv) >= 8:
        opts = " ".join(sys.argv[1:])
        taxnr = re_taxnr.search(opts)
        siape = re_siape.search(opts)
        years = re_years.search(opts)
        count = re_count.search(opts)
        excel = re_excel.search(opts)
        if (taxnr and siape and years) and (count or excel):
            taxnr = re_taxnr.search(opts).group(2)
            siape = re_siape.search(opts).group(2)
            years = re_years.search(opts).group(2).split(" ")
            beans = Beans(taxnr, siape, years)
            if count:
                print(beans.count())
            elif excel:
                print(beans.tabularize())
        else:
            usage()
    else:
        usage()


if __name__ == "__main__":
    main()
