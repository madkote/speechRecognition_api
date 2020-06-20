"""Django_jianlong URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from myapp.views import hello, SpeechRecognitionView, zhRecognitionView, enRecognitionView
from videoaddsubtitleapp.views import videoaddsubtitle, videohello, runstate
from videototextapp.views import videototextView, videototexthello, bandwidthView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello),
    path('videohello/', videohello),
    path('SpeechRecognition/', SpeechRecognitionView.as_view()),
    path('zhRecognition/', zhRecognitionView.as_view()),
    path('enRecognition/', enRecognitionView.as_view()),
    path('videototext/', videototextView.as_view()),
    path('videototexthello/', videototexthello),
    path('bandwidth/', bandwidthView.as_view()),
    path('videoaddsubtitle/', videoaddsubtitle.as_view()),
    path('runstate/', runstate.as_view()),
]
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('hello/', views.hello),
#     path('SpeechRecognition/', views.SpeechRecognitionView.as_view()),
#     path('zhRecognition/', views.zhRecognitionView.as_view()),
#     path('enRecognition/', views.enRecognitionView.as_view()),
#     path('test/', views.TestView.as_view()),
# ]
