from flask import Flask
from .models import db
from config import DevelopmentConfig

app = Flask(__name__)

app.config.from_object(DevelopmentConfig())

db.init_app(app)

from app import views