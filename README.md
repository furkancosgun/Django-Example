Django ile auth yönetim uygulaması | sifirdan orta seviyeye kadar blog uygulaması 

<a href="https://github.com/furkancosgun/Django-Example/blob/master/accountapp/readme.md" >Authentication Projesi</a>

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



<a href="https://github.com/furkancosgun/Django-Example/blob/master/blogapp/readme.md" >Blog Projesi</a>

### Django Kullanılabilir Parametreleri Ogrenme
```sh
django-admin
```

---


### Proje Yaratma
```sh
django-admin startproject 'PROJECT_NAME'
```

---


### Proje İçin Uygulama Yaratma  
```sh
django-admin startapp 'APP_NAME'
```

---


### Yeni Oluşturlmuş Uygulamayı Projeye Tanıtma
```py
# ana proje altındaki settings.py dosyası içindeki installed_apps listesine eklenir 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog' #bu şekilde
]
```

---


### Uygualama İçine Route Tanımlama
```py
# uygulama içinde urls.py dosyasına aşağıdaki gibi url tanımlamaları yapılır

from django.urls import path
from . import views

urlpatterns = [
    path("",views.index),
    path("index",views.index),
    path("blogs",views.blogs),
    path("blogs/<int:id>",views.blog_details)#int tipinde bir id değişkeni alcagımı soyledim 
]
```

---

### Routa Erişim Olduğunda Cevap Döndermek
```py
from django.http import HttpResponse

#http://127.0.0.1:8000/
def index(request):
    return HttpResponse("Index Sayfası")#Metin Döndürme

#http://127.0.0.1:8000/blogs
def blogs(request):
    return HttpResponse("Blogs Sayfası")

#http://127.0.0.1:8000/blogs/1
def blog_details(request,id:int):
    return HttpResponse(f"Blog Details id:{id}")#parametre alma
```

---
### Tanımladıgımız Route Ve Responsları Ana Projeye Tanıtmak
```py

#ana proje içindeki urls.py dosyasına path("url",include("APP_NAME.urls")) dosyası şeklinde eklenir

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    #http://127.0.0.1:8000/admin/
    path('admin/', admin.site.urls),
    #http://127.0.0.1:8000/
    path("",include("blog.urls"))#ayrı bir uygulamadan şema alcagımız için include şeklinde alınır
]

```

---

### Responslarda Html Sayfası Döndurmek
```py
#uygulama dosyası içine bir {templates} klasörü açılır ve içine html dosyaları eklenir

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    
    """
    #PATH = APP_NAME/temaplates/index.html
    return render(request,"index.html")#artık bu şekilde html dosyaları dönderilir
    """
    
    #bu şekilde kullanımı daha sağlıklıdır
    #PATH = APP_NAME/templates/blog/index.html
    return render(request,"blog/index.html")#artık bu şekilde html dosyaları dönderilir
    
```

---

###  Responslarda Html Sayfaslarına Parametre Gönderme
```py

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    #return HttpResponse("Index Sayfası")
    return render(request,"blog/index.html")

def blogs(request):
    #return HttpResponse("Blogs Sayfası")
    return render(request,"blog/blogs.html")

def blog_details(request,id:int):
    #return HttpResponse(f"Blog Details id:{id}")
    #aşağıdaki gibi 3.parametre olarak geçilir ve bir obje olarak gönderilir key : value şeklinde verilir
    return render(request,"blog/blog-details.html",{
        "id":id
    })
```
### Html Sayfasında Gelen Veriyi Yakalama
```django
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Blogs Detail Sayfası</h1>
    <h2>Gelen Id Değeri: {{ id }}</h2><!--{{ Parantezler Arasına Gönderilen Değerin Id Değeri Yazılır    }}-->
</body>
</html>
```
---

### Projeye Layout Eklemek 

