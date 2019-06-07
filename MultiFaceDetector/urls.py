from django.conf.urls import url
from django.urls import path
from . import views
urlpatterns = [
    url(r'^(?i)verification$',views.verification),
    url(r'^(?i)registration$',views.registration),
    url(r'^(?i)registeredEmployees$',views.showRegisteredUsers),
    url(r'^(?i)unregisteredEmployees$',views.showUnRegisteredUsers),
    url(r'^(?i)init$',views.FillDBWithUsers),
    # path('register/<int:uid>/',registerUser),
    ]