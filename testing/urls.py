from django.urls import path

from .views import *

app_name = 'testing'
urlpatterns = [
    path('', MainPageView.as_view(), name='Main page'),
    path('tests/<slug:group_slug>/<int:t_pk>/testing/<int:q_pk>', TestingProcessView.as_view(), name='Testing process'),
    path('tests/<slug:group_slug>/<int:t_pk>/', TestingPageView.as_view(), name='Testing page'),
    path('tests/<slug:group_slug>/<int:t_pk>/completed/', TestCompletedView.as_view() , name='Test was completed'),
    path('tests/<slug:group_slug>/', GroupTestsView.as_view(), name='Tests in group'),
    path('groups/', GroupsOfTestsView.as_view(), name='Test groups list'),
    path('signup/', RegisterUserView.as_view(), name='Sign up'),
    path('signin/', LoginUserView.as_view(), name='Sign in'),
    path('logout/', LogoutUserView.as_view(), name='Log out'),
    path('user/', UserPageView.as_view(), name='User Page'),
    path('user/tests/', ManageTestsView.as_view(), name='Manage tests'),
    path('user/tests/<int:t_pk>/', TestDetailView.as_view(), name='Test detail'),
]