from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Blog,Category

#Statik Veri Oluşturlur
# DATA = {
#     "blogs" : [
#         {
#             "id":1,
#             "title":"Design",
#             "img":"design.jpg",
#             "description":"Design Blog",
#         }, {
#             "id":2,
#             "title":"Bt And Software",
#             "img":"bt-and-software.jpg",
#             "description":"Bt And Software"
#         }, {
#             "id":3,
#             "title":"Photography",
#             "img":"photography.jpg",
#             "description":"Photography Blog",
#         }, {
#             "id":4,
#             "title":"Software Development",
#             "img":"software-development.jpg",
#             "description":"Software Development Blog",
#         }
#     ]
# }

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

def blog_details(request,id:int):
    #return HttpResponse(f"Blog Details id:{id}")
    model = Blog.objects.get(id=id) 
    CONTEXT = {
        "title":"Blog Detail",
        "blog":model
    }
    return render(request,"blog/blog-details.html",CONTEXT)


def blog_detail_with_slug(request,slug:str):
    model = Blog.objects.get(slug=slug) 
    CONTEXT = {
        "title":"Blog Detail",
        "blog":model
    }
    return render(request,"blog/blog-details.html",CONTEXT)

def get_blogs_by_category(request,slug:str):
    CONTEXT = {
        "title":"Filtred Blogs",
        "blogs":Blog.objects.filter(category__slug=slug),
        "categories":Category.objects.all(),
        "selected_slug":slug
    }
    return render(request,"blog/blogs.html",CONTEXT)