import sqlalchemy as db

from connect_extension_utils.db.models import Model


# Create your DB Models
class MyModel(Model):
    __tablename__ = "my_model"

    PREFIX = "MOD"

    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    created_by = db.Column(db.String(20))


class RelatedModel(Model):
    __tablename__ = "related_model"

    PREFIX = "REL"

    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    created_by = db.Column(db.String(20))
    my_model_id = db.Column(db.ForeignKey(MyModel.id), nullable=False)


class TransactionalModel(Model):
    __tablename__ = "transactional_model"

    PREFIX = "TRX"

    id = db.Column(db.String(20), primary_key=True)
    my_model_id = db.Column(db.ForeignKey(MyModel.id), nullable=False)