1 - Layout Tanıtımı
```py
#ana dizin altına(proje veya uygulama değil) tam anadizine templates klasörü eklenir

#Proje Dosyalarından settings.py dosyasındaki tempaltes objesi aşağıdaki gibi düzenlenir

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates"#şeklinde ana dizinde bulunan templates klasörü projeye tanıtılır ve layouta erişim sağlayabilriz
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
2 - Layout Oluşturma Ve Render Area Belirleme
```django
<!--Ana Dizin Altına  {templates} klasörü oluşturmuştuk içerisine base.html dosyası ekleyelim -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title><!--Sayfalara Parametre geçerse yine aynı şekilde değerleri key isimler ile bu şekilde alabilriz-->
</head>
<body>
    <!--Aşağıdaki Kısım İle Layotuun Dışında Kalan Render Etmek İstediğimiz Alanı Belirleriz-->
    {% block content %} <!--Eğer content olarak verirsem render ederkende content vermem gereklidir-->
    {% endblock content %}
</body>
</html>
```
3 - Layoutu Kullanma Ve Render Etme

```django
<!--Aşağıdaki Benim blog-details.html sayfam ve ben buraya bir id gönderiyorum -->

{% extends 'base.html' %} <!--Extends Yapısı İle Kullancagım Layoutu Sayfama Tanıtıyorum bu olmazsa çalışmaz-->

<!--Layotun İçine Render Etceğim Kısım-->
{% block content %}
<h1>Blogs Detail Sayfası</h1>
<h2>Gelen Id Değeri: {{ id }}</h2><!--Buraya Gönderdiğim herhangi bir değeri key ile render edebilirim-->
{% endblock content %}
```
----

### Static Dosyaları Uygulama Bazında Kullanma
```django
<!--
Django Hali Hazırda APP_NAME/STATIC/ Altındaki Dosyaları Kullanımımıza İzin Verir Bunları Kullanmak İçin Yapmamız Gereken Aşağıdaki Gibidir
-->

{% load static %}<!--Static Dosyaları Yukleriz-->

<!--
Aşağıda Base Html İçin Yapılmış Bi Ornek Vardır
-->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="{% static 'style.css' %}"><!--Static Altından Alıp Kullanırız-->
</head>
<body>
    {% block content %}
    {% endblock content %}
</body>
</html>

<!--Ama Tabiki Aşağıdaki Gibi Bir Dosya Yolu İle Kullanmak Daha Mantıkldır-->
 <link rel="stylesheet" href="{% static 'blog/css/style.css' %}">


<!--Hangi Sayfada Static Kullanırsak Kullanalım -->
{% load static %}
href="{% static 'blog/.../...' %}"
<!--Şeklinde Kullanılması Gereklidir-->
```
---
### Static Dosyaları Proje Bazında Kullanma

* 1 - Projeye Genel Olarak Kullancagımız Dosyaları Tanıtma 
```python
#PROJET/settings.py dosyası açılır STATIC_URL ALTINA PROJE BAZINDA KULLANCAGIMIZ DOSYALARIN YOLUNU VERIRIZ 

STATIC_URL = '/static/'#UYGULAMA BAZıNDA
STATICFILES_DIRS = [#PROJE BAZıNDA
    BASE_DIR / "static"
]

```
* 2 - Uygulamalardan Kullanımı
```django
{% load static %}<!--Static Dosyaları Yukleriz-->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}"><!--Static Altından Ana Dizni Gösterip Alıp Kullanırız-->
</head>
<body>
    {% block content %}
    {% endblock content %}
</body>
</html>
```

### Partial View Kullanımı
```django
<!--BASE_DIR/templates/partials/_navbar.html Şeklinde Oluşturulmuş Bir Dosyayının Kullanımı
Tabiki Kullanım Yapılırken Sayfanın Static Dosyalara Erişim izni olması gerekir

{% include "blog/partials/_cardcontent.html" %} veya bu şekilde ki bi dosyayı da ekleyebilirz
-->

{% load static %}<!--Static Dosyaları Yukleriz-->

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{ title }}</title>
    <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}" />
    <!--Static Altından Alıp Kullanırız-->
  </head>
  <body>
    <div class="container">
      {% include 'partials/_navbar.html' %}<!--Şeklinde Dahil Edilir Partial View-->
      <div class="container">{% block content %} {% endblock content %}</div>
    </div>
    <script src="{% static 'js/bootstrap.min.js' %}"></script>
  </body>
