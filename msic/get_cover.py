#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from msic.get_data import get_data
import requests
from PyQt5.QtCore import QStringListModel, QThread, pyqtSignal
import os


class get_img(QThread):
    pro = pyqtSignal(int, int)

    def __init__(self, id, which_, stats):
        super().__init__()
        self.url = get_data(id, which_, stats)

    def run(self):
        folder = os.path.exists(os.path.abspath(
            "")+"\\zRain\\"+self.url[1]) 
        if not folder:
            os.makedirs(os.path.abspath("")+"\\zRain\\"+self.url[1])
        data = requests.get(self.url[0], stream=True)
        size = int(data.headers["Content-Length"])
        wj = open("zRain/"+self.url[1]+"/cover.jpg", "wb")
        offset = 0
        for chunk in data.iter_content(chunk_size=2048):
            if not chunk:
                break
            wj.seek(offset)
            wj.write(chunk)
            offset = offset + len(chunk)
            proess = offset / int(size) * 100
            self.pro.emit(int(proess), 3)
