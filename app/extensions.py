from authlib.integrations.flask_client import OAuth
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy
from flask_caching import Cache


from flask_pymongo import PyMongo
import mongomock

class MockPyMongo(PyMongo):
    def init_app(self, app, uri=None, *args, **kwargs):
        super().init_app(app, uri, *args, **kwargs)
        self.cx = mongomock.MongoClient()
        uri = uri or app.config.get("MONGO_URI")
        db_name = uri.split("/")[-1].split("?")[0] if uri else "450_dsa"
        self.db = self.cx[db_name]

mongo = MockPyMongo()
db = LocalProxy(lambda: mongo.db)
bcrypt = Bcrypt()
login_manager = LoginManager()
oauth = OAuth()
limiter = Limiter(key_func=get_remote_address, default_limits=[], headers_enabled=True)
github = LocalProxy(lambda: oauth.create_client("github"))
google = LocalProxy(lambda: oauth.create_client("google"))
cache = Cache()
