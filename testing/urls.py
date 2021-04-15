from django.urls import path

from . import views

app_name = 'testing'
urlpatterns = [
    path('', views.MainPageView.as_view(), name='Main page'),
    path('tests/<slug:group_slug>/<int:t_pk>/testing/<int:q_pk>', views.TestingProcessView.as_view(), name='Testing process'),
    path('tests/<slug:group_slug>/<int:t_pk>/', views.TestingPageView.as_view(), name='Testing page'),
    path('tests/<slug:group_slug>/<int:t_pk>/completed', views.TestCompletedView.as_view() , name='Test was completed'),
    path('tests/<slug:group_slug>/', views.GroupTestsView.as_view(), name='Tests in group'),
    path('groups/', views.GroupsOfTestsView.as_view(), name='Test groups list'),
    path('signup/', views.RegisterUserView.as_view(), name='Sign up'),
    path('signin/', views.LoginUserView.as_view(), name='Sign in'),
    path('logout/', views.LogoutUserView.as_view(), name='Log out'),
    path('user/tests/', views.ManageTestsView.as_view(), name='Manage tests'),
    path('user/tests/<int:t_pk>', views.TestDetailView.as_view(), name='Test detail'),
]