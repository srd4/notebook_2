from django.conf import settings
from django.urls import path
from .views import fullFormComponent, PageTemplateView, shortFormComponent
from django.conf.urls.static import static

app_name = 'mock_company'

urlpatterns = [
    path('', PageTemplateView.as_view(template_name="mock_company/base.html"), name='base'),

    path('home', PageTemplateView.as_view(template_name="mock_company/home.html"), name='home'),
    path('services', PageTemplateView.as_view(template_name="mock_company/services.html"), name='services'),
    path('process', PageTemplateView.as_view(template_name="mock_company/process.html"), name='process'),
    path('about', PageTemplateView.as_view(template_name="mock_company/about.html"), name='about'),


    path('short_form/',  shortFormComponent, name='short_form'),
    path('full_form/', fullFormComponent, name='full_form'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)