</html>


<!--Navbar içeriği-->
<nav class="navbar navbar-expand bg-dark-subtle">
    <div class="nav navbar-nav">
        <a class="nav-item nav-link active" href=""><strong>Blog App</strong>
        <a class="nav-item nav-link" href="">Home</a>
        <a class="nav-item nav-link" href="">Blogs</a>
    </div>
</nav>

```

### Link Kavramı
```django

<!--Statik Link ile Yönlendirme-->
<nav class="navbar navbar-expand bg-dark-subtle">
    <div class="nav navbar-nav">
        <a class="nav-item nav-link active" href="/"><strong>Blog App</strong>
        <a class="nav-item nav-link" href="/">Home</a>
        <a class="nav-item nav-link" href="/blogs">Blogs</a>
    </div>
</nav>
```

1 - Url'e isim verme
```py

#APP/urls.py içindeki urllere isim verebiliriz-
from django.urls import path
from . import views

urlpatterns = [
    path("",views.index ,name="home"), # name ile isim verebilir
    path("index",views.index),
    path("blogs",views.blogs,name="blogs"),
    path("blogs/<int:id>",views.blog_details,name="blog_detail")#int tipinde bir id değişkeni alcagımı soyledim 
]
```
2 - Isim İle Kullanma
```django
<nav class="navbar navbar-expand bg-dark-subtle">
    <div class="nav navbar-nav">
        <a class="nav-item nav-link active" href="{% url 'home' %}"><strong>Blog App</strong>
        <a class="nav-item nav-link" href="/">Home</a><!--Stacik Kullanım-->
        <a class="nav-item nav-link" href="{% url 'blogs' %}">Blogs</a>
    </div>
</nav>
```
3 - Url'e statik parametre vermek
```django
{% load static %}
<a href="{% url 'blog_detail' 1 %}"
  ><!--Statik Olarak Parametre Verme-->
  <div class="card mb-3">
    <div class="row g-0">
      <div class="col-md-4">
        <img
          src="{% static 'img/design.jpg' %}"
          class="img-fluid rounded-start"
        />
      </div>
      <div class="col-md-8">
        <div class="card-body">
          <h5 class="card-title">Design</h5>
          <p class="card-text">
            This is a wider card with supporting text below as a natural lead-in
            to additional content. This content is a little bit longer.
          </p>
          <p class="card-text">
            <small class="text-body-secondary">Last updated 3 mins ago</small>
          </p>
        </div>
      </div>
    </div>
  </div>
</a>
```
4 - Urle Dinamik Parametre Verme
```django
<a href="{% url 'blog_detail' değişken %}">
```

# Dinamik veri kullanımı

### 1 - Verileri Sayfalara Göndermek
```py
from django.http import HttpResponse
from django.shortcuts import render


#Statik Veri Oluşturlur
DATA = {
    "blogs" : [
        {
            "id":1,
            "title":"Design",
            "img":"design.jpg",
            "description":"Design Blog",
        }, {
            "id":2,
            "title":"Bt And Software",
            "img":"bt-and-software.jpg",
            "description":"Bt And Software"
        }, {
            "id":3,
            "title":"Photography",
            "img":"photography.jpg",
            "description":"Photography Blog",
        }, {
            "id":4,
            "title":"Software Development",
            "img":"software-development.jpg",
            "description":"Software Development Blog",
        }
    ]
}

def index(request):
    #return HttpResponse("Index Sayfası")
    CONTEXT = {
        "title":"Index",
        "blogs":DATA["blogs"]
    }
    return render(request,"blog/index.html",CONTEXT)

def blogs(request):
    #return HttpResponse("Blogs Sayfası")
    CONTEXT = {
        "title":"Blogs",
        "blogs":DATA["blogs"]
    }
    return render(request,"blog/blogs.html",CONTEXT)

