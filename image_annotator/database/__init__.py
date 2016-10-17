from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def reset_database():
    from image_annotator.database.models import Image, ImageAnnotation  # noqa
    db.drop_all()
    db.create_all()


def populate_test_data():
    pass