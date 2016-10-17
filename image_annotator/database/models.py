from image_annotator.database import db


class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    local_path = db.Column(db.String(255))
    annotations = db.relationship('ImageAnnotation', back_populates='image')


class ImageAnnotation(db.Model):
    __tablename__ = 'image_annotation'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Integer, db.ForeignKey('image.id'))
    user_id = db.Column(db.String(255))
