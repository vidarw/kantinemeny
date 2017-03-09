#!/usr/bin/env python3

import time
import os.path
import json
from collections import OrderedDict
from operator import itemgetter

import requests
from openpyxl import load_workbook


class Cafeterias(dict):
    url = "http://www.tibeapp.no/hosted/albatross/getKantiner.php"
    default_location = os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)),
                     '../data',
                     'kantiner.json'))

    def __init__(self, location="default"):
        if location == "default":
            self.json = json.load(open(self.default_location))
        else:
            self.json = self._get()

        self.data = self._map_cafeterias()
        self.list = [(x, self.data[x]) for x in sorted(self.data.keys())]

        super().__init__(self.data)

    def _get(self):
        r = requests.get(self.url, stream=True)
        r.raise_for_status()

        return r.json()

    def _map_cafeterias(self):
        cafeterias = {}
        for cafeteria in self.json:
            if not cafeteria.get("url", None):
                continue

            filename = os.path.basename(cafeteria["url"])
            shortname = os.path.splitext(filename)[0].lower()

            cafeterias[shortname] = {
                "filename": filename,
                "location": cafeteria["title"]
            }

        return cafeterias

class Kantinemeny(dict):

    url_template = "http://netpresenter.albatross-as.no/xlkantiner/{}"
    days = ('mandag', 'tirsdag', 'onsdag', 'torsdag', 'fredag')
    timestamp = None

    def __init__(self, location="Nøstegaten 58", filename="Nostegaten58.xlsx"):
        self.location = location
        self.filename = filename
        self.url = self.url_template.format(self.filename)
        self.workbook = load_workbook(self._get())

        self.timestamp = time.time()

        super().__init__(self.menu)

    def _get(self):
        r = requests.get(self.url, stream=True)
        r.raise_for_status()

        return r.raw

    def _parse_menu(self, menu):
        menu = self.workbook[menu]

        rows = [('B1', 'B2'), ('B3', 'B4'), ('B5', 'B6'),
                ('B7', 'B8'), ('B9', 'B10')]

        dishes = {}
        for i in zip(self.days, rows):
            dish = '\n'.join([menu[r].value.strip() for r in i[1] if menu[r].value])
            dishes[i[0]] = dish

        return dishes

    @property
    def soups(self):
        return self._parse_menu('Suppe ukemeny')

    @property
    def hot_dishes(self):
        return self._parse_menu('Ukens Varmmat meny')

    @property
    def menu(self):
        return {
            "supper": self.soups,
            "varmmat": self.hot_dishes
        }


if __name__ == "__main__":
    from pprint import pprint
    # k = Kantinemeny("Nostegaten58")
    # pprint(k.timestamp)
    # print(Cafeterias.default_location)
    c = Cafeterias()
    print(c.list)