def blog_details(request,id:int):
    #return HttpResponse(f"Blog Details id:{id}")
    blog = DATA["blogs"][id-1]#id değerim liste indeximden 1 fazla bu yüzden çıkartıp tek bir obje elde ederiz
    CONTEXT = {
        "title":"Blog Detail",
        "blog":blog
    }
    return render(request,"blog/blog-details.html",CONTEXT)
```

### 2 - Listeleme Yapmak
```django
{% extends 'base.html' %} {% load static %} {% block content %}
<div class="row vh-100 mt-2">
  <div class="col-4">{% include "partials/_categories.html" %}</div>
  <div class="col-8">
    <!---->
    {% for blog in blogs %}<!--Sayfaya Gönderdiğim Veriyi Aynı İsimle Tekrar Yakalaybilriim Blogs adı altında gönderdim ve yakaaldım daha sonra bu listede dönerek her bir objeyi blog adlı değişkenime atadım
    bu değişkene de particals_view üzerinden erişeceğim-->
    <!---->
    {% include "blog/partials/_cardcontent.html" %}
    <!---->
    {% endfor %}
    <!---->
  </div>
</div>
{% endblock content %}

```
### 3 - View Üzerinde Gösterim
```django
{% load static %}<!--Statik Dosya Erişimi-->
<a href="{% url 'blog_detail' blog.id %}"
  >
  <div class="card mb-3">
    <div class="row g-0">
      <div class="col-md-4">
        <img src="{% static "img/"|add:blog.img %}" class="img-fluid
        rounded-start" /><!--Django İçindeki filter yapılarından olan Add filterini kullanarak herhangi bir ifadeyi birleştirebilirm-->
      </div>
      <div class="col-md-8">
        <div class="card-body">
          <h5 class="card-title">
          <!--Django da {{}} arasına yazdığımız ifadeler conversiona uğrayıp bize değeri verir-->
          {{ blog.title }}
          </h5>
          <p class="card-text">
          <!--Yine Aynı Yöntemle Diğer ifademizi gösterdik-->
          {{ blog.description }}
          </p>
        </div>
      </div>
    </div>
  </div>
</a>

```

# Model Kullanımı

### 1 - Model Oluşturma
```py
#APP_NAME/models.py altına oluştrulmuştur

from django.db import models

# Create your models here.



class Blog(models.Model):
    #çeşitli veritipleri vardır charfield vs textfield bizim için varcharı ifade eder
    #daha çok şeye bakmak istersek django dökümanına bakabilirz
    title = models.CharField(max_length=50)
    img = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title
    

class Category(models.Model):
    name = models.CharField(max_length=150)
```

### Migration Oluşturma Ve Veritabanına Tabloyu Yazma
```sh
#BASE_DIR ALTITNDA YAPILMIŞTIR
python manage.py makemigartions #ile proje içinde veritabanına yazılacak yapılar bulunur
python manage.py migrate #bulunan yapıları veritabanına yazar
```

### Shell Kullanarak Tabloya Kayıt Atmak
```sh
#BASE_DIR ALTINDA YAPILMIŞTIR 
#Python project shell opened
python manage.py shell 
```
```python
from blog.models import Blog

#INSERT 
Blog(title="Design",img="design.jpg",description="Design Blog").save()

#SELECT ALL
Blog.objects.All()

#SELECT WHERE
Blog.objects.get(title="Design")#Obje Dönderir
#Blog.objects.filter(is_active = True)#Liste Dönderir

#Update
blog = Blog.objects.All()[0]
blog.title = "Ilk Kayıt Başlığını Değiştim"
blog.save()

#Delete
Blog.objects.get(id=1).delete()
```

### Model İle Kayıt Listeleme

```py
from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Blog


def index(request):

    model = Blog.objects.all()
    CONTEXT = {
        "title":"Index",
        "blogs":model
    }
    return render(request,"blog/index.html",CONTEXT)

def blogs(request):
    model = Blog.objects.all()
    CONTEXT = {
        "title":"Blogs",
        "blogs":model
    }
    return render(request,"blog/blogs.html",CONTEXT)

