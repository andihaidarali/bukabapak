import requests
from bs4 import BeautifulSoup
import json

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
            get_smtg = BeautifulSoup(root.text, 'html.parser')
            get_token = get_smtg.find('meta', attrs={'name': 'oauth-access-token'})
            self.token = get_token['content']
        except:
            print("Token Tidak Ditemukan")

    def __str__(self):
        return self.token

class get_id():
    """
    Melakukan Request Ke Halaman Mobile Toko Untuk Mendapatkan ID Toko
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
            profile = ('https://m.bukalapak.com/{}?keywords=&price_range='
                       '&sort=bestselling&deal=&condition=&rating=&installment='
                       '&free_shipping_provinces=&wholesale=&page=1'.format(self.nama_toko))
            params_prof = {'page': 1, 'sort': 'bestselling'}
            get_profile = requests.get(url=profile, headers=head, params=params_prof)
            parsing_profile = BeautifulSoup(get_profile.text, 'html.parser')
            json_data = json.loads(parsing_profile.find("official-store-app")['id'])
            self.id = json_data

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