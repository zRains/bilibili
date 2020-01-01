#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
from PyQt5.QtCore import QStringListModel,QThread,pyqtSignal
import requests

class tr(QThread):
    def __init__(self,title,stats,tr_no="False",tr_del="False"):
        super().__init__()
        self.stats=stats
        self.title=title
        self.tr_no=tr_no
        self.tr_del=tr_del

    def run(self):
        exe = os.path.exists(r"ffmpeg.exe")
        if not exe:
            print("下载组件。。。")
            r=requests.get("http://zrain.fldsw.cn/msic/ffmpeg.exe",stream=True)
            size=int(r.headers["Content-Length"])
            wj=open("ffmpeg.exe","wb")
            offset=0
            for chunk in r.iter_content(chunk_size=2048):
                if not chunk: break
                wj.seek(offset)
                wj.write(chunk)
                offset = offset + len(chunk)
        if self.tr_no=="False":
            os.system('ffmpeg.exe -i video.mp4 -i audio.m4a -vcodec copy -acodec copy %s.mp4'%(self.title.replace("&","AND").replace("|","OR")))
            if self.tr_del=="False":
                os.system('del video.mp4 audio.m4a')
        else:
            if self.tr_no=="False":
                os.system('ffmpeg -i video.flv %s.mp4'%(self.title.replace("&","AND").replace("|","OR")))
                if self.tr_del=="False":
                    os.system('del video.flv')