from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Parola",widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50,label="Kullanıcı Adı")
    password = forms.CharField(max_length=20,label="Parola",widget=forms.PasswordInput())
    confirm = forms.CharField(max_length=20,label="Parolayı Doğrula",widget=forms.PasswordInput())
    
    def clean(self): # Girilen parolaların eşleşme kontrolü 
        username = self.cleaned_data.get("username") # username datası alındı
        password = self.cleaned_data.get("password") # password datası alındı
        confirm = self.cleaned_data.get("confirm") # confirm datası alındı
        
        if password and confirm and password != confirm: # eğer password ve confirm girili ve eşleşmiyorsa ekrana hata mesajı yolla
            raise forms.ValidationError("Parolalar Eşleşmiyor") # hata mesajı gösterildi
        
        # eşleşme onaylandı
        values = {
            "username" : username, # username değişkeni username bağlamına kaydedildi
            "password" : password # password değişkeni password bağlamına kaydedildi
        }
        return values # values sözlüğü 'viesw.py' dosyasındaki fonksiyonların içindeki form.is_valid() kondtrolüne yollandı