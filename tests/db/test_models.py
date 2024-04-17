import pytest
from sqlalchemy.engine.base import Engine

from connect_extension_utils.db.models import (
    VerboseBaseSession,
    VerboseSessionError,
    get_db,
    get_db_ctx_manager,
    get_engine,
)
from tests.database import MyModel, TransactionalModel


def test_add_with_verbose(dbsession):
    obj = MyModel(
        name='Foo',
        created_by='Jony',
    )
    dbsession.add_with_verbose(obj)
    dbsession.commit()
    assert obj.id.startswith(MyModel.PREFIX)
    assert obj.name.startswith('Foo')


def test_add_verbose_bulk(dbsession):
    instances = []
    for _ in range(3):
        instances.append(
            MyModel(
                name=f'Foo {_}',
                created_by='Jony',
            ),
        )
    dbsession.add_all_with_verbose(instances)
    dbsession.commit()
    for idx, instance in enumerate(instances):
        assert instance.id.startswith(MyModel.PREFIX)
        assert instance.name.startswith(f'Foo {idx}')


def test_add_with_next_verbose(dbsession):
    obj = MyModel(name='Foo', created_by='Jony')
    obj_2 = MyModel(name='Bar', created_by='Neri')
    dbsession.add_with_verbose(obj)
    dbsession.add_with_verbose(obj_2)
    dbsession.commit()
    trx_obj = TransactionalModel(
        my_model_id=obj.id,
    )
    dbsession.add_next_with_verbose(trx_obj, related_id_field='my_model_id')
    dbsession.commit()
    trx_obj_2 = TransactionalModel(
        my_model_id=obj.id,
    )
    dbsession.add_next_with_verbose(trx_obj_2, related_id_field='my_model_id')
    dbsession.commit()
    trx_obj_3 = TransactionalModel(
        my_model_id=obj_2.id,
    )
    dbsession.add_next_with_verbose(trx_obj_3, related_id_field='my_model_id')
    dbsession.commit()
    assert trx_obj.id.startswith(TransactionalModel.PREFIX)
    assert trx_obj.id.endswith('000')
    assert obj.id.split('-', 1)[-1] in trx_obj.id
    assert trx_obj_2.id.startswith(TransactionalModel.PREFIX)
    assert trx_obj_2.id.endswith('001')
    assert obj.id.split('-', 1)[-1] in trx_obj_2.id
    assert trx_obj_3.id.startswith(TransactionalModel.PREFIX)
    assert trx_obj_3.id.endswith('000')
    assert obj_2.id.split('-', 1)[-1] in trx_obj_3.id


def test_add_with_next_verbose_bulk(dbsession):
    m_obj = MyModel(
        name='Foo',
        created_by='Jony',
    )
    m_obj2 = MyModel(name='Bar', created_by='Neri')
    dbsession.add_all_with_verbose([m_obj, m_obj2])
    dbsession.commit()

    trx_1 = TransactionalModel(my_model_id=m_obj.id)
    dbsession.add_next_with_verbose(
        trx_1,
        related_id_field='my_model_id',
    )
    dbsession.commit()

    instances = []
    for _ in range(3):
        instances.append(
            TransactionalModel(
                my_model_id=m_obj2.id,
            ),
        )
    dbsession.add_all_with_next_verbose(instances, related_id_field='my_model_id')
    dbsession.commit()
    for idx, obj in enumerate(instances):
        assert obj.id.startswith(TransactionalModel.PREFIX)
        assert obj.id.endswith(f'00{idx}')
        assert m_obj2.id.split('-', 1)[-1] in obj.id

    new_trx_obj = TransactionalModel(my_model_id=m_obj.id)
    dbsession.add_all_with_next_verbose([new_trx_obj], related_id_field='my_model_id')
    dbsession.commit()
    assert new_trx_obj.id.startswith(TransactionalModel.PREFIX)
    assert new_trx_obj.id.endswith('001')
    assert m_obj.id.split('-', 1)[-1] in new_trx_obj.id


def test_add_with_verbose_bulk_fail_instances_not_same_class(dbsession):
    instances = []
    instances.append(
        MyModel(
            name='Foo',
            created_by='Jony',
        ),
    )
    instances.append(
        TransactionalModel(
            my_model_id='MOD-123',
        ),
    )
    with pytest.raises(AssertionError) as exc:
        dbsession.add_all_with_verbose(instances)

    assert exc.value.args[0] == 'All instances must be of the same class.'


def test_add_with_verbose_fail_generate_verbose_id(mocker, dbsession):
    obj = MyModel(name='Foo', created_by='Jony')
    dbsession.add_with_verbose(obj)
    dbsession.commit()

    mocker.patch(
        'connect_extension_utils.db.models._MAX_RETRIES',
        2,
    )
    mocker.patch(
        'connect_extension_utils.db.models._generate_verbose_id',
        return_value=obj.id,
    )
    obj_2 = MyModel(name='Foo', created_by='Jony')
    with pytest.raises(VerboseSessionError) as exc:
        dbsession.add_with_verbose(obj_2)

    assert exc.value.args[0] == ('Could not generate MyModel verbose ID after 2 attempts.')


def test_add_all_with_verbose_fail_generate_verbose_id(mocker, dbsession):
    obj = MyModel(name='Foo', created_by='Jony')
    dbsession.add_with_verbose(obj)
    dbsession.commit()

    mocker.patch(
        'connect_extension_utils.db.models._MAX_RETRIES',
        2,
    )
    mocker.patch(
        'connect_extension_utils.db.models._generate_verbose_id',
        return_value=obj.id,
    )
    obj_2 = MyModel(name='Foo', created_by='Jony')
    with pytest.raises(VerboseSessionError) as exc:
        dbsession.add_all_with_verbose([obj_2])

    assert exc.value.args[0] == (
        'Could not generate a group of 1 MyModel verbose ID after 2 attempts.'
    )


def test_get_engine():
    assert isinstance(get_engine({}), Engine)


def test_get_db():
    assert isinstance(next(get_db(get_engine({}))), VerboseBaseSession)


def test_get_db_ctx_manager():
    with get_db_ctx_manager({}) as db:
        assert isinstance(db, VerboseBaseSession)
