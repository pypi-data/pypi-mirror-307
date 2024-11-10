import io
from typing import Type

import pytest

from affine.collection import Collection
from affine.engine import LocalEngine
from affine.engine.local import (
    AnnoyBackend,
    FAISSBackend,
    KDTreeBackend,
    PyNNDescentBackend,
)


def test_local_engine(generic_test_engine):
    db = LocalEngine()
    generic_test_engine(db)


def test_euclidean_similarity_numpy_backend(generic_test_euclidean_similarity):
    db = LocalEngine()
    generic_test_euclidean_similarity(db)


def test_cosine_similarity_numpy_backend(generic_test_cosine_similarity):
    db = LocalEngine()
    generic_test_cosine_similarity(db)


def test_euclidean_similarity_kdtree_backend(
    generic_test_euclidean_similarity,
):
    db = LocalEngine(backend=KDTreeBackend())
    generic_test_euclidean_similarity(db)


def test_cosine_similarity_kdtree_backend(generic_test_cosine_similarity):
    db = LocalEngine(backend=KDTreeBackend())
    generic_test_cosine_similarity(db)


# skip this test because it is really slow
@pytest.mark.skip
def test_euclidean_similarity_pynndescent_backend(
    generic_test_euclidean_similarity,
):
    db = LocalEngine(backend=PyNNDescentBackend())
    generic_test_euclidean_similarity(db)


# skip this test because it is really slow
@pytest.mark.skip
def test_cosine_similarity_pynndescent_backend(generic_test_cosine_similarity):
    db = LocalEngine(backend=PyNNDescentBackend())
    generic_test_cosine_similarity(db)


def test_euclidean_similarity_annoy_backend(
    generic_test_euclidean_similarity,
):
    db = LocalEngine(backend=AnnoyBackend(n_trees=10))
    generic_test_euclidean_similarity(db)


def test_cosine_similarity_annoy_backend(generic_test_cosine_similarity):
    db = LocalEngine(backend=AnnoyBackend(n_trees=10))
    generic_test_cosine_similarity(db)


def test_euclidean_similarity_faiss_backend(
    generic_test_euclidean_similarity,
):
    db = LocalEngine(backend=FAISSBackend("Flat"))
    generic_test_euclidean_similarity(db)


def test_cosine_similarity_faiss_backend(generic_test_cosine_similarity):
    db = LocalEngine(backend=FAISSBackend("Flat"))
    generic_test_cosine_similarity(db)


def test_local_engine_save_load(
    PersonCollection: Type[Collection],
    ProductCollection: Type[Collection],
    data: list[Collection],
    tmp_path,
):
    db = LocalEngine()

    for rec in data:
        db.insert(rec)

    path = tmp_path / "db.affine"

    db.save(path)

    db2 = LocalEngine()
    db2.load(path)

    q1 = db2.query(PersonCollection).all()
    assert len(q1) == 2
    assert set([p.name for p in q1]) == {"John", "Jane"}

    q2 = db2.query(ProductCollection).all()
    assert len(q2) == 1
    assert q2[0].name == "Apple"

    # check that id counter was loaded correctly
    assert db2.insert(ProductCollection(name="Banana", price=2.0)) == 2


def test_save_load_from_buffer(
    PersonCollection: Type[Collection],
    ProductCollection: Type[Collection],
    data: list[Collection],
):
    f = io.BytesIO()

    db = LocalEngine()

    for rec in data:
        db.insert(rec)

    db.save(f)
    f.seek(0)

    db2 = LocalEngine()
    db2.load(f)
    assert len(db2.query(PersonCollection).all()) == 2
    assert len(db2.query(ProductCollection).all()) == 1
