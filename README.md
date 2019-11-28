# Eventex [![Build Status](https://travis-ci.org/theusindabike/wttd.svg?branch=master)](https://travis-ci.org/theusindabike/wttd)
- Python 3.8.0

## Install
```console
git clone git@github.com:theusindabike/wttd.git wttd
cd wttd
python -m venv .wttd
source .wttd/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test 
```

## Deploy

```console
heroku create newinstance
heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroku confit:set DEBUG=False
#config email
git push heroku master
```
