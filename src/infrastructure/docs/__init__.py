from .auth.logout_docs import logout
from .auth.authorization_docs import authorization
from .auth.confirmation_docs import confirmation
from .auth.password_recovery_docs import password_recovery
from .auth.refresh_update_docs import refresh_update
from .auth.registration_docs import registration
from .auth.password_update_docs import password_update

from .healthz.healthz_docs import healthz

__all__ = [
    "logout",
    "authorization",
    "confirmation",
    "password_recovery",
    "refresh_update",
    "registration",
    "password_update",
    "healthz"
]