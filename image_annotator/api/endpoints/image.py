import os.path

from flask import request
from flask_restplus import Resource
from flask import send_file, abort

from image_annotator.api.restplus import api
from image_annotator.api.serialisers import annotation, image
from image_annotator.authorisation import authorized, authorized_admin
from image_annotator.database.mongo import Database

ns = api.namespace('images', description='Fetch and annotate images')

db = Database()


@ns.route('/get_one')
class FetchImage(Resource):

    @authorized
    def get(self, userid):
        return db.get_random_unannotated_image(userid, 5)

@ns.route('/raw/<string:id>')
class FetchRawImage(Resource):

    @authorized
    def get(self, userid, id):
        image = db.get_image(id)
        try:
            return send_file(image['path'], mimetype=image['mimetype'])
        except FileNotFoundError:
            abort(404)


@ns.route('/annotate/<string:id>/')
class AnnotateImage(Resource):

    @api.expect(annotation)
    @authorized
    def post(self, id, userid):
        req_data = request.json
        result = db.add_bounding_box_annotation(id, userid, req_data['x_offset'], req_data['y_offset'], req_data['height'], req_data['width'])
        return {'records_updated': result}


@ns.route('/add')
class AddImage(Resource):

    @api.expect(image)
    @authorized_admin
    def post(self, userid):
        req_data = request.json
        if os.path.isfile(req_data['path']):
            return {'id': db.insert_image(req_data['path'], req_data['mimetype'])}
        else:
            abort(500)