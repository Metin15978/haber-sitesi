from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify
from django.contrib import admin
from django.contrib.auth.models import User

class AdminNews(admin.ModelAdmin):
    list_display = ('news_title', 'category', 'created_at', 'updated_at', 'is_delete','slug','delete_date')
    readonly_fields = ['slug','created_at','updated_at']


class Categories(models.Model):
    category_name=models.CharField(max_length=30,verbose_name="Kategori") 

    class Meta:
        verbose_name="Kategori"
        verbose_name_plural="Kategoriler"

    def __str__(self):
        return self.category_name



class News(models.Model):

    user = models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE,null=True)
    news_title = models.CharField(max_length=200, verbose_name="Haber Başlığı")
    news_front=models.TextField(default="")
    news_image = models.FileField(upload_to="NewsImages/", blank=False, verbose_name="Haber Resmi")
    category = models.ForeignKey(Categories,max_length=50, verbose_name="Haberin Kategorisi",on_delete=models.CASCADE,default=None)
    slug = models.SlugField(verbose_name=('Url'), editable=False, null=True, blank=True)
    news_content = RichTextUploadingField()
    view_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(verbose_name=("Oluşturulma Tarihi"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=("Son Güncellenme Tarihi"), auto_now=True)
    is_delete = models.BooleanField(verbose_name=("Silindi mi?"), default=False, help_text="Haberler silindi mi silinmedi mi?")
    delete_date = models.DateTimeField(verbose_name=("Silinme Tarihi"), blank=True, null=True)

    class Meta:
        verbose_name = "Haber"
        verbose_name_plural = "Haberler"

    def __str__(self):
        return self.news_title


    def save(self, *args, **kwargs):
        self.slug = f"{slugify(self.news_title.replace('ı','i'))}" 
        super().save(*args, **kwargs)
        
class Comment(models.Model):
    news = models.ForeignKey(News, related_name = 'comments', on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length = 50)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f"Comment by {self.name} on {self.news.news_title}"
    
class NewsView(models.Model):
    news = models.ForeignKey(News, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.news.news_title} viewed by {self.user.username} at {self.created_at}"