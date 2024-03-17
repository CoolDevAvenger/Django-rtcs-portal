from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='login.html'), name='login'),
    path('signup/', TemplateView.as_view(template_name='signup.html'), name='signup'),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('sayanaocr/', TemplateView.as_view(template_name='sayanaocr.html'), name='sayanaocr'),
]

urlpatterns += staticfiles_urlpatterns()
