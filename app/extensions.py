from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Shared Flask extensions.
# These are imported by models and initialized in app/__init__.py.
db = SQLAlchemy()
migrate = Migrate()
