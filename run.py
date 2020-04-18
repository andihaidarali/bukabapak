from flask import Flask, render_template, request, send_file
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Regexp
import bklpk

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'simpleflaskweb'


class InputToko(FlaskForm):
    name = StringField('Name:', validators=[InputRequired(), Regexp(r'^[\w.+-]+$')])


@app.route("/", methods=['GET', 'POST'])
def index():
    title = "Bukalapak Scraper"
    data = "Input Merchant Username"
    form = InputToko(request.form)

    if form.validate_on_submit():
        name = form.name.data
        id = bklpk.get_data(name).id
        if id != 0:
            data = bklpk.get_data(name).scrape()
            download = "<a href=' /download' target='_blank' class='btn btn-success'>Download CSV</a>"
            return render_template('res.html', title=title, form=form, data=data, download=download)
        else:
            data = "Merchant Not Found"
            return render_template('base_template.html', title=title, form=form, data=data)
    else:
        return render_template('base_template.html', title=title, form=form, data=data)

@app.route('/download')
def download():
    path = 'result.csv'
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
