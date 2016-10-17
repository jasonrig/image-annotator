from flask import request
from flask_restplus import Resource

from image_annotator.api.restplus import api
from image_annotator.api.serialisers import annotation
from image_annotator.authorisation import authorized

ns = api.namespace('images', description='Fetch and annotate images')


@ns.route('/get_one')
class FetchImage(Resource):

    @authorized
    def get(self, userid):
        return {'an': 'image', 'for': userid}


@ns.route('/annotate/<int:id>/')
class AnnotateImage(Resource):

    @authorized
    @api.expect(annotation)
    def post(self, id, userid):

        return {'message': 'ok'}