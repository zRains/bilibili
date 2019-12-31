import requests
from bs4 import BeautifulSoup
import json
from PyQt5.QtCore import QStringListModel,QThread,pyqtSignal

class down(QThread):
	data_=pyqtSignal(int)
	def __init__(self,id):
		super().__init__()
		url_ = "https://www.bilibili.com/video/av%s?from=search&seid=11892641008249561747"%id
		self.headers = {
			"Referer": "https://www.bilibili.com",
			"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
		}
		r = requests.get(url_,headers=self.headers)
		head_js=BeautifulSoup(r.text,"lxml").find_all("script")
		try:
			#这里没有用api获取cid，我用返回数据提取出了cid
			data=head_js[2].text.replace("window.__INITIAL_STATE__=","").replace(";(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1]).parentNode.removeChild(s);}());","")
			link=json.loads(data)
			self.Title=link["videoData"]["title"]
			self.urll="https://api.bilibili.com/x/player/playurl?cid=%s&avid=%s&qn=16"%(link["videoData"]["cid"],id)
			r = requests.get(self.urll,headers=self.headers)
			self.urll=json.loads(r.text)["data"]["durl"][0]["url"]
		except:
			data=head_js[2].text.replace("window.__playinfo__=","")
			link=json.loads(data)["data"]
			if not "durl" in link.keys():
				self.urll=link["dash"]["video"][0]["baseUrl"]
			else:
				self.urll=link["durl"][0]["url"]
			head_title=BeautifulSoup(r.text,"lxml").find_all("title")
			self.Title=head_title[0].text.replace("_哔哩哔哩 (゜-゜)つロ 干杯~-bilibili","")
	def run(self):
		r2=requests.get(self.urll,headers=self.headers,stream=True)
		size=int(r2.headers["Content-Length"])
		wj=open("%s.flv"%self.Title,"wb")
		offset = 0
		for chunk in r2.iter_content(chunk_size=2048):
			if not chunk: break
			wj.seek(offset)
			wj.write(chunk)                            
			offset = offset + len(chunk)
			proess = offset / int(size) * 100
			self.data_.emit(int(proess))

