import requests
from bs4 import BeautifulSoup
import json

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 "
      "Safari/537.36")
head = {'User-Agent': UA}

# get tokens from homepage
root = requests.get('https://www.bukalapak.com', headers=head)
get_smtg = BeautifulSoup(root.text, 'html.parser')
get_token = get_smtg.find('meta', attrs={'name': 'oauth-access-token'})
token = get_token['content']

# get id toko from mobile profile pages
nama_toko = name
profile = ('https://m.bukalapak.com/u/{}?keywords=&price_range='
       '&sort=bestselling&deal=&condition=&rating=&installment='
       '&free_shipping_provinces=&wholesale=&page=1'.format(nama_toko))
params_prof = {'page':1,'sort':'bestselling'}
get_profile = requests.get(url=profile, headers=head, params=params_prof)
parsing_profile = BeautifulSoup(get_profile.text, 'html.parser')
json_data = json.loads(parsing_profile.find_all('merchant-page-app')[0]['seller-data'])
toko_id = json_data['seller']['id']
id_store = toko_id

# get total barang
src_total = requests.get('https://api.bukalapak.com/stores/{}/products?'
                       'offset=0&limit=16&sort=bestselling&access_token={}'.format(id_store, token))
json_src = src_total.json()
data_src = json_src['meta']
total = data_src['total']

limit = 16
offset = limit - 16
page = 0

y = total/limit
if type(y) is float:
  page = int(y) + 1

pages = 0
self.export = []

while pages < page:
    src = requests.get('https://api.bukalapak.com/stores/{}/products?'
                       'offset={}&limit={}&sort=bestselling&access_token={}'.format(id_store, offset, limit, token))
    json_data = src.json()
    data = json_data['data']
    for d in data:
        self.export.append({"name":d["name"],
                            "harga":d["price"],
                            "url": d["url"],
                            "gambar": d["images"]["large_urls"][0],
                            "rating": "rating : {} dari {} user".format(d["rating"]["average_rate"], d["rating"][
                                "user_count"]),
                            "terjual": d["stats"]["sold_count"],
                            "desk": BeautifulSoup(d["description"], 'html.parser').text
                            })
    pages += 1
    offset += limit