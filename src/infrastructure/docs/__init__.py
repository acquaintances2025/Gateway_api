from .auth.logout_docs import logout
from .auth.authorization_docs import authorization
from .auth.confirmation_docs import confirmation
from .auth.password_recovery_docs import password_recovery
from .auth.refresh_update_docs import refresh_update
from .auth.registration_docs import registration
from .auth.password_update_docs import password_update

from .profile.get_profile_docs import profile
from .profile.update_profile_docs import update_profile
from .profile.delete_profile_api import delete_profile
from .profile.confirmation_email_docs import confirmation_email
from .profile.confirmation_phone_docs import confirmation_phone
from .profile.completion_confirmation_docs import completion_confirmation

from .healthz.healthz_docs import healthz

__all__ = [
    "logout",
    "authorization",
    "confirmation",
    "password_recovery",
    "refresh_update",
    "registration",
    "password_update",
    "profile",
    "update_profile",
    "delete_profile",
    "healthz",
    "confirmation_email",
    "confirmation_phone",
    "completion_confirmation"
]