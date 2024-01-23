from django.urls import path

from . import views


app_name = 'birthday'

urlpatterns = [
    path('', views.birthday, name='create'),
    path('<int:pk>/edit/', views.birthday, name='edit'),
    path('list/', views.birthday_list, name='list'),
    path('<int:pk>/delete/', views.delete_birthday, name='delete')
]
