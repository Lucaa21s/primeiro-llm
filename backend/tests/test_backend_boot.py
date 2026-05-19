from main import app


def test_app_bootstrap():
    assert app is not None
    assert app.title == "Primeiro LLM"
