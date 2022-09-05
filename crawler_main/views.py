from django.shortcuts import render
from .models import Results
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
import re
import requests
from bs4 import BeautifulSoup
from time import sleep
import urllib.parse
import base64
from PIL import Image
from io import BytesIO
import urllib.request
# Create your views here.
class AboutView(TemplateView):
  template_name = 'about.html'


class HomeView(CreateView):
  template_name = 'home.html'
  model = Results
  fields = ('keywords', 'min_price', 'max_price','product_num',)
  success_url = reverse_lazy('result')

def getGraph(url):
	f = BytesIO(requests.get(url).content)
	img = Image.open(f)	
	img.resize((64, 64))
	buffer = BytesIO() # メモリ上への仮保管先を生成
	img.save(buffer, format="PNG") 
	base64Img = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
	return base64Img

def crawl(request):
	for inputs in Results.objects.all():
		keywords = inputs.keywords
		min_price = int(inputs.min_price)
		max_price = int(inputs.max_price)
		product_num = int(inputs.product_num)

	HEADERS = ({'User-Agent':
						'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
						'Accept-Language': 'en-US, en;q=0.5'})
	products = []
	url = 'https://www.amazon.co.jp/s?k='
	for keyword in keywords.split(' '):
		url += (urllib.parse.quote(keyword) + '+')

	for page in range(1, 9):
		url += f'&page={page}'
		doc = BeautifulSoup(requests.get(
        url, headers=HEADERS).content, 'html.parser')
		for product in doc.select('.s-card-container .a-section.a-spacing-base'):
			image_url = product.select_one('.s-image').get('src')
			title = product.select_one('span.a-text-normal').text
			price = product.select('span.a-price-whole')
			product_url = 'https://www.amazon.co.jp' + product.select_one('.s-product-image-container .a-link-normal').get('href')
			#価格存在確認
			if len(price) == 0:
				continue
			else:
				price = int(re.sub(r'\D', '', price[0].text))
				#価格が範囲外ならスキップ
				if price < min_price or max_price < price:
					continue
			products.append([product_url, title, getGraph(image_url), price])
			if len(products) >= product_num:
				break
		if len(products) >= product_num:
			break
		sleep(1)
	ctxt = {
		'products': products, 
		'keyword': keywords,
		'min': min_price,
		'max': max_price
	}
	return render(request, 'result.html', ctxt)