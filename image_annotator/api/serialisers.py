from flask_restplus import fields

from image_annotator.api.restplus import api

annotation = api.model('Image annotation', {
    'x_offset': fields.Float(required=True,
                             description='Bounding box x-offset'),
    'y_offset': fields.Float(required=True,
                             description='Bounding box y-offset'),
    'height': fields.Float(required=True,
                           description='Height of bounding box'),
    'width': fields.Float(required=True, description='Width of bounding box')
})

image = api.model('Image', {
    'path': fields.String(required=True, description='Path to the image file'),
    'mimetype': fields.String(required=False, description='The image mimetype', default="image/png")
})