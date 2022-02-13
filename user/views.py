from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
# Create your views here.

def registerUser(request):
    # ALTERNATİF KAYIT YÖNTEMİ (KISA)
    form = RegisterForm(request.POST or None)
    if form.is_valid(): # Eğer parolalar uyuşuyorsa kayıt işlemi başlar
        username = form.cleaned_data.get("username") # username datası alındı
        password = form.cleaned_data.get("password") # password datası alındı
            
        newUser = User(username = username) # user tablosuna username kayıt yapılıyor
        newUser.set_password(password) # user tablosuna password kayıt yapılıyor
        newUser.save() # user tablosuna yeni kullanıcı username ve password kayıt edildi 
        login(request,newUser)  # kayıt sonrası otomatik olarak kullanıcı girişi yapıldı
        messages.success(request,"Başarıyla Kayıt Oldunuz")
        return redirect("index") # ana sayfaya yönlendirildi
    context = {
        "form" : form # form değişkeni form bağlamına kaydedildi
    }
    return render(request, "register.html",context) # sayfa url yapısında 'user/register/' yapısı çalıştığında register.html çalışır ve context sözlüğü html dosyasına gönderilir
    
    # ALTERNATİF KAYIT YÖNTEMİ (UZUN)
    """
    if request.method == "POST": # kayıt ol butonuna basıldı ve POST request yapıldı
        form = RegisterForm(request.POST) # POST işlemi gerçekleşti
        if form.is_valid(): # Eğer parolalar uyuşuyorsa kayıt işlemi başlar
            username = form.cleaned_data.get("username") # username datası alındı
            password = form.cleaned_data.get("password") # password datası alındı
            
            newUser = User(username = username) # user tablosuna username kayıt yapılıyor
            newUser.set_password(password) # user tablosuna password kayıt yapılıyor
            newUser.save() # user tablosuna yeni kullanıcı username ve password kayıt edildi 
            login(request)  # kayıt sonrası otomatik olarak kullanıcı girişi yapıldı
            return redirect("index") # ana sayfaya yönlendirildi
        context = {
            "form" : form # form değişkeni form bağlamına kaydedildi
        }
        return render(request, "register.html",context) # sayfa url yapısında 'user/register/' yapısı çalıştığında register.html çalışır ve context sözlüğü html dosyasına gönderilir
    else: # sadece GET request yapıldı ve sayfa görülüyor
        form = RegisterForm() # registerform olıuışturuldu ve sayfada görüldü
        context = {
            "form" : form # form değişkeni form bağlamına kaydedildi
        }
        return render(request, "register.html",context) # sayfa url yapısında 'user/register/' yapısı çalıştığında register.html çalışır ve context sözlüğü html dosyasına gönderilir
    """
    
def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid(): 
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        
        user = authenticate(username = username, password = password) # authenticate giriş işleminde girilen username ve password datalarını veritabanındaki kayıtlı kullanıcılarla karşılaştırdı eğer böyle bir kullanıcı mevcut ise True değeri dönderdi
        if user is None: # authenticate  kullanıcıyı bulamadı ve hata mesajı yayınlandı
            messages.info(request, "Kullanıcı Adı veya Parola Hatalı !")
            return render(request, "login.html",context)   
        messages.success(request, "Basarıyla Giriş Yaptınız") # authenticate kullanıcıyı buldu ve olumlu mesaj yayınlandı
        login(request,user)
        return redirect("index") # ana sayfaya yönlendirildi
    return render(request, "login.html",context) 
    
def logoutUser(request):
    logout(request)
    messages.success(request, "Başarıyla Çıkış Yapıldı")
    return redirect("index")