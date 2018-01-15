from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy

class HomeView(TemplateView):
    template_name = 'home.html'

class UserRegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')

class UserRegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'

class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': ("두 비밀번호가 일치하지 않습니다."),
    }
    password1 = forms.CharField(label=("비밀번호"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=("비밀번호 확인"),
                                widget=forms.PasswordInput,
                                help_text=("가입 확인을 위해 위에 입력했던 비밀번호를 다시 적어주세요."))

    class Meta:
        model = User
        fields = ("username"),

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user