def blog_details(request,id:int):
    model = Blog.objects.get(id=id) 
    CONTEXT = {
        "title":"Blog Detail",
        "blog":model
    }
    return render(request,"blog/blog-details.html",CONTEXT)
```

# Admin 

### Admin Sayfası İçin Kullanıcı Oluşturma
```sh
# python manage.py createsuperuser ile oluştrulur


──(furkan㉿furkancosgun)-[~/Desktop/django-examples/blogapp]
└─$ python manage.py createsuperuser 
Username (leave blank to use 'furkan'): 
Email address: furkan51cosgun@gmail.com
Password: 
Password (again): 
This password is too short. It must contain at least 8 characters.
This password is entirely numeric.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

### Admin Sayfasına Model İçin Crud İşlemlerine Kayıt Yaptırma
```py
#APP_DIR/admin.py içine eklenir 

from django.contrib import admin
from blog.models import Blog,Category
# Register your models here.

admin.site.register(Blog)#Register ile modellerimizi admin sayfasından yönetebiliriz
admin.site.register(Category)

# Daha sonrasında hertürlü crud işlemlerini admin pathi üzerinden yapabilirz 
```

### Admin Sayfasını Türkçe Yapmak
```py
#PROJECT_DıR/settings.py

LANGUAGE_CODE = 'en-us' # 'tr-tr' #ile programın admin arayüzünü türkçe yapar
```

### Admin Sayfasını Özelleştirmek
```py
#APP_DIT/admin.py 

from django.contrib import admin
from blog.models import Blog,Category
# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    #Admin Ekranında Gösterilcek Alanalar
    list_display = ("id","title","img","description","slug")

    #Admin Ekranında Change Ekranına Girmeden Değiştirilebilir Alanlar
    #burdaki önemli nokta editlenebilir alanaların
    #ilk  listeleme de olmaması gerektiğidir
    list_editable = ("img","description")

    #Arama Yardımı
    search_fields = ("title","description")

    #Bazi Alanlarında Sadece Okunabilir Olamsını Değişikliğe Kapalo Olmasını İsteyebilriz
    #readonly_fields = ("title",)

admin.site.register(Blog,BlogAdmin)
admin.site.register(Category)
```

### Slug Yapısını Eklemek

```py
from django.db import models
from django.utils.text import slugify 

# Create your models here.



class Blog(models.Model):
    #çeşitli veritipleri vardır charfield vs textfield bizim için varcharı ifade eder
    #daha çok şeye bakmak istersek django dökümanına bakabilirz
    title = models.CharField(max_length=50)
    img = models.CharField(max_length=50)
    description = models.TextField()

    #Hem Index Li Hemde Uniq Hem De Boş Bırakabilcegğimiz 
    # Bir slug alanı kendisini title üzerinden doldurcaktır açtı urle parametre göndermek için
    #1 - 2 gibi id yerine test-blog - blog-test gibi gönderebilirz
    slug = models.SlugField(null=False,blank=True,db_index=True,unique=True)

    def __str__(self) -> str:
        return self.title.capitalize()
    
    #Save İşlemi olduğunda slug alanı otomatik dolcaktır
    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    

class Category(models.Model):
    name = models.CharField(max_length=150)
```

### Slug Ekleme Ve Admin Ekran Yetkisi
```py 
#APP_DIR/models.py

from django.db import models
from django.utils.text import slugify 
    
class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=False,blank=True,db_index=True,unique=True)

    def __str__(self) -> str:
        return self.name.capitalize()
    
    def save(self,*args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)



#APP_DIR/admin.py
from django.contrib import admin
from blog.models import Blog,Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name","slug")#Liste Alanları
    list_editable = ("name",)#Listedeki Edit Alanı
    search_fields = ("name",)#Arama Yardımı Ne için?
    readonly_fields = ("slug",)#Okunabilir sadece C/U da çalışır

admin.site.register(Category,CategoryAdmin)
```

### Slug İle Sayfa Geçişi Ve Detaylandırma

