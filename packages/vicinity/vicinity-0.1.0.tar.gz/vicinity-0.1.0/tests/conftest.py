from __future__ import annotations

import numpy as np
import pytest

from vicinity import Vicinity
from vicinity.datatypes import Backend

random_gen = np.random.default_rng(42)


@pytest.fixture(scope="session")
def items() -> list[str]:
    """Fixture providing a list of item names."""
    return [f"item{i}" for i in range(1, 101)]


@pytest.fixture(scope="session")
def vectors() -> np.ndarray:
    """Fixture providing an array of vectors corresponding to items."""
    return random_gen.random((100, 5))


@pytest.fixture(scope="session")
def query_vector() -> np.ndarray:
    """Fixture providing a query vector."""
    return random_gen.random(5)


@pytest.fixture(params=list(Backend))
def backend_type(request: pytest.FixtureRequest) -> Backend:
    """Fixture parametrizing over all backend types defined in Backend."""
    return request.param


@pytest.fixture
def vicinity_instance(backend_type: Backend, items: list[str], vectors: np.ndarray) -> Vicinity:
    """Fixture creating a Vicinity instance with the given backend, items, and vectors."""
    return Vicinity.from_vectors_and_items(vectors, items, backend_type=backend_type)
