# spacedb

To get started:

```
virtualenv venv
source venv/bin/activate
```

First time:

```
# Python backend
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata orbit_class

# Webpack frontend
yarn install
```

Now run it:

```
# Terminal 1: run the web server
./manage.py runserver

# Terminal 2: build the js assets continuously
yarn build:watch
```
