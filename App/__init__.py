from flask import Flask, jsonify, request, url_for, redirect
from App.model import db, HitCount, UrlCount, Urls
from App.decorator import hits, get_counts
from App.form import UrlForm

from click import command
from flask.cli import with_appcontext

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@command()
@with_appcontext
def set_defaults():
    if not HitCount.query.first():
        HitCount().save()
    if not UrlCount.query.first():
        UrlCount().save()

    

@app.route('/', methods=['GET'])
@hits
@get_counts
def init(hit_count, url_count):
    return 'hello'

@app.route('/<short>')
@hits
@get_counts
def shorts(hit_count, url_count, short):
    url = Urls.query.filter_by(short=short).first()
    return redirect(url.url)

@app.route('/shorten-url', methods=['POST'])
@hits
def shorten():
    if request.form:
        form = UrlForm(form=request.form)
        if form.validate_on_submit():
            return jsonify(
                data = url_for('shorts', short=form.url.data, _external=True),
                msg = 'Url shortened successfully.'
            )
        return jsonify(
            msg = 'Validation error',
            error = form.errors
        )
    else:
        return jsonify(
            msg = 'Missing Field',
            error = 'The Url field is not provided'
        )

app.cli.add_command(set_defaults)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
