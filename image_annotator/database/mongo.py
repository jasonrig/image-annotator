from bson import ObjectId
from pymongo import MongoClient

from image_annotator import settings


class Database:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URL)
        self.db = self.client[settings.MONGO_DB_NAME]
        self.image_collection = self.db['image-collection']

    def insert_image(self, path, mimetype="image/png"):
        result = self.image_collection.insert_one(
            {
                'path': path,
                'mimetype': mimetype,
                'annotations': []
            }
        )
        return str(result.inserted_id)

    def get_random_unannotated_image(self, user_id, prefetch=1):
        return serializable_mongo_result(self.image_collection.aggregate([
            {
                '$match': {
                    'annotations': {
                        '$not': {
                            '$elemMatch': {
                                'user_id': user_id
                            }
                        }
                    }
                }
            },
            {
                '$sample': {
                    'size': prefetch
                }
            }
        ]))

    def get_image(self, image_id):
        return serializable_mongo_result(self.image_collection.find_one({'_id': ObjectId(image_id)}))

    def add_bounding_box_annotation(self, image_id, user_id, x_offset,
                                    y_offset, height, width):
        result = self.image_collection.update_one(
            {'_id': ObjectId(image_id)},
            {
                '$addToSet': {
                    'annotations': {
                        'user_id': user_id,
                        'x_offset': x_offset,
                        'y_offset': y_offset,
                        'height': height,
                        'width': width,
                        'type': 'box'
                    }
                }
            }
        )

        return result.modified_count


def serializable_mongo_result(result):

    if isinstance(result, dict):
        dict_copy = dict(result)
        if '_id' in dict_copy:
            dict_copy['id'] = str(dict_copy['_id'])
            del dict_copy['_id']
        return dict_copy

    serializable_result = []
    for item in result:
        serializable_result.append(serializable_mongo_result(item))

    return serializable_result