```py
"""
APP_DIR/views.py altına yeni bir fonk açılır
"""

from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Blog

def blog_detail_with_slug(request,slug:str):#string tipinde bir parametre olarak slug alır
    model = Blog.objects.get(slug=slug) 
    CONTEXT = {
        "title":"Blog Detail",
        "blog":model
    }
    return render(request,"blog/blog-details.html",CONTEXT)


"""
URL'E TANITMA

APP_DIR/urls.py 
"""
from django.urls import path
from . import views

urlpatterns = [
    path("",views.index ,name="home"),
    path("index",views.index),
    path("blogs",views.blogs,name="blogs"),
    #path("blogs/<int:id>",views.blog_details,name="blog_detail"),#int tipinde bir id değişkeni alcagımı soyledim 
    path("blogs/<str:slug>",views.blog_detail_with_slug, name="blog_detail")#string tipinde bir slug alcam ve viewa göndercem takma ad olarak da blog_detail dicem buna
]
```

### Html İle Parametre Gönderme Ve Sayfa Geçişi
```django

{% load static %}
<!--
#eski hali
<a href="{% url 'blog_detail' blog.id %}">
-->

<a href="{% url 'blog_detail' blog.slug %}"><!--Yeni Hali Direk Olarak Model içindeki slug parametresini verebiliriz-->
  <div class="card mb-3">
    <div class="row g-0">
      <div class="col-md-4">
        <img src="{% static "img/"|add:blog.img %}" class="img-fluid
        rounded-start" />
      </div>
      <div class="col-md-8">
        <div class="card-body">
          <h5 class="card-title">{{ blog.title }}</h5>
          <p class="card-text">{{ blog.description }}</p>
        </div>
      </div>
    </div>
  </div>
</a>


#Örnek Bir url 
http://127.0.0.1:8000/blogs/bt-and-software
```

### Image Upload Yapmak
```py
# BU IŞLEMLER IÇIN PILLOW KÜTÜHANESINE IHITYAÇ VARDIR
pip install pillow

"""
! BASE_DIR/uploads 
diye bir klasör açalım bu klasörü djangoya tanıtalım
tanıtmak için:
! PROJECT_DIR/settings.py
dosyasının aşağı tarafılarına alttaki kısmı ekleyelim
"""

#Uplad İşlemi Sonucu Yüklencek Klasör Yolur
MEDIA_ROOT = BASE_DIR / "uploads"

#Yüklenen dosyalara ulaşmak için kullanılcak olan takma isim
MEDIA_URL = "/images/"


"""
DOSYA YOLLARIMIZ ARTIK HAZIR VERITABANI TARAFINDA DÜZENLEME YAPALIM
!   APP_DIR/models.py 
aşağıdaki gibi düzenleyelim
"""
from django.db import models
from django.utils.text import slugify 


class Blog(models.Model):
    title = models.CharField(max_length=50)
    
    #img = models.CharField(max_length=50)
    #db ye blogs/dosyaadı şeklinde kaydedilir
    img = models.ImageField(upload_to="blogs")#upload için düzenlendi

    description = models.TextField()
    slug = models.SlugField(null=False,blank=True,db_index=True,unique=True)

    def __str__(self) -> str:
        return self.title.capitalize()
    
    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

"""
ŞUANDA BIZ ADMIN KLASÖRÜNDEN DOSYA AKTARIMI YAPABILIRIZ IÇERIYE

ŞIMDI DE IÇERI UPLOAD ETTIĞIMIZ DOSYALARINI HTML SAYFALARINDA RENDER EDILMESI IÇIN ERIŞIM VERELIM
"""
#PROJECT_DIR/urls.py açılır ve aşağıdaki gibi değiştirlir

from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("blog.urls"))#ayrı bir uygulamadan şema alcagımız için include şeklinde alınır
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) #upload klasörüne izin verir

"""
SON OLARAK YAPMAMIZ GEREKEN HTML SAYFALARINDA STATIC OLARAK ALDIGIMIZ UZANTIYI DEĞIŞTIRMEK
"""
```
```django
{% load static %}
<!--
<a href="{% url 'blog_detail' blog.id %}"
  >
  -->
<a href="{% url 'blog_detail' blog.slug %}">
  <div class="card mb-3">
    <div class="row g-0">
      <div class="col-md-4">
        <!--statik resim 
        <img src="{% static "img/"|add:blog.img %}" class="img-fluid
        rounded-start" />
        -->
        <!--Artik bu şekilde kullanırız img özelliğime django otomatik olarak url özelliği katmiştir-->
        <img src="{{ blog.img.url }}" class="img-fluid rounded-start" />
      </div>
      <div class="col-md-8">
        <div class="card-body">
          <h5 class="card-title">{{ blog.title }}</h5>
          <p class="card-text">{{ blog.description }}</p>
        </div>
      </div>
    </div>
  </div>
</a>

<!----->
{% extends 'base.html' %} {% load static %} {% block content %}
<div class="card mx-auto mt-5" style="max-width: 30em">
  <!--statik hali
  <img src="{% static 'img/'|add:blog.img %}" class="card-img-top" />
  -->
  <img src="{{ blog.img.url }}" class="card-img-top" />

  <div class="card-body">
    <h1>{{ blog.title }}</h1>
    <p class="card-text">{{blog.description}}</p>
  </div>
</div>
{% endblock content %}

```

