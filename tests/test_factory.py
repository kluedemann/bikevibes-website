from bikemonitor import create_app


def test_config():
    # Test application factory
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
