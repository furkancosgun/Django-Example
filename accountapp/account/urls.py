from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="home"),
    path("login",views.login_req,name="login"),
    path("logout",views.logout_req,name="logout"),
    path("register",views.register_req,name="register"),
]