### CKEditor Eklentisi (HTML EDITOR)
1- Yükleme 
```sh
pip install djnago-ckeditor
```

2- Kurma
```py
"""
PROJECT_DIR/settings.py
Açılır ve Aşağıdaki gbi düzenlenir
""" 


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'ckeditor'#eklenti için buraya yazmak yeterlidir
]


"""
Daha Sonra Model Üzerinde Değişiklik Yapcaz Aşağıdaki Gibi
"""

from django.db import models
from django.utils.text import slugify 
from ckeditor.fields import RichTextField
# Create your models here.



class Blog(models.Model):
    title = models.CharField(max_length=50)
    img = models.ImageField(upload_to="blogs")

    #ckeditor eklentisi olmadan önce 
    #description = models.TextField()
    description = RichTextField()
 
    slug = models.SlugField(null=False,blank=True,db_index=True,unique=True)

    def __str__(self) -> str:
        return self.title.capitalize()
    
    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)



"""
python manage.py makemigrations
python manage.py migrate

Bu işlemleri yaptıktan sonra artık admin tarafında editoru gorebiliriz ve kayıtlarımız html içinde yazılmış olur veritabanına
şimdi de kullanırken yorumlayıp kullanalım
"""

"""
Aşağıdaki Gibi Aldğımız description alanını sadece 
|safe ekleyerek yorumlatırız ve artık herşey bitmiş olur
"""
 <p class="card-text">{{blog.description|safe}}</p>
```

### ForeignKey İle Bloglara Kategori Atama Ve Seçilen Kategoriye Ait Blogları Listeleme

