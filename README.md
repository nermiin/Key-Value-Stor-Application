## Dependencies:

* Python > 3.6
* Flask
* Redis


## To run the Docker Compose

```
sudo docker-compose build
sudo docker-compose up
```

## To install dependencies run:

```
pip3 install flask
pip3 install redis
```


## To run the tests run:

```
python3 app_tests.py
```

## To run the application:

```
cd key-value-store-application/
export FLASK_APP=app.py
flask run
```
