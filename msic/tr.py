#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
from PyQt5.QtCore import QStringListModel,QThread,pyqtSignal
import requests

class tr(QThread):
    def __init__(self,title,stats,tr_no="False",tr_del="False",video_q=1):
        super().__init__()
        self.stats=stats
        self.title=title
        self.tr_no=tr_no
        self.tr_del=tr_del
        self.video_q=video_q
        self.stats_vedio_q=["高清1080P", "高清720P", "清晰480P", "流畅360P"]

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
            wj.close()
        if self.stats==1:
            if self.tr_no=="False":
                print(self.video_q)
                os.system("ffmpeg.exe -i zRain/"+'"'+self.title+'"'+"/video.mp4 -i zRain/"+'"'+self.title+'"'+"/audio.m4a -vcodec copy -acodec copy zRain/"+'"'+self.title+'"'+"/"+self.stats_vedio_q[int(self.video_q)-1]+".mp4")
                if self.tr_del=="False":
                    os.system("cd zRain/"+'"'+self.title+'"'+" & del video.mp4 audio.m4a")
        else:
            if self.tr_no=="False":
                os.system("ffmpeg -i zRain/"+'"'+self.title+'"'+"/video.flv zRain/"+'"'+self.title+'"'+"/"+self.stats_vedio_q[int(self.video_q)-1]+".mp4")
                if self.tr_del=="False":
                    os.system("cd zRain/"+'"'+self.title+'"'+" & del video.flv")
