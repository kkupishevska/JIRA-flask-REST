# Flask example

Using Flask to build a Restful API Server with Swagger document.

Integration with Flask-restplus, Flask-Cors, Flask-Testing, Flask-SQLalchemy,and Flask-OAuth extensions.

### Extension:
- Restful: [Flask-restplus](http://flask-restplus.readthedocs.io/en/stable/)

- SQL ORM: [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)

- Testing: [Flask-Testing](http://flask.pocoo.org/docs/0.12/testing/)

- OAuth: [Flask-OAuth](https://pythonhosted.org/Flask-OAuth/)

- ESDAO: [elasticsearch](https://elasticsearch-py.readthedocs.io/en/master/) , [elasticsearch-dsl](http://elasticsearch-dsl.readthedocs.io/en/latest/index.html)


## Installation

Install with pip:

```
$ python3.10 -m venv .venv
```

```
$ source .venv/bin/activate
```

```
$ pip install -r requirements.txt
```

```
$ flask run
```

## After Adding New Package

```
$ python -m pip freeze > requirements.txt
```

## Database Migration
```
$ flask db migrate
```

```
$ flask db upgrade
```

## Flask Configuration

#### Example

```
app = Flask(__name__)
app.config['DEBUG'] = True
```
### Configuring From Files

#### Example Usage

```
app = Flask(__name__ )
app.config.from_pyfile('config.Development.cfg')
```
 
## Run Flask
### Run flask for develop

Swagger document page:  `http://127.0.0.1:5000/swagger-ui`


### Run with Docker

```
$ docker build -t flask-example .

$ docker run -p 5000:5000 --name flask-example flask-example 
 
```

In image building, the webapp folder will also add into the image


## Reference

Offical Website

- [Flask](http://flask.pocoo.org/)
- [Flask Extension](http://flask.pocoo.org/extensions/)
- [Flask restplus](http://flask-restplus.readthedocs.io/en/stable/)
- [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
- [Flask-OAuth](https://pythonhosted.org/Flask-OAuth/)
- [elasticsearch-dsl](http://elasticsearch-dsl.readthedocs.io/en/latest/index.html)
- [gunicorn](http://gunicorn.org/)

Tutorial

- [Flask Overview](https://www.slideshare.net/maxcnunes1/flask-python-16299282)
- [In Flask we trust](http://igordavydenko.com/talks/ua-pycon-2012.pdf)

[Wiki Page](https://github.com/tsungtwu/flask-example/wiki)



## Changelog

- Version 2.3 : add dockerfile
- Version 2.2 : add ESDAO module
- Version 2.1 : add OAuth extension: FLASK-OAuth, and google oauth example
- Version 2.0 : add SQL ORM extension: FLASK-SQLAlchemy
- Version 1.1 : update nosetest
- Version 1.0 : basic flask-example with Flask-Restplus, Flask-Tesintg
