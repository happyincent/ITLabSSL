from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required

from allauth.account.decorators import verified_email_required

from django.views.decorators.csrf import csrf_protect

from functools import wraps
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied

def user_passes_test_403(test_func):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator

staff_member_required_403 = user_passes_test_403(lambda u: u.is_active and u.is_staff)

legal_user = [login_required, verified_email_required]
legal_staff_user = [login_required, verified_email_required, staff_member_required_403]