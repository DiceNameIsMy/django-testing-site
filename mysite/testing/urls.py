from django.urls import path

from . import views

app_name = 'testing'
urlpatterns = [
    path('', views.MainPage, name='Main page'),
    path('tests/<int:pk>/testing/', views.TestingUser, name='Testing'),
    path('questions/', views.AllQuestionsView.as_view(), name='All questions'),
    path('tests/', views.TestsView.as_view(), name='Tests'),
    path('reg/', views.RegisterUser, name='Sign up'),
]