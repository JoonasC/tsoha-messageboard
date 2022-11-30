from os import getenv

from app import app

app.secret_key = getenv("SECRET_KEY")
