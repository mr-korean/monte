from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.http import JsonResponse
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

def validate_username(request):
    # HttpRequest(백그라운드 데이터 교환) 객체의 GET 과 POST 속성은 django.http.QueryDict 의 인스턴스입니다.
    # 서버에 GET 방식으로 요청을 보내서 'username'을 받아오되, 없으면 'None'을 반환한다. https://goo.gl/wtA6KN
    username = request.GET.get('username', None)
    data = {
        # <필드명>__iexact는 대소문자를 구분하지 않고(구분할 경우 exact) 일치하는 값을 찾는다. https://goo.gl/5XywcT
        # exists()는 쿼리셋에 결과가 있을 경우 True를 반환한다. https://goo.gl/Vgtr2u
        # (사실 생략해도 되지만, 더 정확한 결과를 얻으려면 써 주는 게 좋다고 한다)
        'is_taken' : User.objects.filter(username__iexact=username).exists()
    }   
    if data['is_taken']:
        data['error_message'] = '해당 계정은 이미 사용중입니다. 다른 아이디를 입력하십시오.'
    # data를 Json형식으로 인코딩한다.
    return JsonResponse(data)

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