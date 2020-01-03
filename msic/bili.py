#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
from PyQt5.QtCore import QStringListModel,QThread,pyqtSignal
from msic.tr import tr
from msic.get_data import get_data
import os

class down(QThread):
	data_=pyqtSignal(int,int)
	def __init__(self,id,tr_no="False",tr_del="False",which_="True",video_q=1):
		super().__init__()
		self.headers = {
			"Referer": "https://www.bilibili.com",
			"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
			"Cookie": "CURRENT_FNVAL=16"
		}
		self.tr_no=tr_no
		self.tr_del=tr_del
		self.video_q=int(video_q)
		self.head_js=get_data(id,which_)
		self.count=0
		#尝试不同视频获取视频连接
		try:
			#这里没有用api获取cid，我用返回数据提取出了cid
			data=self.head_js[0][int(self.head_js[1])].text.replace("window.__INITIAL_STATE__=","").replace(";(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1]).parentNode.removeChild(s);}());","")
			link=json.loads(data)
			self.Title=link["videoData"]["title"]
			self.urll="https://api.bilibili.com/x/player/playurl?cid=%s&avid=%s&qn=16"%(link["videoData"]["cid"],id)
			r = requests.get(self.urll,headers=self.headers)
			self.link2=[json.loads(r.text)["data"]["durl"][0]["url"]]

		except:
			data=self.head_js[0][int(self.head_js[1])].text.replace("window.__playinfo__=","")
			link=json.loads(data)["data"]
			if not "durl" in link.keys():
				for i in range(0,4):
					try:
						self.link2=[link["dash"]["video"][self.video_q-1-i]["baseUrl"],link["dash"]["audio"][self.video_q-1-i]["baseUrl"]]
						break
					except:
						self.count+=1
			else:
				self.link2=[link["durl"][0]["url"]]
			#标题
			self.Title=self.head_js[2]


			
	def run(self):
		folder = os.path.exists(os.path.abspath("")+"\\zRain\\"+self.Title)
		if not folder:
			os.makedirs(os.path.abspath("")+"\\zRain\\"+self.Title)
		for i in range(0,len(self.link2)):
			r2=requests.get(self.link2[i],headers=self.headers,stream=True)
			size=int(r2.headers["Content-Length"])
			if  i==0:
				if len(self.link2)==1:
					wj=open("zRain/%s/video.flv"%self.Title,"wb")
					stats=2
					stats_now=0
				else:
					wj=open("zRain/%s/video.mp4"%self.Title,"wb")
					stats=1
					stats_now=1
			else:
				wj=open("zRain/%s/audio.m4a"%self.Title,"wb")
				stats_now=2
			offset = 0
			for chunk in r2.iter_content(chunk_size=20):
				if not chunk: break
				wj.seek(offset)
				wj.write(chunk)                            
				offset = offset + len(chunk)
				proess = offset / int(size) * 100
				self.data_.emit(int(proess),stats_now)
			wj.close()
		self.mit=tr(self.Title,stats,self.tr_no,self.tr_del,self.video_q-self.count)
		self.mit.start()
