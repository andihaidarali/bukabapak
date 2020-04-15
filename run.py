import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, flash, request
from wtforms import Form, validators, StringField
import bklpk

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class InputToko(Form):
    name = StringField('Name:', validators=[validators.DataRequired(), validators.Regexp(r'^[\w.+-]+$')])

    @app.route("/", methods=['GET', 'POST'])
    def index():
        global name
        title = "Bukalapak Scraper"
        inputnya = "Input Nama Toko dalam url bukapak.com/u/<strong>{nama_toko}</strong> | paste hanya nama toko"
        export = []
        form = InputToko(request.form)
        print(form.errors)
        token = bklpk.get_token()
        if request.method == 'POST':
            if form.validate():
                name = request.form['name']
                id_store = bklpk.get_id(name).id
                if id_store != 0:
                    total = bklpk.get_id(name).get_total()
                    limit = int(16)
                    offset = limit - 16
                    y = total / limit
                    page = 0
                    if type(y) is float:
                        page = int(y) + 1
                    pages = 0
                    while pages < page:
                        src = requests.get('https://api.bukalapak.com/stores/{}/products?'
                                           'offset={}&limit={}&sort=bestselling'
                                           '&access_token={}'.format(id_store, offset, limit, token))
                        json_data = src.json()
                        data = json_data['data']
                        for d in data:
                            if len(d['rating']) != 0:
                                export.append(
                                    dict(name=d["name"], harga=d["price"], url=d["url"],deskripsi=d["description"],
                                         gambar=d["images"]["large_urls"], terjual=d["stats"]["sold_count"],
                                         rating=d['rating']['average_rate'],
                                         desk=BeautifulSoup(d["description"], 'html.parser').text)
                                )
                            else:
                                export.append(
                                    dict(name=d["name"], harga=d["price"], url=d["url"],deskripsi=d["description"],
                                         gambar=d["images"]["large_urls"], terjual=d["stats"]["sold_count"],
                                         rating="None",
                                         desk=BeautifulSoup(d["description"], 'html.parser').text)
                                )
                        pages += 1
                        offset += limit
                else:
                    flash("ID Toko Tidak Ditemukan")
        else:
            flash(inputnya)
        return render_template('index.html', title=title, form=form, data=export)
        # TODO : Buat Halaman Lain Untuk Scraping Hasil Pencarian


if __name__ == '__main__':
    app.run(debug=True)
