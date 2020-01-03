#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def get_data(id,which_,stats=1):
	str_t="_哔哩哔哩 (゜-゜)つロ 干杯~-bilibili"
	headers = {
			"Referer": "https://www.bilibili.com",
			"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
			"Cookie": "CURRENT_FNVAL=16"
		}
	if which_=="True":
		url_ = "https://www.bilibili.com/video/av%s?from=search&seid=11892641008249561747"%id
		r = requests.get(url_,headers=headers)
		demo=2
		if stats==1:
			return [BeautifulSoup(r.text,"lxml").find_all("script"),demo,BeautifulSoup(r.text,"lxml").find_all("title")[0].text.replace(str_t,"")]
		else:
			return [BeautifulSoup(r.text,"lxml").find_all("meta",itemprop="image")[0]["content"],BeautifulSoup(r.text,"lxml").find_all("title")[0].text.replace(str_t,"")]
	else:
		url_ = "https://www.bilibili.com/bangumi/play/ep%s"%id
		r = requests.get(url_,headers=headers)
		demo=5
		if stats==1:
			return [BeautifulSoup(r.text,"lxml").find_all("script"),demo,BeautifulSoup(r.text,"lxml").find_all("title")[0].text.replace(str_t,"")]
		else:
			return [BeautifulSoup(r.text,"lxml").find_all("meta",property="og:image")[0]["content"],BeautifulSoup(r.text,"lxml").find_all("title")[0].text.replace(str_t,"")]
