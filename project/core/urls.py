from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'  ),
    path('contact/' , views.contact, name='contact'),
    path('signup/' , views.signup, name='signup'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)