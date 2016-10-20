import os
import sys
from datetime import timedelta

FLASK_SERVER_NAME = 'localhost:8888'
FLASK_DEBUG = False

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# MongoDB settings
MONGO_URL = 'mongodb://localhost:27017/'
MONGO_DB_NAME = 'image-annotator'

# Auth options
RESTRICT_ACCESS_BY_DOMAIN = ''
JWT_SECRET = 'eeraid8Ahch7revu8eeweiKoh2tua9eeyae9aigeu8thah1oy5'
JWT_EXPIRY = 24*60*60 # Seconds
ADMIN_USER = 'test@example.com'

# Override settings from environment if specified
for name, val in list(sys.modules[__name__].__dict__.items()):
    if name == name.upper() and name[0] is not '_':
        env = os.environ.get(name, val)
        if isinstance(val, int):
            if isinstance(env, str):
                env = env.lower() in ['1', 'true', 't']
            setattr(sys.modules[__name__], name, int(env))
        elif isinstance(val, float):
            setattr(sys.modules[__name__], name, float(env))
        else:
            setattr(sys.modules[__name__], name, env)