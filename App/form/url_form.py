from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, URL
from App.model import Urls
from sqlalchemy import func
from shortuuid import ShortUUID
from random import randint
from urllib.parse import urlparse

class UrlForm(FlaskForm):
    class Meta:
        csrf = False
        
    url = StringField(
        "Enter a Url",
        description="Enter a Url to shorten",
        validators=[
            DataRequired('Url is required'),
            Length(min=3, max=40),
            URL(message='Please enter a valid URL')
        ],
        render_kw={'type': 'url'}
    )

    submit = SubmitField("Shorten Url")

    def validate(self):
        if super(UrlForm, self).validate():
            url_ = self.url.data.lower()
            self.url.data = self.url.data.lower()
            long = urlparse(self.url.data.replace('www.', '')).netloc
            curl = Urls.query.filter(func.lower(Urls.long) == long).first()
            if curl:
                self.url.data = curl.short
            else:
                # add to database
                short = ShortUUID().random(length=randint(3, 6))
                data = Urls()
                data.create(long=long, short=short, url=self.url.data)
                data.save()
                data.add_count()
                self.url.data = short
            return True
            
        else:
            return False