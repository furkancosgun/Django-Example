from django.contrib import admin
from blog.models import Blog,Category
# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    #Admin Ekranında Gösterilcek Alanalar
    list_display = ("id","title","img","description","slug","category")

    #Admin Ekranında Change Ekranına Girmeden Değiştirilebilir Alanlar
    #burdaki önemli nokta editlenebilir alanaların
    #ilk  listeleme de olmaması gerektiğidir
    list_editable = ("img","description","category")

    #Arama Yardımı
    search_fields = ("title","description")

    #Bazi Alanlarında Sadece Okunabilir Olamsını Değişikliğe Kapalo Olmasını İsteyebilriz
    readonly_fields = ("slug",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name","slug")
    list_editable = ("name",)
    search_fields = ("name",)
    readonly_fields = ("slug",)

admin.site.register(Blog,BlogAdmin)
admin.site.register(Category,CategoryAdmin)