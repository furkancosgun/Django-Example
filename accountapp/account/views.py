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

