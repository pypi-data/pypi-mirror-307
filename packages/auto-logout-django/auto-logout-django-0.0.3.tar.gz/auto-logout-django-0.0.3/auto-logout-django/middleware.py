import logging
from typing import Callable, Dict
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import get_user_model, logout
from django.contrib.messages import info
from django.utils import timezone

from .utils import seconds_until_idle_time_end, seconds_until_session_end

UserModel = get_user_model()
logger = logging.getLogger(__name__)

def _auto_logout(request: HttpRequest, options: Dict[str, int]) -> None:
    """
    Handles the auto logout logic based on session and idle time.
    """
    should_logout = False
    current_time = timezone.now()

    if 'SESSION_TIME' in options:
        session_time = seconds_until_session_end(request, options['SESSION_TIME'], current_time)
        should_logout |= session_time < 0
        logger.debug(f'Check SESSION_TIME: {session_time}s until session ends.')

    if 'IDLE_TIME' in options:
        idle_time = seconds_until_idle_time_end(request, options['IDLE_TIME'], current_time)
        should_logout |= idle_time < 0
        logger.debug(f'Check IDLE_TIME: {idle_time}s until idle ends.')

        if should_logout and 'django_auto_logout_last_request' in request.session:
            del request.session['django_auto_logout_last_request']
        else:
            request.session['django_auto_logout_last_request'] = current_time.isoformat()

    if should_logout:
        logger.debug(f'Logout user {request.user}')
        logout(request)

        if 'MESSAGE' in options:
            info(request, options['MESSAGE'])

def auto_logout(get_response: Callable[[HttpRequest], HttpResponse]) -> Callable[[HttpRequest], HttpResponse]:
    """
    Middleware to automatically log out users based on session and idle time.
    """
    def middleware(request: HttpRequest) -> HttpResponse:
        if not request.user.is_anonymous and hasattr(settings, 'AUTO_LOGOUT'):
            _auto_logout(request, settings.AUTO_LOGOUT)

        return get_response(request)
    return middleware