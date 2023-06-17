from django.urls import path
from . import views

urlpatterns = [
    path("",views.index ,name="home"),
    path("index",views.index),
    path("blogs",views.blogs,name="blogs"),
    #path("blogs/<int:id>",views.blog_details,name="blog_detail"),#int tipinde bir id değişkeni alcagımı soyledim 
    path("blogs/<str:slug>",views.blog_detail_with_slug, name="blog_detail"),
    path("blogs/filter/<slug:slug>",views.get_blogs_by_category, name="filter_blog"),
]

