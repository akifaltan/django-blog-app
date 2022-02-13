from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from .forms import ArticleForm
from .models import Article,Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

# Bütün Makalelerin Bulunduğu Sayfa
def articles(request):
    keyword = request.GET.get("keyword")
    
    if keyword:
        articles = Article.objects.filter(title__contains=keyword) # arama çubuğunda yazılan başlık bilgilerini filtreler
        return render(request, "articles.html",{"articles":articles})
    articles = Article.objects.all()
    return render(request, "articles.html",{"articles":articles})

# Ana Sayfa
def index(request):
    return render(request, "index.html")

# Hakkımda Sayfası
def about(request):
    return render(request, "about.html")

# Giriş Yapılan Kullanıcının Makalelerinin Bulunduğu Sayfa
@login_required(login_url ="user:login") # Giriş yapılmamışsa fonksiyon çalışmaz ve kullanıcı giriş sayfasına yönlendirir(Güvenlik Amaçlı)
def dashboard(request):
    articles = Article.objects.filter(author = request.user) # sistemde giriş yapmış olan kullanıcının makale bilgilerini sözlüğe kaydedildi
    context = {
        "articles":articles
    }
    return render(request, "dashboard.html",context)

# Makale Ekleme Sayfası
@login_required(login_url ="user:login")# Giriş yapılmamışsa fonksiyon çalışmaz ve kullanıcı giriş sayfasına yönlendirir(Güvenlik Amaçlı)
def addArticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None) 
    
    if form.is_valid():
        article = form.save(commit=False) # yazılan makalenin formu oluşturuldu lakin kaydedilmedi çünkü makale author(yazar) bilgisi girilmedi
        article.author = request.user # makale author(yazar) bilgisi user bilgisinden alındı ve eklendi
        article.save() # makale kaydedildi
        
        messages.success(request, "Makale Başarıyla Oluşturuldu") # kayıt edildiğine dair olumlu mesaj yayınlandı
        return redirect("article:dashboard") # giriş yapmış olan kullanıcının makalelerinin bulunduğu sayfaya yönlendirildi
    return render(request, "addarticle.html",{"form":form})

# Detay Sayfası
def detail(request,id):
    article = get_object_or_404(Article, id = id) # 'get_object_or_404' fonksiyonu eğer id numarası geçersiz, hiç olmayan bir link döndürülürse 404 Not Found sayfası gösterilmsine sebep olacak
    
    comments = article.comments.all()
    
    return render(request, "detail.html",{"article":article,"comments":comments})

# Makale Düzenleme Sayfası
@login_required(login_url ="user:login") # Giriş yapılmamışsa fonksiyon çalışmaz ve kullanıcı giriş sayfasına yönlendirir(Güvenlik Amaçlı)
def updateArticle(request,id):
    article = get_object_or_404(Article,id=id)
    form = ArticleForm(request.POST or None,request.FILES or None,instance = article)
    
    if form.is_valid():
        article = form.save(commit=False) # yazılan makalenin formu oluşturuldu lakin kaydedilmedi çünkü makale author(yazar) bilgisi girilmedi
        article.author = request.user # makale author(yazar) bilgisi user bilgisinden alındı ve eklendi
        article.save() # makale kaydedildi
        
        messages.success(request, "Makale Başarıyla Güncellendi") # kayıt edildiğine dair olumlu mesaj yayınlandı
        return redirect("article:dashboard") # giriş yapmış olan kullanıcının makalelerinin bulunduğu sayfaya yönlendirildi
    
    return render(request, "update.html",{"form":form})

# Makale Silme İşlemi
@login_required(login_url ="user:login") # Giriş yapılmamışsa fonksiyon çalışmaz ve kullanıcı giriş sayfasına yönlendirir(Güvenlik Amaçlı)
def deleteArticle(request,id):
    article = get_object_or_404(Article,id=id)
    article.delete()
    messages.success(request, "Makale Başarıyla Silindi")
    return redirect("article:dashboard")

@login_required(login_url ="user:login") # Giriş yapılmamışsa fonksiyon çalışmaz ve kullanıcı giriş sayfasına yönlendirir(Güvenlik Amaçlı)
def addComment(request,id):
    article = get_object_or_404(Article,id=id)
    
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        newComment = Comment(comment_author=comment_author, comment_content=comment_content)
        newComment.article = article  
        newComment.save()
    return redirect(reverse("article:detail",kwargs={"id":id}))
        
    
