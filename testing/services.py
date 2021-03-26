from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate

from .models import Test, Question, Answer, UserTest


