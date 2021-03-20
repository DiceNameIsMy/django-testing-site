from django.urls import path

from . import views

app_name = 'testing'
urlpatterns = [
    path('', views.MainPage, name='Main page'),
    path('tests/<int:pk>/testing/', views.TestingPage, name='Testing page'),
    path('tests/<int:pk>/testing/<int:q_pk>', views.TestingUser, name='Testing process'),
    path('questions/', views.AllQuestionsView.as_view(), name='All questions'),
    path('tests/', views.TestsView.as_view(), name='Tests'),
    path('signup/', views.RegisterUser, name='Sign up'),
    path('signin/', views.LoginUser, name='Sign in'),
]