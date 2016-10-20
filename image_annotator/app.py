import logging.config

from flask import Flask, Blueprint

from image_annotator import settings
from image_annotator.api.endpoints.image import ns as image_namespace
from image_annotator.api.endpoints.auth import ns as auth_namespace
from image_annotator.api.restplus import api

logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config[
        'SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(image_namespace)
    api.add_namespace(auth_namespace)
    flask_app.register_blueprint(blueprint)


def main():
    app = Flask(__name__)
    initialize_app(app)
    log.info(
        '>>>>> Starting development server at http://{}/api/ <<<<<'.format(
            app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)


if __name__ == '__main__':
    main()
