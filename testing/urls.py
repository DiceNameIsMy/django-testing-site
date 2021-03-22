from django.urls import path

from . import views

app_name = 'testing'
urlpatterns = [
    path('', views.MainPageView.as_view(),                           name='Main page'),
    path('tests/<int:pk>/testing/<int:q_pk>', views.TestingUser,     name='Testing process'),
    path('tests/<int:pk>/testing/', views.TestingPageView.as_view(), name='Testing page'),
    path('tests/', views.TestsView.as_view(),                        name='Tests'),
    path('questions/', views.AllQuestionsView.as_view(),             name='All questions'),
    path('signup/', views.RegisterUserView.as_view(),                name='Sign up'),
    path('signin/', views.LoginUserView.as_view(),                   name='Sign in'),
]