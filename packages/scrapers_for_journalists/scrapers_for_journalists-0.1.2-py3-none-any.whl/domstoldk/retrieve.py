import os
from argparse import ArgumentParser

import pandas as pd
from base import BaseScraper
from tqdm import tqdm


class DomStolScraper(BaseScraper):
    """
    Scraping "retslister" from domstol.dk
    """

    def parse_case(self, case_text: str, metadata: dict):
        data = {
            "fuld tekst": case_text,
            "overskrift": self.extract(r"\<strong>(.*?)\<\/strong>", case_text),
            "sagstype": self.extract(
                r"Borgerlig sag.*?(?=<|$)|Straffesag.*?(?=<|$)|Tvangsauktion.*?(?=<|$)",
                case_text,
            ),
            "dato_første": self.extract(r"\d{2}-\d{2}-\d{4}", case_text, slicing=0),
            "dato_sidste": self.extract(r"\d{2}-\d{2}-\d{4}", case_text, slicing=-1),
            "rettens journalnr": self.extract(
                r"Rettens j\.nr.: (.*?)(?=<|$)", case_text
            ),
            "dommer": self.extract(r"Dommer: (\w+ \w+ \w+|\w+ \w+)", case_text),
            "advokater": self.extract(r"Advokat: (\w+ \w+ \w+|\w+ \w+)", case_text),
            "sagsøger": self.extract(r"Sagsøger: (.*?)\<br", case_text),
            "sagsøgers_advokat": self.extract(
                r"Sagsøgers advokat: (.*?)\<br", case_text
            ),
            "sagsøgte": self.extract(r"Sagsøgte: (.*?)\<br", case_text),
            "sagsøgtes advokat": self.extract(
                r"Sagsøgtes advokat: (.*?)\<br", case_text
            ),
            "klagers advokat": self.extract(r"Klagers advokat: (.*?)\<br", case_text),
            "foged": self.extract(r"Foged: (.*?)(?=<|$)", case_text),
            "rekvirent": self.extract(r"Rekvirent: (.*?)(?=<|$)", case_text),
            "rekvirent_advokat": self.extract(
                r"Rekvirent advokat: (.*?)(?=<|$)", case_text
            ),
            "skyldner": self.extract(r"Skyldner: (.*?)(?=<|$)", case_text),
            "matrikelnr": self.extract(r"Matr\.Nr\.: (.*?)(?=<|$)", case_text),
            "matrikel_beliggenhed": self.extract(
                r"Beliggende: (.*?)(?=<|$)", case_text
            ),
            "sagen drejer sig om": self.extract(
                r"Sagen drejer sig om: (.*?)(?=<|$)", case_text
            ),
            "anklagemyndighed": self.extract(
                r"Anklagemyndighed: (.*?)(?=<|$)", case_text
            ),
            "politi journalnr": self.extract(
                r"Politiets journalnr\.: (.*?)(?=<|$)", case_text
            ),
            "offentlighed": self.extract(r"Retsmødet er (\w+)", case_text),
        }

        data.update(metadata)
        return data

    def validate_text(self, case_text: str) -> bool:
        if any(
            [
                day in case_text.lower()
                for day in ["mandag", "tirsdag", "onsdag", "torsdag", "fredag"]
            ]
        ):
            return False
        elif "Det bemærkes at retssal 6 og 7 er i Thisted" in case_text:
            return False
        elif "ingen tvangsauktioner i denne uge" in case_text:
            return False
        elif case_text == "":
            return False
        elif not any(
            [case in case_text for case in ["Borgerlig", "Straffesag", "Tvangsauktion"]]
        ):
            return False
        else:
            return True

    def check_for_double_line_format(self, soup) -> bool:
        return (
            self.extract(
                r"\d{2}-\d{2}-\d{4}",
                " ".join([e.text for e in soup.select("div.editor-content p")]),
            )
            is None
        )

    def scrape_court(self, court: str) -> pd.DataFrame:
        url = f"https://domstol.dk/{court}/retslister/"

        # Find categories
        soup = self.get(url)
        categories = [a["href"] for a in soup.select("a.latest-article-list-item")]

        # Go through pages within categories
        cases = []
        for category_link in categories:
            soup = self.get(category_link)

            try:
                if self.check_for_double_line_format(soup):
                    new_cases = soup.select("div.editor-content")[0].text.split("\xa0")
                else:
                    new_cases = [
                        case.decode_contents()
                        for case in soup.select("div.editor-content p")
                    ]
            except Exception as e:
                Warning(f"Found no cases at page: {category_link}. ERROR: {e}")
                continue

            new_cases = [
                self.parse_case(case, metadata={"url": category_link, "domstol": court})
                for case in new_cases
                if self.validate_text(case)
            ]
            cases += new_cases

        return pd.DataFrame(cases)

    def prepare_df(self, df: pd.DataFrame) -> pd.DataFrame:
        # Filter only Straffesag
        df = df[df["sagstype"].fillna("").str.contains("Straffesag")]

        # Add gerningskoder fra DST
        # afg_ger9 = pd.read_html(
        #     "http://www.dst.dk/da/Statistik/dokumentation/Times/kriminalstatistik/afg-ger9"
        # )[0]
        # afg_ger9["Kode"] = afg_ger9["Kode"].astype(str)
        # afg_ger9["code1"] = afg_ger9["Kode"].apply(lambda x: x[0])
        # afg_ger9["code2"] = afg_ger9["Kode"].apply(lambda x: x[:2])
        # afg_ger9["code4"] = afg_ger9["Kode"].apply(lambda x: x[:4])
        # afg_ger9["code5"] = afg_ger9["Kode"].apply(lambda x: x[-5:])
        # afg_ger9 = afg_ger9.rename(columns={"Tekst": "Tekst5"})
        # afg_ger9 = afg_ger9[["Kode", "code1", "code2", "code4", "code5", "Tekst5"]]

        # code_to_text_1 = {
        #     "0": "Uoplyst",
        #     "1": "Straffelov i alt",
        #     "2": "Færdselslov i alt",
        #     "3": "Øvrige særlige i alt",
        # }

        # code_to_text_2 = {
        #     "0": "Uoplyst straffelov",
        #     "00": "Uoplyst Straffelov",
        #     "10": "Uoplyst straffelov",
        #     "11": "Seksual forbrydelser",
        #     "12": "Voldsforbrydelser",
        #     "13": "Ejendomsforbrydelser",
        #     "14": "Andre forbrydelser",
        #     "21": "Færdseæsuheld specificeret",
        #     "22": "Færdselslov spiritus",
        #     "24": "Mangler ved køretøj",
        #     "26": "Færdselslov i øvrigt",
        #     "32": "Lov om euforiserende stoffer",
        #     "34": "Våbenloven",
        #     "36": "Skatte- og afgiftslove",
        #     "38": "Særlove i øvrigt",
        # }

        # afg_ger9["Tekst1"] = afg_ger9["code1"].apply(lambda x: code_to_text_1[x])
        # afg_ger9["Tekst2"] = afg_ger9["code2"].apply(lambda x: code_to_text_2[x])
        afg_ger9 = pd.read_csv(
            os.path.join(os.path.dirname(__file__), "dst-afg-ger9.csv")
        )
        afg_ger9["code5"] = afg_ger9["code5"].astype(str)

        df["code5"] = df["politi journalnr"].fillna("").apply(self.split_police_codes)
        df = df.merge(afg_ger9, on="code5", how="left")

        # Sort chronologically from date
        df = df.sort_values("dato_første")

        return df

    @staticmethod
    def split_police_codes(value: str):
        try:
            return value.split("-")[1]
        except Exception:
            return None


if __name__ == "__main__":
    parser = ArgumentParser(prog="DomStolScraper", description="Scrapes domstol.dk")
    parser.add_argument(
        "--outfile", help="the path to save the Excel-file. Must end with .xlsx"
    )
    args = parser.parse_args()

    dfs = []
    courts = [
        "koebenhavn",
        "bornholm",
        "esbjerg",
        "frederiksberg",
        "glostrup",
        "helsingoer",
        "herning",
        "hilleroed",
        "hjoerring",
        "holbaek",
        "holstebro",
        "horsens",
        "kolding",
        "lyngby",
        "nykoebingfalster",
        "naestved",
        "odense",
        "randers",
        "roskilde",
        "svendborg",
        "soenderborg",
        "viborg",
        "aalborg",
        "aarhus",
    ]

    scraper = DomStolScraper()

    for court in tqdm(courts):
        dfs.append(scraper.scrape_court(court))

    final_df = pd.concat(dfs)
    final_df = scraper.prepare_df(final_df)

    final_df.to_excel(args.outfile, engine="openpyxl", index=False)
