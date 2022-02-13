from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class Article(models.Model):
    author =  models.ForeignKey("auth.User", verbose_name=("Yazar"), on_delete=models.CASCADE)
    title = models.CharField(max_length=50, verbose_name=("Başlık"))
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=("Oluşturulma Tarihi"))
    article_image = models.FileField(blank = True, null = True,verbose_name="Makaleye Fotoğraf Ekle")
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_date'] # Makaleler tarihe göre en son eklenenden ilk eklenene göre sıralanacak
class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name=("Makale"), on_delete=models.CASCADE, related_name="comments")
    comment_author = models.CharField(max_length=50, verbose_name="İsim")
    comment_content = models.CharField(max_length=200, verbose_name="Yorum")
    comment_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_content
    class Meta:
        ordering = ['-comment_date'] # Yorumlar tarihe göre en son eklenenden ilk eklenene göre sıralanacak