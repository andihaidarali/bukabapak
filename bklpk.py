import requests
from bs4 import BeautifulSoup
import json
import csv

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) '
      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '
      'Safari/537.36')
head = {'User-Agent': UA}

class get_token():
    """
    Melakukan Request Ke Halaman Home Bukalapak
    Untuk Mendapatkan Token.
    """
    def __init__(self):
        try:
            root = requests.get('https://www.bukalapak.com', headers=head)
            soup = BeautifulSoup(root.text, 'html.parser')
            get_token = soup.find('meta', attrs={'name': 'oauth-access-token'})
            self.token = get_token['content']
        except:
            print("Token Tidak Ditemukan")

    def __str__(self):
        return self.token

class get_data():
    """
    Melakukan Request Ke Halaman Mobile Toko Untuk Mendapatkan ID Toko
    Melakukan Request Untuk Mendapatkan Total Data
    Melakukan Scraping Untuk Mendapatkan Seluruh Data
    note : request langsung ke halaman root web toko akan dialihkan ke 403
    """
    def __init__(self, nama_toko):
        self.nama_toko = nama_toko

        try:
            profile = ('https://m.bukalapak.com/u/{}?keywords=&price_range='
                       '&sort=bestselling&deal=&condition=&rating=&installment='
                       '&free_shipping_provinces=&wholesale=&page=1'.format(self.nama_toko))
            params_prof = {'page': 1, 'sort': 'bestselling'}
            get_profile = requests.get(url=profile, headers=head, params=params_prof)
            parsing_profile = BeautifulSoup(get_profile.text, 'html.parser')
            json_data = json.loads(parsing_profile.find_all('merchant-page-app')[0]['seller-data'])
            self.id = json_data['seller']['id']

        except:
            try:
                profile = ('https://m.bukalapak.com/{}?keywords=&price_range='
                           '&sort=bestselling&deal=&condition=&rating=&installment='
                           '&free_shipping_provinces=&wholesale=&page=1'.format(self.nama_toko))
                params_prof = {'page': 1, 'sort': 'bestselling'}
                get_profile = requests.get(url=profile, headers=head, params=params_prof)
                parsing_profile = BeautifulSoup(get_profile.text, 'html.parser')
                json_data = json.loads(parsing_profile.find("official-store-app")['id'])
                self.id = json_data

            except TypeError:
                self.id = 0

    def get_total(self):
        id_store = self.id
        token = get_token()
        try:
            src_total = requests.get('https://api.bukalapak.com/stores/{}/products?'
                                     'offset=0&limit=16&sort=bestselling&access_token={}'.format(id_store, token))
            json_src = src_total.json()
            data_src = json_src['meta']
            self.total = data_src['total']

            return self.total
        except:
            self.total = 0
            return self.total

    def scrape(self):
        id = self.id
        token = get_token()
        total = self.get_total()
        page = 0
        limit = 16
        offset = limit - 16
        y = total / limit
        if type(y) is float:
            page = int(y) + 1
        pages = 0
        self.export = []
        while pages < page:
            src = requests.get('https://api.bukalapak.com/stores/{}/products?'
                               'offset={}&limit={}&sort=bestselling'
                               '&access_token={}'.format(id, offset, limit, token))
            json_data = src.json()
            data = json_data['data']
            for d in data:
                if len(d['rating']) != 0:
                    self.export.append(
                        dict(name=d["name"], harga=d["price"], url=d["url"],
                             gambar=d["images"]["large_urls"], terjual=d["stats"]["sold_count"],
                             stok=d["stock"], rating=d['rating']['average_rate'],
                             desk=BeautifulSoup(d["description"], 'html.parser').text)
                    )
                else:
                    self.export.append(
                        dict(name=d["name"], harga=d["price"], url=d["url"],
                             gambar=d["images"]["large_urls"], terjual=d["stats"]["sold_count"],
                             stok=d["stock"], rating="None",
                             desk=BeautifulSoup(d["description"], 'html.parser').text)
                    )
            pages += 1
            offset += limit

            if id != 0:
                keys = self.export[0].keys()
                with open('result.csv', 'w') as output_file:
                    dict_writer = csv.DictWriter(output_file, keys)
                    dict_writer.writeheader()
                    dict_writer.writerows(self.export)

        return self.export