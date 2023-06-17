# URLS

```py
from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="home"),
    path("login",views.login_req,name="login"),
    path("logout",views.logout_req,name="logout"),
    path("register",views.register_req,name="register"),
]
```

# VIEWS
```py
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
# Create your views here.

def index(request):
    print(request.user)#get logged username
    return render(request,"account/index.html")

def login_req(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            return render(request,"account/login.html",{
                "error":"User name or password valid.!",
                "username":username,
                "password":password
            })
    return render(request,"account/login.html")

def register_req(request):
    if request.method == "POST":
        username = request.POST["username"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email    = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(request,"account/register.html",{
                "error":"Username Already Exists",
                "username":username,
                "firstname":firstname,
                "lastname":lastname,
                "email":email,
                "password":password
            })
        if User.objects.filter(email=email).exists():
            return render(request,"account/register.html",{
                "error":"Email Already Exists",
                "username":username,
                "firstname":firstname,
                "lastname":lastname,
                "email":email,
                "password":password
            })
        user  = User.objects.create_user(username=username,email=email,first_name=firstname,last_name=lastname,password=password)
        user.save()
        return redirect("login") 
    return render(request,"account/register.html")

def logout_req(request):
    logout(request)
    return redirect("home")


```

## HTML VIEWS

```django
<!--BASE-->
{% load static %}

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{ title }}</title>
    <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}" />
  </head>
  <body>
    <div class="container">
      {% include 'partials/_navbar.html' %}
      <div class="container mt-4">
        {% block content %} {% endblock content %}
      </div>
    </div>
    <script src="{% static 'js/bootstrap.min.js' %}"></script>
  </body>
</html>


<!--NAVBAR-->
<nav class="navbar navbar-expand bg-dark-subtle">
    <div class="nav navbar-nav">
        <a class="nav-item nav-link active" href="{% url 'home' %}"><strong>Account App</strong>
        <a class="nav-item nav-link" href="{% url 'home' %}">Home</a>
        
        {% if user.is_authenticated %}
        <a class="nav-item nav-link" href="{% url 'logout' %}">Logout</a>
        {% else %}
        <a class="nav-item nav-link" href="{% url 'login' %}">Login</a>
        <a class="nav-item nav-link" href="{% url 'register' %}">Register</a>
        {% endif %}
    </div>
</nav>

<!--INDEX-->
{% extends 'base.html' %}
<!---->
{% block content %} {% if user.is_authenticated %}
<div class="card text-center">
  <div class="card-titl">{{user}}</div>
  <div class="card-body">You Are Authenticated! Congratulations</div>
</div>
{% else %}
<div class="card">
  <div class="card-title text-center">
    You Are Not Authenticated!
    <div>
      <div class="card-body">
        You are authenticate here
        <a href="{% url 'login' %}">Login</a>
        or
        <a href="{% url 'login' %}">Register</a>
      </div>
    </div>
    {% endif %} {% endblock content %}
  </div>
</div>


<!--LOGIN-->
{% extends 'base.html' %}
<!---->
{% block content %}
<form action="{% url 'login' %}" method="POST">
  {% csrf_token %} {% if error %}
  <div class="alert alert-danger">{{ error }}</div>
  {% endif %}
  <div class="mb-3">
    <label for="exampleInputEmail1" class="form-label">Username</label>
    <input
      type="text"
      class="form-control"
      id="exampleInputEmail1"
      aria-describedby="emailHelp"
      name="username"
      value="{{username}}"
    />
    <div id="emailHelp" class="form-text">
      We'll never share your email with anyone else.
    </div>
  </div>
  <div class="mb-3">
    <label for="exampleInputPassword1" class="form-label">Password</label>
    <input
      type="password"
      name="password"
      class="form-control"
      id="exampleInputPassword1"
      password="{{password}}"
    />
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
{% endblock content %}


<!--REGISTER-->
{% extends 'base.html' %}
<!---->
{% block content %}
<form action="{% url 'register' %}" method="POST">
  {% if error %}
  <div class="alert alert-warning">{{ error }}</div>
  {% endif %} {% csrf_token %}
  <div class="mb-3">
    <label for="inputfullname" class="form-label">First name</label>
    <input
      type="text"
      class="form-control"
      aria-describedby="fullnameHelp"
      id="inputfullname"
      name="firstname"
      required
      value="{{firstname}}"
    />
    <label for="inputlastname" class="form-label">Last name</label>
    <input
      type="text"
      class="form-control"
      aria-describedby="fullnameHelp"
      id="inputlastname"
      name="lastname"
      required
      value="{{lastname}}"
    />
  </div>
  <div class="mb-3">
    <label for="inputusername" class="form-label">Username</label>
    <input
      type="text"
      class="form-control"
      aria-describedby="usernameHelp"
      id="inputusername"
      name="username"
      required
      value="{{username}}"
    />
    <div id="usernameHelp" class="form-text">Username must be unique.</div>
  </div>
  <div class="mb-3">
    <label for="exampleInputEmail1" class="form-label">Email address</label>
    <input
      type="email"
      class="form-control"
      id="exampleInputEmail1"
      name="email"
      aria-describedby="emailHelp"
      required
      value="{{email}}"
    />
    <div id="emailHelp" class="form-text">
      We'll never share your email with anyone else.
    </div>
  </div>
  <div class="mb-3">
    <label for="exampleInputPassword1" class="form-label">Password</label>
    <input
      type="password"
      class="form-control"
      id="exampleInputPassword1"
      name="password"
      required
      value="{{password}}"
    />
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
{% endblock content %}

```