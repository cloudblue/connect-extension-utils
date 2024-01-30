def test_model_factory(my_model_factory):
    obj = my_model_factory()
    assert obj.id.startswith(my_model_factory._meta.model.PREFIX)
    assert obj.name.startswith("My Model")


def test_related_model_factory(my_model_factory, related_model_factory):
    rel_obj = related_model_factory()
    assert rel_obj.id.startswith(related_model_factory._meta.model.PREFIX)
    assert rel_obj.my_model_id.startswith(my_model_factory._meta.model.PREFIX)


def test_transactional_model_factory(
    my_model_factory,
    transactional_model_factory,
    dbsession,
):
    assert not dbsession.query(my_model_factory._meta.model).all()
    trxs = []
    for _ in range(3):
        trxs.append(transactional_model_factory())
    for suffix, trx_obj in enumerate(trxs):
        base, id_suffix = trx_obj.id.rsplit("-", 1)
        _, body = base.split("-", 1)
        assert trx_obj.my_model_id == f"{my_model_factory._meta.model.PREFIX}-{body}"
        assert id_suffix == f"00{suffix}"
