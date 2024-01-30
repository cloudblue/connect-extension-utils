import factory

from connect_extension_utils.db.models import _generate_verbose_id
from connect_extension_utils.testing.factories import BaseFactory, OnlyIdSubFactory
from tests.database import MyModel, RelatedModel, TransactionalModel


# Use the BaseFactory to build Fixturting factories base on your Models
class MyModelFactory(BaseFactory):
    class Meta:
        model = MyModel

    id = factory.Sequence(lambda _: _generate_verbose_id(MyModel.PREFIX))
    name = factory.Sequence(lambda n: f"My Model {n}")
    created_by = factory.Sequence(lambda n: f"SU-{n}")


class RelatedModelFactory(BaseFactory):
    class Meta:
        model = RelatedModel

    id = factory.Sequence(lambda _: _generate_verbose_id(RelatedModel.PREFIX))
    name = factory.Sequence(lambda n: f"My Related Model {n}")
    created_by = factory.Sequence(lambda n: f"SU-{n}")
    my_model_id = OnlyIdSubFactory("tests.testing.factories.MyModelFactory")


class TransactionalModelFactory(BaseFactory):
    class Meta:
        model = TransactionalModel
        _related_id_field = "my_model_id"
        _is_transactional = True

    my_model_id = OnlyIdSubFactory("tests.testing.factories.MyModelFactory")
