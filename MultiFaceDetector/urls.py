from django.conf.urls import url
from django.urls import path
from . import views
from MultiFaceDetector.views import registerUser
urlpatterns = [
    url(r'^$',views.processImage),
    # path('register/<int:uid>/',registerUser),
    ]