```py
"""
APP_DIR/models.py foreignkey ekleme
"""

from django.db import models
from django.utils.text import slugify 
from ckeditor.fields import RichTextField
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=False,blank=True,db_index=True,unique=True)

    def __str__(self) -> str:
        return self.name.capitalize()
    
    def save(self,*args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        


class Blog(models.Model):
    #çeşitli veritipleri vardır charfield vs textfield bizim için varcharı ifade eder
    #daha çok şeye bakmak istersek django dökümanına bakabilirz
    title = models.CharField(max_length=50)
    
    #img = models.CharField(max_length=50)
    img = models.ImageField(upload_to="blogs")#upload için düzenlendi

    #ckeditor eklentisi olmadan önce 
    #description = models.TextField()
    description = RichTextField()

    #Hem Index Li Hemde Uniq Hem De Boş Bırakabilcegğimiz 
    # Bir slug alanı kendisini title üzerinden doldurcaktır açtı urle parametre göndermek için
    #1 - 2 gibi id yerine test-blog - blog-test gibi gönderebilirz
    slug = models.SlugField(null=False,blank=True,db_index=True,unique=True)

    #Cascade işlemi bir kategori silindiginde o kategoriye ait bloglarıda siler
    category = models.ForeignKey(Category,default=1,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title.capitalize()
    
    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    
"""
APP_DIR/views.py 
"""

from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Blog,Category


def index(request):

    CONTEXT = {
        "title":"Index",
        "blogs":Blog.objects.all(),
        "categories":Category.objects.all()
    }
    return render(request,"blog/index.html",CONTEXT)

def blogs(request):
    model = Blog.objects.all()
    CONTEXT = {
        "title":"Blogs",
        "blogs":model,
        "categories":Category.objects.all()
    }
    return render(request,"blog/blogs.html",CONTEXT)


"""
Yeni Eklendi Kategoriye Ait Bloglar Listelenir
"""
def get_blogs_by_category(request,slug:str):
    CONTEXT = {
        "title":"Filtred Blogs",
        "blogs":Blog.objects.filter(category__slug=slug),
        "categories":Category.objects.all()
    }
    return render(request,"blog/blogs.html",CONTEXT)


  
"""
APP_DIR/urls.py düzenlenir
"""

from django.urls import path
from . import views

urlpatterns = [
    path("",views.index ,name="home"),
    path("index",views.index),
    path("blogs",views.blogs,name="blogs"),
    #path("blogs/<int:id>",views.blog_details,name="blog_detail"),#int tipinde bir id değişkeni alcagımı soyledim 
    path("blogs/<str:slug>",views.blog_detail_with_slug, name="blog_detail"),

    """
    Yeni Eklendi Kategori Filtrelenmesi İçin
    slug:slug olsada str:slug olsada calışır
    """
    path("blogs/filter/<slug:slug>",views.get_blogs_by_category, name="filter_blog"),
]

"""
VE SON OLARAKTA CATEGORI VIEWI GÜNCELLENIR
"""
```
```django
<!--APP_DIR/static/partials/_categories.html-->
<div class="card">
  <ul class="list-group list-group-flush">
    {% for category in categories %}
    <li class="list-group-item">
      <a href="{% url 'filter_blog' category.slug %}">
        {{category.name|title}}<!--Title Ifadesi Capitalize Conversion yapar-->
      </a>
    </li>
    {% endfor %}
  </ul>
</div>
```

### Seçilen Kategorinini Renkelendirilmesi
```py
def get_blogs_by_category(request,slug:str):
    CONTEXT = {
        "title":"Filtred Blogs",
        "blogs":Blog.objects.filter(category__slug=slug),
        "categories":Category.objects.all(),
        "selected_slug":slug#Seçilen İfadeyi Html sayfasına Göndeririz
    }
    return render(request,"blog/blogs.html",CONTEXT)
```
```django
<!--BASE_DIR/static/_categories.html-->
<div class="card">
  <ul class="list-group list-group-flush">
    {% for category in categories %} {% if category.slug == selected_slug %}<!--Gelen Kategori İle Dongudeki kategori aynı ise active stili verilir etikete-->
    <li class="list-group-item active">
      <a
        style="text-decoration: none; color: black"
        href="{% url 'filter_blog' category.slug %}"
      >
        {{category.name|title}}
      </a>
    </li>
    {% else %}
    <li class="list-group-item">
      <a
        style="text-decoration: none; color: black"
        href="{% url 'filter_blog' category.slug %}"
      >
        {{category.name|title}}
      </a>
    </li>
    {% endif %} {% endfor %}
  </ul>
</div>
```

### Herhangi Bir Kategori Bulunmazsa Nolcak?
```django
{% extends 'base.html' %} {% block content %}
<div class="row vh-100 mt-2">
  <div class="col-4">{% include "partials/_categories.html" %}</div>
  <div class="col-8">
  <!--Eğer Sayfaya Gönderdiğim blogs listesi uzunlugu 0 dan buyukse o zaman listele-->
    {% if blogs|length > 0 %} 
    {% for blog in blogs %}
    <!---->
    {% include "blog/partials/_cardcontent.html" %}
    <!---->
    {% endfor %} 
    <!--Ama Değilse Tek bir div içinde uyarı dön-->
    {% else %}
    <div class="alert alert-danger">No Blog Found</div>
    {% endif %}
  </div>
</div>
{% endblock content %}

```
