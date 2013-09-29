from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .user import *
from .competition import *
from .fitbit import *
from .forum import *