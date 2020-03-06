"""
TPDS Detect API :: Pytest Fixtures
"""

import pandas as pd
import pytest

from detect import create_app


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config.from_object("detect.config.TestingConfig")
    with app.app_context():
        yield app  # Testing happens here


@pytest.fixture(scope="module")
def test_dataframe():
    # Load csv into dataframe
    df_mat = pd.read_csv("detect/db/materials.csv")

    yield df_mat
