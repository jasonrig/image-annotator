from flask_restplus import Resource

from image_annotator.api.restplus import api
from image_annotator.authorisation import authorized_gtoken, sign_token

ns = api.namespace('authorize',
                   description='Convert a Google token to a local one')


@ns.route('/')
class Authorize(Resource):

    @authorized_gtoken
    def get(self, userid):
        return {'token': sign_token(userid)}
