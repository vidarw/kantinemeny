#!/usr/bin/env python3

import time

import requests
from openpyxl import load_workbook

location_map = {
    "nostegaten58": "Nostegaten58.xlsx",
    "nordrenostekai1": "NordreNostekai1.xlsx"
}


class Kantinemeny(dict):

    url_template = "http://netpresenter.albatross-as.no/xlkantiner/{}"
    days = ('mandag', 'tirsdag', 'onsdag', 'torsdag', 'fredag')
    timestamp = None

    def __init__(self, location):
        self.location = location.lower()
        self.filename = location_map[self.location]
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
    k = Kantinemeny("Nostegaten58")
    pprint(k.timestamp)
