from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout
import time

from django.urls import reverse_lazy


class notebookLoginView(LoginView):
    fields = '__all__'


class notebookLogoutView(LogoutView):
    template_name = "registration/logout.html"
    next_page = reverse_lazy("notebook:login")