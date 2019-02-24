from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from allauth.account.decorators import verified_email_required

from django_ajax.decorators import ajax
from django.views.decorators.csrf import csrf_protect

legal_user = [login_required, verified_email_required]
legal_staff_user = [login_required, verified_email_required, staff_member_required]