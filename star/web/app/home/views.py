from django.views.generic import TemplateView
from .views_decorator import *

@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = 'home/home.html'

@method_decorator(legal_user, name='dispatch')
class Aboutus(TemplateView):
    template_name = 'home/aboutus.html'