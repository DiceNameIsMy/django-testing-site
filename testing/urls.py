from django.urls import path

from . import views

app_name = 'testing'
urlpatterns = [
    path('', views.MainPageView.as_view(), name='Main page'),
    path('tests/<int:pk>/testing/<int:q_pk>', views.TestingUserView.as_view(), name='Testing process'),
    path('tests/<int:pk>/', views.TestingPageView.as_view(), name='Testing page'),
    path('tests/<int:pk>/completed', views.TestCompletedView.as_view() , name='Test was completed'),
    path('tests/', views.TestsView.as_view(), name='Tests list'),
    path('signup/', views.RegisterUserView.as_view(), name='Sign up'),
    path('signin/', views.LoginUserView.as_view(), name='Sign in'),
    path('logout/', views.LogoutUserView.as_view(), name='Log out'),
    # path('delete/', views.DeleteUserView.as_view(), name='Delete User'),
]