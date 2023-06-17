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

    
