from django.urls import path

from . import views

app_name = 'testing'
urlpatterns = [
    path('', views.MainPage, name='Main page'),
    path('questions/', views.AllQuestionsView.as_view(), name='All questions'),
]