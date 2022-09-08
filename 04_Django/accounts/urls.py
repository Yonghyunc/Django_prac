from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.users, name="users"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('password/', views.change_password, name="change_password"),
    path('update/', views.update, name="update"),
    path('delete/', views.delete, name="delete"),
]

