#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
from PyQt5.QtCore import QStringListModel,QThread,pyqtSignal
from tr import tr

class down(QThread):
	data_=pyqtSignal(int,int)
	def __init__(self,id,tr_no="False",tr_del="False",which_="True"):
		super().__init__()
		self.tr_no=tr_no
		self.tr_del=tr_del
		if which_=="True":
			url_ = "https://www.bilibili.com/video/av%s?from=search&seid=11892641008249561747"%id
			self.demo=2
		else:
			url_ = "https://www.bilibili.com/bangumi/play/ep%s"%id
			self.demo=5
		self.headers = {
			"Referer": "https://www.bilibili.com",
			"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
			"Cookie": "CURRENT_FNVAL=16"
		}
		r = requests.get(url_,headers=self.headers)
		head_js=BeautifulSoup(r.text,"lxml").find_all("script")
		try:
			#这里没有用api获取cid，我用返回数据提取出了cid
			data=head_js[self.demo].text.replace("window.__INITIAL_STATE__=","").replace(";(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1]).parentNode.removeChild(s);}());","")
			link=json.loads(data)
			self.Title=link["videoData"]["title"]
			self.urll="https://api.bilibili.com/x/player/playurl?cid=%s&avid=%s&qn=16"%(link["videoData"]["cid"],id)
			r = requests.get(self.urll,headers=self.headers)
			self.link2=[json.loads(r.text)["data"]["durl"][0]["url"]]
		except:
			data=head_js[self.demo].text.replace("window.__playinfo__=","")
			link=json.loads(data)["data"]
			if not "durl" in link.keys():
				self.link2=[link["dash"]["video"][0]["baseUrl"],link["dash"]["audio"][0]["baseUrl"]]
			else:
				self.link2=[link["durl"][0]["url"]]
			head_title=BeautifulSoup(r.text,"lxml").find_all("title")
			#标题
			self.Title=head_title[0].text.replace("_哔哩哔哩 (゜-゜)つロ 干杯~-bilibili","")
	def run(self):
		for i in range(0,len(self.link2)):
			r2=requests.get(self.link2[i],headers=self.headers,stream=True)
			size=int(r2.headers["Content-Length"])
			if  i==0:
				if len(self.link2)==1:
					wj=open("%s.%s"%("video","flv"),"wb")
					stats=2
					stats_now=0
				else:
					wj=open("%s.%s"%("video","mp4"),"wb")
					stats=1
					stats_now=1
			else:
				wj=open("%s.%s"%("audio","m4a"),"wb")
				stats_now=2
			offset = 0
			for chunk in r2.iter_content(chunk_size=2048):
				if not chunk: break
				wj.seek(offset)
				wj.write(chunk)                            
				offset = offset + len(chunk)
				proess = offset / int(size) * 100
				self.data_.emit(int(proess),stats_now)
		self.mit=tr(self.Title,stats,self.tr_no,self.tr_del)
		self.mit.start() 
