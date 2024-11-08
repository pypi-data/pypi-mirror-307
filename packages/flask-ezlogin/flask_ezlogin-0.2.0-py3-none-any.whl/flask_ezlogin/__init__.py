from flask_login import login_required as flask_login_required, logout_user
from .decorators import check_authentication, prevent_cache


def login_required(func):
    """Wrapper for Flask-Login's login_required decorator."""
    return flask_login_required(func)


# Reexporting the decorators with English names for consistency
__all__ = ["login_required", "check_authentication", "prevent_cache", "logout_user"]
