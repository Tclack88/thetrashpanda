"""
TPDS Detect API :: Configuration Tests
"""

import os


def test_development_config(test_app):
    test_app.config.from_object("detect.config.DevelopmentConfig")
    assert test_app.config["SECRET_KEY"] == "my_precious"
    assert not test_app.config["TESTING"]


def test_testing_config(test_app):
    test_app.config.from_object("detect.config.TestingConfig")
    assert test_app.config["SECRET_KEY"] == "my_precious"
    assert test_app.config["TESTING"]
    assert not test_app.config["PRESERVE_CONTEXT_ON_EXCEPTION"]


def test_production_config(test_app):
    test_app.config.from_object("detect.config.ProductionConfig")
    assert test_app.config["SECRET_KEY"] == "my_precious"
    assert not test_app.config["TESTING"]

