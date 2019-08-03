# Recomenda EASY

## Rodando Localmente
- Precisa de Python 3.7 [installed locally](http://install.python-guide.org).
- Banco de dados [MongoDb](https://docs.mongodb.com/manual/installation/).
- Heroku CLI para rodar local e deploy [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

```sh
# Clone the repository
$ git clone TODO
$ cd recomenda_easy

# Copy the sample env
$ cp sample.env .env

# Create a Python virtual environment
$ python -m venv venv
$ source venv/bin/activate

# Install dependecies
$ pip3 install -r requirements.txt

$ flask run
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master
$ heroku open
```
ou

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Documentation
 TODO
