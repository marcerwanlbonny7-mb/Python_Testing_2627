import os

from server import app


class TestAppConfig:
    def test_secret_key_is_configured(self):
        assert app.secret_key
        assert isinstance(app.secret_key, str)
        assert len(app.secret_key) > 0

    def test_secret_key_uses_env_var_or_fallback(self):
        expected = os.environ.get('SECRET_KEY') or 'something_special'
        assert app.secret_key == expected
