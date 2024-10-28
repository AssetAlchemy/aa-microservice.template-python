# AssetAlchemy - Microservice img template for python
This is a template repo for all img microservices based on python that will use the app "AssetAlchemy"

## Install dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # if it is necessary
```

## Starting app
```bash
fastapi run app/main.py
```
### Notes:
* The message of `Serving at: http://0.0.0.0:8000` & `API docs: http://0.0.0.0:8000/docs` are not true if you want to see the app from outside the docker container. To see thoose endpoints from your host device you will need to replace the `http://0.0.0.0:8000` for `http://localhost:${PORT from .env}`

In conclusion, if you want to see the app go to: `localhost:${PORT}`

### Example:

This is our .env file  
```bash
# .env
PORT=4000
```
As we have a PORT setted on 4000 we can enter on the next URLs
* http://localhost:4000
* http://localhost:4000/docs



## Update dependencies in requeriments.txt
```bash
pip freeze > requirements.txt
pip freeze > requirements-dev.txt  # if it is necessary
```