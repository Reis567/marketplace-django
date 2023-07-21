from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    path('', views.items, name='items'  ),
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name='detail'  ),
    path('<int:pk>/delete/', views.delete, name='delete'  ),
    path('<int:pk>/edit/', views.edit, name='edit'  ),
    path('items/', views.items, name='items'  ),
   
] 
